# IOT-simulation — Pipeline de données IoT industriel

Simulation de capteurs de machines industrielles, stockage dans PostgreSQL, pipeline ETL Python vers un data warehouse MySQL, puis tableau de bord Streamlit.

```
simulateur Python ──► PostgreSQL (source) ──► ETL extract / transform / load ──► MySQL (warehouse) ──► Streamlit
 5 machines simulées   machines, sensors,      nettoyage, UTC, dédoublonnage,      tables + vues        6 pages
 1 mesure / 10 s       maintenance, metadata   chargement UPSERT idempotent        d'agrégation
```

## Structure

| Dossier | Rôle |
|---|---|
| `src/industrial_iot/` | Simulateur : `simulator.py` (modèle de mesure), `measurements.py` (état initial des machines), `database.py` (pool PostgreSQL), `main.py` (boucle) |
| `ETL/` | `Extraction.py` (PostgreSQL), `Transformation.py` (nettoyage), `Load.py` (MySQL, UPSERT), `Pipeline.py` (orchestration) |
| `sql/db_sources/` | Schéma et données de référence PostgreSQL |
| `sql/db_destination/` | Schéma MySQL et vues `machine_summary`, `maintenance_summary` |
| `sql/migrations/` | Scripts de correction des données créées par les anciennes versions |
| `dashboard/` | Application Streamlit multipage |
| `tests/` | Tests unitaires et test d'intégration de bout en bout |

## Modèle de simulation

Chaque machine part d'un état nominal (`measurements.py`). À chaque cycle :

```
X_n = X_(n-1) + 0.05 × (X_nominal − X_(n-1)) + bruit
```

Le terme de rappel empêche la dérive d'une marche aléatoire pure. Les valeurs sont bornées (température 0–150, vibration 0–100, rpm 0–5000) et le statut est calculé ainsi : `ALERT` si température > 100, vibration > 50 ou rpm > 4000 ; `STOPPED` si rpm = 0 ; sinon `RUNNING`. La génération est parallélisée par machine avec `ThreadPoolExecutor`, et l'insertion utilise un `ThreadedConnectionPool`.

## Installation (Windows / PowerShell)

Prérequis : Python 3.10+, PostgreSQL et MySQL 8.0.19+ en local.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env   # puis renseigner les identifiants
python test_connections.py
```

### Créer les bases

1. **PostgreSQL** (base `PG_DATABASE`), dans cet ordre : `sql/db_sources/machine.sql`, `captures.sql`, `maintenance.sql`, `metadata.sql`. Les scripts sont relançables.
2. **MySQL** (base `MYSQL_DATABASE`) : `sql/db_destination/create_tables.sql`, puis les deux scripts de `sql/db_destination/views/`.

### Bases créées avec une ancienne version

Les anciennes versions du simulateur écrivaient `MACHINE_0001` à `MACHINE_0005`, identifiants absents de la table `machines` (`MACHINE_01` à `MACHINE_20`) : les vues affichaient alors 0 mesure par machine. Après sauvegarde, exécuter `sql/migrations/001_align_machine_ids_postgres.sql` puis `002_align_machine_ids_mysql.sql`, puis recréer les vues.

## Exécution

```powershell
python src\industrial_iot\main.py                      # simulateur continu (Ctrl+C pour arrêter)
python src\industrial_iot\main.py --cycles 3 --interval 2
python ETL\Pipeline.py                                 # ETL complet, relançable sans doublon
streamlit run dashboard\Home.py
```

## Tests

```powershell
pytest                                   # tests unitaires (aucune base requise)
$env:IOT_INTEGRATION_TEST = "1"; pytest  # + test de bout en bout et pages du dashboard
ruff check .
```

Le test d'intégration crée ses propres bases `iot_simulation_test` dans PostgreSQL et MySQL, puis les supprime : les bases de travail ne sont pas modifiées. Il vérifie le simulateur, deux exécutions successives de l'ETL (idempotence), les vues et le rendu des six pages Streamlit.

## Choix techniques

- **Idempotence** : `INSERT … ON DUPLICATE KEY UPDATE` sur la clé primaire de chaque table. L'identifiant source des mesures (`metadata.id`) est conservé dans MySQL.
- **Fuseaux horaires** : PostgreSQL stocke des `TIMESTAMPTZ` ; l'ETL convertit en UTC avant MySQL, dont le type `DATETIME` ne conserve pas de fuseau.
- **Qualité** : les mesures sans machine, sans date, non numériques, infinies, NaN ou avec un rpm négatif sont rejetées. Les doublons `(machine_id, measured_at)` sont supprimés.
- **Sécurité** : identifiants uniquement dans `.env` (ignoré par Git), requêtes paramétrées, noms de tables en liste blanche.

## Journal de correction — octobre 2026

| Problème constaté | Correction |
|---|---|
| Le `rpm` émis était celui du cycle précédent | La mesure utilise le nouvel état |
| Température bornée à 100 alors que l'alerte exige > 100 : aucune alerte possible (0 sur 84 030 mesures) | Plages alignées sur les seuils (0–150, 0–100, 0–5000) |
| Marche aléatoire divergente (température observée entre 8 et 100 °C, rpm à 0) | Terme de rappel vers la valeur nominale |
| Identifiants `MACHINE_000X` absents de la table `machines` | Identifiants alignés + script de migration |
| `metadata.machine_id SERIAL PRIMARY KEY` dans le script source | Clé `id BIGSERIAL`, `machine_id` clé étrangère, index |
| Insertion de maintenance sans `maintenance_id` (échec `NOT NULL`) | `BIGSERIAL` + insertion relançable |
| Schéma MySQL du dépôt différent des colonnes sources : chargement impossible | Schéma aligné sur la source |
| Seconde exécution de l'ETL en erreur (clé dupliquée) | UPSERT |
| Vue `maintenance_summary` basée sur une colonne inexistante | Vue basée sur `cost_eur` ; page Maintenance mise à jour |
| Identifiants en dur, connexion ouverte à l'import | Lecture de `.env`, pool créé à la demande |
| `.env` et `__pycache__` versionnés | Retirés de l'index Git, `.env.example` ajouté |

### Limites connues

- L'ETL relit toute la table `metadata` à chaque exécution (chargement complet idempotent, pas incrémental).
- 5 machines sur 20 sont simulées. Pour en simuler davantage, ajouter leur état initial dans `measurements.py`.
- Aucun capteur physique n'est utilisé : toutes les mesures sont simulées.
- Le fichier `.env` a été présent dans l'historique Git : si ces mots de passe servent ailleurs, il faut les changer.
