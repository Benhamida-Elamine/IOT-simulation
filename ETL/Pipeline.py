
from Extraction import (
    extract_machines,
    extract_maintenance,
    extract_metadata,
    extract_sensors,
    get_postgres_connection,
)
from Load import (
    get_mysql_connection,
    load_machines,
    load_maintenance,
    load_metadata,
    load_sensors,
)
from Transformation import (
    transform_machines,
    transform_maintenance,
    transform_metadata,
    transform_sensors,
)


def run_pipeline():
    pg_connection = None
    mysql_connection = None

    try:
        print("=== Démarrage du pipeline ETL ===")

        # 1. Connexion aux bases
        pg_connection = get_postgres_connection()
        mysql_connection = get_mysql_connection()

        # 2. Extraction depuis PostgreSQL
        print("\n--- Extraction ---")

        raw_machines = extract_machines(pg_connection)
        raw_sensors = extract_sensors(pg_connection)
        raw_metadata = extract_metadata(pg_connection)
        raw_maintenance = extract_maintenance(pg_connection)

        # 3. Transformation des données
        print("\n--- Transformation ---")

        machines = transform_machines(raw_machines)
        sensors = transform_sensors(raw_sensors)
        metadata = transform_metadata(raw_metadata)
        maintenance = transform_maintenance(raw_maintenance)

        # 4. Chargement dans MySQL
        # Les machines sont chargées en premier,
        # car les autres tables peuvent les référencer.
        print("\n--- Chargement dans MySQL ---")

        load_machines(mysql_connection, machines)
        load_sensors(mysql_connection, sensors)
        load_metadata(mysql_connection, metadata)
        load_maintenance(mysql_connection, maintenance)

        # Valider la transaction uniquement si tout a réussi
        mysql_connection.commit()

        print("\n=== Pipeline ETL terminé avec succès ===")

    except Exception as error:
        if mysql_connection is not None:
            mysql_connection.rollback()

        print(f"\nÉchec du pipeline ETL : {error}")
        raise

    finally:
        if pg_connection is not None:
            pg_connection.close()

        if mysql_connection is not None:
            mysql_connection.close()


if __name__ == "__main__":
    run_pipeline()
