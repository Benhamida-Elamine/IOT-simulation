
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_mysql_connection():
    """Ouvre une connexion à la base MySQL."""
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=os.getenv("MYSQL_DATABASE", "industrial_iot_dw"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
    )


def load_table(connection, table_name, rows):
    """
    Insère les lignes dans une table MySQL.
    Les noms de tables sont définis par le programme,
    et les valeurs sont transmises avec des paramètres SQL.
    """
    if not rows:
        print(f"{table_name} : aucune ligne à charger.")
        return 0

    columns = list(rows[0].keys())

    # Vérifie que toutes les lignes possèdent les mêmes colonnes.
    if any(set(row.keys()) != set(columns) for row in rows):
        raise ValueError(
            f"Les lignes de {table_name} n'ont pas toutes les mêmes colonnes."
        )

    # Les noms de tables et de colonnes doivent provenir
    # de notre schéma connu, jamais de données utilisateur.
    allowed_tables = {
        "machines",
        "sensors",
        "metadata",
        "maintenance",
    }

    if table_name not in allowed_tables:
        raise ValueError(f"Table non autorisée : {table_name}")

    for column in columns:
        if not column.replace("_", "").isalnum():
            raise ValueError(f"Nom de colonne invalide : {column}")

    column_names = ", ".join(f"`{column}`" for column in columns)
    placeholders = ", ".join(["%s"] * len(columns))

    query = (
        f"INSERT INTO `{table_name}` ({column_names}) "
        f"VALUES ({placeholders})"
    )

    values = [
        tuple(row[column] for column in columns)
        for row in rows
    ]

    cursor = connection.cursor()

    try:
        cursor.executemany(query, values)
        inserted = cursor.rowcount
        print(f"{table_name} : {inserted} lignes insérées.")
        return inserted
    finally:
        cursor.close()


def load_machines(connection, rows):
    """Charge les machines dans MySQL."""
    return load_table(connection, "machines", rows)


def load_sensors(connection, rows):
    """Charge les capteurs dans MySQL."""
    return load_table(connection, "sensors", rows)


def load_metadata(connection, rows):
    """Charge les mesures dans MySQL."""
    return load_table(connection, "metadata", rows)


def load_maintenance(connection, rows):
    """Charge l'historique de maintenance dans MySQL."""
    return load_table(connection, "maintenance", rows)
