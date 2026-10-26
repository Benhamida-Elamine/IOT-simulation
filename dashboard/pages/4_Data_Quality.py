import streamlit as st
import pandas as pd
from db import load_data

st.set_page_config(page_title="Data Quality", page_icon="🛡️", layout="wide")
st.title("🛡️ Data Quality")
st.caption("Profiling descriptif des tables de destination. Les rejets ETL nécessitent une table de logs dédiée.")

data, errors = load_data()
tables = ["machines", "sensors", "metadata", "maintenance"]
cards = st.columns(4)
for col, table in zip(cards, tables):
    col.metric(f"Lignes · {table}", f"{len(data[table]):,}".replace(",", " "))

table = st.selectbox("Table", tables)
df = data[table]
if df.empty:
    st.warning(f"La table {table} est vide ou indisponible.")
    if errors.get(table): st.code(errors[table])
    st.stop()

quality = pd.DataFrame({
    "Colonne": df.columns,
    "Valeurs nulles": [int(df[c].isna().sum()) for c in df.columns],
    "% nulles": [round(float(df[c].isna().mean() * 100), 2) for c in df.columns],
    "Valeurs distinctes": [int(df[c].nunique(dropna=True)) for c in df.columns],
})
st.subheader("Complétude par colonne")
st.dataframe(quality, use_container_width=True, hide_index=True)
st.subheader("Doublons exacts")
st.metric("Lignes dupliquées", int(df.duplicated().sum()))
st.subheader("Aperçu")
st.dataframe(df.head(200), use_container_width=True, hide_index=True)
