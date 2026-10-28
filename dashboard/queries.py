"""SQL access layer for the Streamlit dashboards."""
import pandas as pd
import streamlit as st
from db import get_connection


@st.cache_data(ttl=30)
def _read_query(query_name: str) -> pd.DataFrame:
    # Only predefined query names are accepted; SQL is never supplied by a user.
    queries = {
        "machine_summary": "SELECT * FROM machine_summary ORDER BY avg_vibration DESC",
        "maintenance_summary": "SELECT * FROM maintenance_summary ORDER BY maintenance_count DESC",
        "metadata": "SELECT * FROM metadata ORDER BY measured_at DESC",
        "machines": "SELECT * FROM machines",
        "sensors": "SELECT * FROM sensors",
        "maintenance": "SELECT * FROM maintenance ORDER BY maintenance_date DESC",
    }
    if query_name not in queries:
        raise ValueError(f"Requête inconnue : {query_name}")

    connection = get_connection()
    try:
        return pd.read_sql(queries[query_name], connection)
    finally:
        connection.close()

def get_machine_summary() -> pd.DataFrame:
    return _read_query("machine_summary")

def get_maintenance_summary() -> pd.DataFrame:
    return _read_query("maintenance_summary")

def get_metadata() -> pd.DataFrame:
    return _read_query("metadata")

def get_machines() -> pd.DataFrame:
    return _read_query("machines")

def get_sensors() -> pd.DataFrame:
    return _read_query("sensors")

def get_maintenance() -> pd.DataFrame:
    return _read_query("maintenance")

def clear_query_cache() -> None:
    _read_query.clear()
