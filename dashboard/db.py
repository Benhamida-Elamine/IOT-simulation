"""MySQL connection helpers used by Streamlit."""
import os
import pandas as pd
import mysql.connector
import streamlit as st
from dotenv import load_dotenv

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(ROOT_DIR, ".env"))

TABLES = ("machines", "sensors", "metadata", "maintenance")

def get_connection():
    required = ("MYSQL_USER", "MYSQL_PASSWORD")
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise RuntimeError("Variables manquantes dans .env : " + ", ".join(missing))
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=os.getenv("MYSQL_DATABASE", "industrial_iot_dw"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        connection_timeout=5,
    )

def get_connection_status():
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        return True, "Connexion MySQL réussie."
    except Exception as exc:
        return False, str(exc)
    finally:
        if connection is not None and connection.is_connected():
            connection.close()

@st.cache_data(ttl=30)
def _read_table(table_name: str) -> pd.DataFrame:
    if table_name not in TABLES:
        raise ValueError(f"Table non autorisée : {table_name}")
    connection = get_connection()
    try:
        return pd.read_sql(f"SELECT * FROM `{table_name}`", connection)
    finally:
        connection.close()

def load_data():
    result, errors = {}, {}
    for table in TABLES:
        try:
            result[table] = _read_table(table)
        except Exception as exc:
            result[table] = pd.DataFrame()
            errors[table] = str(exc)
    return result, errors
