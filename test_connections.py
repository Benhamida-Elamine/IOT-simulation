
import getpass
import mysql.connector
import psycopg2

def test_postgresql():
    print("\n--- Test de connexion PostgreSQL ---")

    

    connection = None

    try:
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="postgres",  
            user="postgres",
            password="***REMOVED***"
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
            host="localhost",
            port=3306,
            database="industrial_iot_dw",
            user="root",
            password="***REMOVED***"
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
