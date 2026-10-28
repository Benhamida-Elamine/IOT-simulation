"""Test de bout en bout : simulateur -> PostgreSQL -> ETL -> MySQL -> vues.

Nécessite PostgreSQL et MySQL accessibles avec les identifiants du fichier .env.
Le test crée puis supprime ses propres bases (iot_simulation_test) :
les bases de travail ne sont jamais modifiées.

Lancement : IOT_INTEGRATION_TEST=1 pytest tests/test_integration.py
"""
import os
import re

import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("IOT_INTEGRATION_TEST") != "1",
    reason="définir IOT_INTEGRATION_TEST=1 pour lancer le test d'intégration",
)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEST_DB = "iot_simulation_test"
SOURCE_SCRIPTS = ["machine.sql", "captures.sql", "maintenance.sql", "metadata.sql"]
DESTINATION_SCRIPTS = ["create_tables.sql", "views/machine_summary.sql", "views/maintenance_summary.sql"]


def read_sql(*parts):
    with open(os.path.join(ROOT_DIR, "sql", *parts), encoding="utf-8") as file:
        return file.read()


def split_statements(script):
    """Découpe un script SQL simple (sans ';' dans les chaînes) en requêtes."""
    script = re.sub(r"--[^\n]*", "", script)
    return [statement.strip() for statement in script.split(";") if statement.strip()]


@pytest.fixture(scope="module")
def databases():
    from dotenv import load_dotenv

    load_dotenv(os.path.join(ROOT_DIR, ".env"))
    import mysql.connector
    import psycopg2

    admin_pg = psycopg2.connect(
        host=os.getenv("PG_HOST"), port=os.getenv("PG_PORT"), dbname=os.getenv("PG_DATABASE"),
        user=os.getenv("PG_USER"), password=os.getenv("PG_PASSWORD"),
    )
    admin_pg.autocommit = True
    admin_my = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"), port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"), password=os.getenv("MYSQL_PASSWORD"),
    )

    with admin_pg.cursor() as cursor:
        cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DB}")
        cursor.execute(f"CREATE DATABASE {TEST_DB}")
    cursor = admin_my.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DB}")
    cursor.execute(f"CREATE DATABASE {TEST_DB}")
    cursor.close()

    os.environ["PG_DATABASE"] = TEST_DB
    os.environ["MYSQL_DATABASE"] = TEST_DB

    # Schéma source, exécuté deux fois pour vérifier que les scripts sont relançables.
    pg = psycopg2.connect(
        host=os.getenv("PG_HOST"), port=os.getenv("PG_PORT"), dbname=TEST_DB,
        user=os.getenv("PG_USER"), password=os.getenv("PG_PASSWORD"),
    )
    for _ in range(2):
        with pg.cursor() as cursor:
            for script in SOURCE_SCRIPTS:
                cursor.execute(read_sql("db_sources", script))
        pg.commit()

    from Load import get_mysql_connection

    my = get_mysql_connection()
    cursor = my.cursor()
    for script in DESTINATION_SCRIPTS:
        for statement in split_statements(read_sql("db_destination", script)):
            cursor.execute(statement)
    cursor.close()

    yield pg, my

    pg.close()
    my.close()
    with admin_pg.cursor() as cursor:
        cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DB} WITH (FORCE)")
    cursor = admin_my.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DB}")
    cursor.close()
    admin_pg.close()
    admin_my.close()


def count(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    value = cursor.fetchone()[0]
    cursor.close()
    return value


def test_pipeline_de_bout_en_bout(databases):
    pg, my = databases
    from main import run
    from measurements import measurements_init
    from Pipeline import run_pipeline

    # Intervalle non nul : deux mesures d'une même machine au même instant seraient
    # considérées comme doublons par l'ETL (l'horloge Windows a une résolution d'environ 15 ms).
    run(cycles=3, interval=0.05)
    expected = 3 * len(measurements_init)
    assert count(pg, "SELECT COUNT(*) FROM metadata") == expected
    assert count(pg, "SELECT COUNT(*) FROM maintenance") == 8
    assert count(pg, "SELECT COUNT(*) FROM sensors") == 60

    # Deux exécutions : la seconde ne doit ni échouer ni créer de doublons.
    run_pipeline()
    run_pipeline()
    my.commit()  # rafraîchit l'instantané de lecture de la connexion de test

    assert count(my, "SELECT COUNT(*) FROM machines") == 20
    assert count(my, "SELECT COUNT(*) FROM sensors") == 60
    assert count(my, "SELECT COUNT(*) FROM maintenance") == 8
    assert count(my, "SELECT COUNT(*) FROM metadata") == expected

    # Les mesures sont bien rattachées aux machines de référence.
    assert count(my, "SELECT COUNT(*) FROM machine_summary WHERE measurement_count = 3") == len(measurements_init)
    assert count(my, "SELECT ROUND(SUM(total_cost_eur)) FROM maintenance_summary") == 3380


@pytest.mark.parametrize("page", [
    "Home.py",
    "pages/1_Machine_Monitoring.py",
    "pages/2_Sensor_Analytics.py",
    "pages/3_Maintenance.py",
    "pages/4_Data_Quality.py",
    "pages/5_ETL_Monitoring.py",
])
def test_pages_dashboard_sans_erreur(databases, page):
    import sys

    from streamlit.testing.v1 import AppTest

    dashboard_dir = os.path.join(ROOT_DIR, "dashboard")
    if dashboard_dir not in sys.path:
        sys.path.insert(0, dashboard_dir)

    app = AppTest.from_file(os.path.join(dashboard_dir, page), default_timeout=60).run()
    assert not app.exception, [e.message for e in app.exception]
    assert not app.error, [e.value for e in app.error]
