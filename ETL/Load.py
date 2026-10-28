
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


# Clé primaire de chaque table de destination.
# Elle sert à mettre à jour une ligne existante au lieu de la dupliquer.
PRIMARY_KEYS = {
    "machines": ["machine_id"],
    "sensors": ["sensor_id"],
    "metadata": ["id"],
    "maintenance": ["maintenance_id"],
}


def load_table(connection, table_name, rows):
    """
    Insère ou met à jour les lignes dans une table MySQL (UPSERT).
    Relancer le pipeline donne donc le même résultat, sans doublon.
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
    if table_name not in PRIMARY_KEYS:
        raise ValueError(f"Table non autorisée : {table_name}")

    for column in columns:
        if not column.replace("_", "").isalnum():
            raise ValueError(f"Nom de colonne invalide : {column}")

    column_names = ", ".join(f"`{column}`" for column in columns)
    placeholders = ", ".join(["%s"] * len(columns))

    primary_key = PRIMARY_KEYS[table_name]
    missing_keys = [key for key in primary_key if key not in columns]
    if missing_keys:
        raise ValueError(
            f"{table_name} : clé primaire absente des données ({', '.join(missing_keys)})."
        )

    update_columns = [column for column in columns if column not in primary_key]
    # Si toutes les colonnes font partie de la clé, une ligne existante est simplement conservée.
    updates = ", ".join(
        f"`{column}` = new_row.`{column}`" for column in update_columns or primary_key
    )

    query = (
        f"INSERT INTO `{table_name}` ({column_names}) "
        f"VALUES ({placeholders}) AS new_row "
        f"ON DUPLICATE KEY UPDATE {updates}"
    )

    values = [
        tuple(row[column] for column in columns)
        for row in rows
    ]

    cursor = connection.cursor()

    try:
        cursor.executemany(query, values)
        print(f"{table_name} : {len(values)} lignes chargées (insérées ou mises à jour).")
        return len(values)
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
