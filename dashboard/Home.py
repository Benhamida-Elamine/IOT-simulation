import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection_status
from queries import (
    get_machine_summary, get_maintenance_summary, get_metadata,
    get_machines, get_sensors, get_maintenance, clear_query_cache
)

st.set_page_config(page_title="Industrial IoT | Overview", page_icon="🏭", layout="wide")
st.markdown("""
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
[data-testid="stMetric"] {background: rgba(128,128,128,.08); padding: 16px; border-radius: 12px; border: 1px solid rgba(128,128,128,.18);}
</style>
""", unsafe_allow_html=True)

st.title("🏭 Industrial IoT Platform")
st.caption("PostgreSQL → ETL Python → MySQL → Streamlit")

with st.sidebar:
    st.header("⚙️ Contrôles")
    if st.button("🔄 Recharger les données", use_container_width=True):
        clear_query_cache()
        st.rerun()

ok, message = get_connection_status()
if not ok:
    st.error("Connexion MySQL impossible. Vérifie les variables MYSQL_* dans le .env.")
    st.code(message)
    st.stop()

try:
    summary = get_machine_summary()
    measurements = get_metadata()
    maintenance = get_maintenance_summary()
    machines = get_machines()
    sensors = get_sensors()
except Exception as exc:
    st.error("Impossible de lire les données analytiques.")
    st.exception(exc)
    st.info("Vérifie que les tables et les vues SQL existent. Consulte les scripts sql/db_destination.")
    st.stop()

if summary.empty and machines.empty:
    st.warning("Aucune machine trouvée. Charge les données avec le pipeline ETL.")
    st.stop()

machine_count = summary["machine_id"].nunique() if "machine_id" in summary.columns else len(summary)
measurement_count = int(summary["measurement_count"].sum()) if "measurement_count" in summary.columns else len(measurements)
sensor_count = sensors["sensor_id"].nunique() if "sensor_id" in sensors.columns else len(sensors)
alert_count = 0
if "avg_temperature" in summary.columns:
    alert_count += int((pd.to_numeric(summary["avg_temperature"], errors="coerce") >= 80).sum())
if "avg_vibration" in summary.columns:
    alert_count += int((pd.to_numeric(summary["avg_vibration"], errors="coerce") >= 7).sum())
last_measurement = pd.to_datetime(summary.get("last_measured_at"), errors="coerce").max() if "last_measured_at" in summary.columns else pd.NaT

c1, c2, c3, c4 = st.columns(4)
c1.metric("Machines", f"{machine_count:,}".replace(",", " "))
c2.metric("Mesures", f"{measurement_count:,}".replace(",", " "))
c3.metric("Capteurs", f"{sensor_count:,}".replace(",", " "))
c4.metric("Machines à surveiller", f"{alert_count:,}".replace(",", " "), help="Seuils de démonstration : température moyenne ≥ 80 ou vibration moyenne ≥ 7. À adapter.")

st.divider()
left, right = st.columns([1.6, 1])
with left:
    st.subheader("📈 État des machines")
    if not summary.empty and "avg_temperature" in summary.columns and "avg_vibration" in summary.columns:
        fig = px.scatter(
            summary, x="avg_temperature", y="avg_vibration",
            size="measurement_count" if "measurement_count" in summary.columns else None,
            color="machine_status" if "machine_status" in summary.columns else None,
            hover_name="machine_id", hover_data=["machine_name"] if "machine_name" in summary.columns else None,
            labels={"avg_temperature": "Température moyenne", "avg_vibration": "Vibration moyenne"}
        )
        fig.update_layout(margin=dict(l=10,r=10,t=20,b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Les colonnes nécessaires au graphique ne sont pas disponibles.")
with right:
    st.subheader("🛠️ Interventions par machine")
    if not maintenance.empty and "maintenance_count" in maintenance.columns:
        top = maintenance.sort_values("maintenance_count", ascending=False).head(10)
        label = "machine_name" if "machine_name" in top.columns else "machine_id"
        fig = px.bar(top, x=label, y="maintenance_count", hover_data=["machine_id"])
        fig.update_layout(xaxis_title="", yaxis_title="Interventions", margin=dict(l=10,r=10,t=20,b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée de maintenance disponible.")

st.subheader("📋 Synthèse par machine (jointure + agrégations SQL)")
if not summary.empty:
    columns = [c for c in [
        "machine_id", "machine_name", "machine_type", "machine_status",
        "measurement_count", "last_measured_at", "avg_temperature",
        "max_temperature", "avg_vibration", "max_vibration", "avg_rpm"
    ] if c in summary.columns]
    st.dataframe(summary[columns], use_container_width=True, hide_index=True)

with st.expander("Détails des tables chargées"):
    st.write(f"Mesures : {len(measurements)}")
    st.write(f"Machines : {len(machines)}")
    st.write(f"Capteurs : {len(sensors)}")
