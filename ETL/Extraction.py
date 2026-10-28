
import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()


def get_postgres_connection():
    return psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
        dbname=os.getenv("PG_DATABASE"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
    )


def extract_machines(connection):
    """Extrait les informations des machines."""
    query = """
        SELECT *
        FROM machines
        ORDER BY machine_id;
    """

    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    print(f"machines : {len(rows)} lignes extraites.")
    return rows


def extract_sensors(connection):
    """Extrait les informations des capteurs."""
    query = """
        SELECT *
        FROM sensors;
    """

    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    print(f"sensors : {len(rows)} lignes extraites.")
    return rows


def extract_metadata(connection):
    """Extrait les mesures des machines."""
    query = """
        SELECT *
        FROM metadata
        ORDER BY measured_at;
    """

    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    print(f"metadata : {len(rows)} lignes extraites.")
    return rows


def extract_maintenance(connection):
    """Extrait l'historique de maintenance."""
    query = """
        SELECT *
        FROM maintenance;
    """

    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    print(f"maintenance : {len(rows)} lignes extraites.")
    return rows


# if __name__ == "__main__":
#     connection = None
#
#     try:
#         connection = get_postgres_connection()
#
#         machines = extract_machines(connection)
#         sensors = extract_sensors(connection)
#         metadata = extract_metadata(connection)
#         maintenance = extract_maintenance(connection)
#
#         print("\nExtraction terminée.")
#
#     except psycopg2.Error as error:
#         print(f"Erreur PostgreSQL : {error}")
#
#     finally:
#         if connection is not None:
#             connection.close()
#             print("Connexion PostgreSQL fermée.")
#
