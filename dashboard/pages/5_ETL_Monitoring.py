import streamlit as st
from db import load_data

st.set_page_config(page_title="ETL Monitoring", page_icon="🔄", layout="wide")
st.title("🔄 ETL Monitoring")
st.caption("Volumes chargés dans les tables de destination.")

st.info(
    "Cette page affiche les volumes actuellement présents. Pour un vrai historique d'exécution "
    "(date, durée, statut, lignes extraites/chargées/rejetées), ajoute une table et une journalisation dans Pipeline.py."
)
data, errors = load_data()
cols = st.columns(4)
for col, table in zip(cols, ["machines", "sensors", "metadata", "maintenance"]):
    col.metric(f"Lignes · {table}", f"{len(data[table]):,}".replace(",", " "))
with st.expander("Erreurs de lecture"):
    if errors:
        for table, error in errors.items():
            st.write(f"**{table}**")
            st.code(error)
    else:
        st.success("Aucune erreur de lecture.")
