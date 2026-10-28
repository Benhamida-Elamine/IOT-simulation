import os
import sys

# Le simulateur et l'ETL sont lancés comme des scripts (imports « plats ») :
# on ajoute leurs dossiers au chemin d'import pour les tests.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for folder in ("src/industrial_iot", "ETL"):
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path:
        sys.path.insert(0, path)
