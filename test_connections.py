
import os

import mysql.connector
import psycopg2
from dotenv import load_dotenv

# Les identifiants sont lus dans le fichier .env (jamais écrits dans le code).
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

def test_postgresql():
    print("\n--- Test de connexion PostgreSQL ---")



    connection = None

    try:
        connection = psycopg2.connect(
            host=os.getenv("PG_HOST", "localhost"),
            port=int(os.getenv("PG_PORT", "5432")),
            dbname=os.getenv("PG_DATABASE", "postgres"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
        )

        cursor = connection.cursor()
        cursor.execute("SELECT current_database(), version()")

        result = cursor.fetchone()

        print("Connexion PostgreSQL réussie !")
        print("Base utilisée :", result[0])
        print("Version :", result[1].split(",")[0])

        cursor.close()

    except Exception as error:
        print("Échec de la connexion PostgreSQL.")
        print("Erreur :", error)

    finally:
        if connection is not None:
            connection.close()
            print("Connexion PostgreSQL fermée.")


def test_mysql():
    print("\n--- Test de connexion MySQL ---")



    connection = None

    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            port=int(os.getenv("MYSQL_PORT", "3306")),
            database=os.getenv("MYSQL_DATABASE", "industrial_iot_dw"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
        )

        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE(), VERSION()")

        result = cursor.fetchone()

        print("Connexion MySQL réussie !")
        print("Base utilisée :", result[0])
        print("Version :", result[1])

        cursor.close()

    except Exception as error:
        print("Échec de la connexion MySQL.")
        print("Erreur :", error)

    finally:
        if connection is not None and connection.is_connected():
            connection.close()
            print("Connexion MySQL fermée.")


if __name__ == "__main__":
    test_postgresql()
    test_mysql()
