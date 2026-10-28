import pandas as pd
import plotly.express as px
import streamlit as st
from queries import get_machine_summary, get_metadata

st.set_page_config(page_title="Machine Monitoring", page_icon="⚙️", layout="wide")
st.title("⚙️ Machine Monitoring")
st.caption("Sélection d'une machine, indicateurs agrégés et historique.")

try:
    summary = get_machine_summary()
    measurements = get_metadata()
except Exception as exc:
    st.error("Lecture impossible. Vérifie les tables et vues SQL.")
    st.exception(exc)
    st.stop()

if summary.empty:
    st.info("Aucune machine dans la vue machine_summary.")
    st.stop()

machine_ids = summary["machine_id"].dropna().astype(str).sort_values().unique().tolist()
selected = st.selectbox("Machine", machine_ids)
machine_row = summary[summary["machine_id"].astype(str) == selected].iloc[0]
df = measurements[measurements["machine_id"].astype(str) == selected].copy() if "machine_id" in measurements.columns else pd.DataFrame()
time_col = "measured_at" if "measured_at" in df.columns else ("timestamp" if "timestamp" in df.columns else None)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Mesures", int(machine_row.get("measurement_count", 0)))
c2.metric("Température moyenne", f"{machine_row['avg_temperature']:.2f}" if pd.notna(machine_row.get("avg_temperature")) else "N/D")
c3.metric("Vibration moyenne", f"{machine_row['avg_vibration']:.2f}" if pd.notna(machine_row.get("avg_vibration")) else "N/D")
c4.metric("Dernière mesure", str(machine_row.get("last_measured_at", "N/D")))

metrics = [c for c in ["temperature", "temperature_c", "vibration", "vibration_mm_s", "rpm"] if c in df.columns]
if time_col and metrics:
    df[time_col] = pd.to_datetime(df[time_col], errors="coerce")
    metric = st.selectbox("Mesure à afficher", metrics)
    df[metric] = pd.to_numeric(df[metric], errors="coerce")
    df = df.dropna(subset=[time_col, metric]).sort_values(time_col)
    if not df.empty:
        st.plotly_chart(px.line(df, x=time_col, y=metric, title=f"{metric} — {selected}"), use_container_width=True)
else:
    st.info("Colonnes de mesures reconnues ou horodatage introuvables. Vérifie le schéma metadata.")

st.subheader("Historique des mesures")
st.dataframe(df.sort_values(time_col, ascending=False) if time_col and not df.empty else df, use_container_width=True, hide_index=True)
