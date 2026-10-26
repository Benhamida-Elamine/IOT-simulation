import streamlit as st
import plotly.express as px
from queries import get_maintenance_summary, get_maintenance

st.set_page_config(page_title="Maintenance", page_icon="🛠️", layout="wide")
st.title("🛠️ Maintenance Analytics")
st.caption("Jointure des machines, de la maintenance et des agrégats de mesures.")

try:
    summary = get_maintenance_summary()
    history = get_maintenance()
except Exception as exc:
    st.error("Lecture impossible. Vérifie les tables et vues SQL.")
    st.exception(exc)
    st.stop()

if summary.empty and history.empty:
    st.info("Aucune donnée de maintenance. Vérifie la table maintenance et le chargement ETL.")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Machines", summary["machine_id"].nunique() if "machine_id" in summary.columns else 0)
c2.metric("Interventions", int(summary["maintenance_count"].sum()) if "maintenance_count" in summary.columns else len(history))
c3.metric("Minutes d'arrêt cumulées", int(summary["total_downtime_minutes"].fillna(0).sum()) if "total_downtime_minutes" in summary.columns else "N/D")

if "maintenance_count" in summary.columns:
    label = "machine_name" if "machine_name" in summary.columns else "machine_id"
    fig = px.bar(summary.sort_values("maintenance_count", ascending=False), x=label, y="maintenance_count", hover_data=["machine_id"])
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Maintenance et état des mesures")
cols = [c for c in ["machine_id", "machine_name", "maintenance_count", "last_maintenance_at", "total_downtime_minutes", "last_measured_at", "avg_temperature", "avg_vibration"] if c in summary.columns]
st.dataframe(summary[cols], use_container_width=True, hide_index=True)

st.subheader("Historique des interventions")
st.dataframe(history, use_container_width=True, hide_index=True)
