# Industrial IoT Streamlit dashboards

## Pré-requis
Les tables MySQL `machines`, `sensors`, `metadata`, `maintenance` doivent exister et correspondre au schéma réel. Les vues `machine_summary` et `maintenance_summary` doivent être créées après adaptation du script au schéma réel.

## Installer
Depuis la racine du projet :
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r .\dashboard\requirements.txt
streamlit run .\dashboard\Home.py
```

## Créer tables et vues
1. Inspecter le schéma actuel de MySQL.
2. Adapter `sql/db_destination/create_tables.sql` aux colonnes réelles. Ne pas l'exécuter aveuglément sur des tables existantes.
3. Exécuter le script de tables uniquement si tu crées la destination depuis zéro.
4. Créer les vues avec les scripts dans `sql/db_destination/views/`.
5. Lancer Streamlit.

## Important
Les scripts SQL fournis sont des modèles de départ. Ils supposent notamment :
- `machines(machine_id, name, machine_type, status, created_at)`
- `sensors(sensor_id, machine_id, sensor_type, unit, installed_at)`
- `metadata(machine_id, temperature, vibration, rpm, status, measured_at)`
- `maintenance(machine_id, maintenance_date, maintenance_type, description, duration_minutes, status)`

Si tes tables actuelles diffèrent, adapte les scripts ou envoie-moi leur structure pour que je les ajuste. Ne supprime pas les tables existantes sans sauvegarde.
