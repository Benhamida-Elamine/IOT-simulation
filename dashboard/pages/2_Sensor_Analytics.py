import pandas as pd
import plotly.express as px
import streamlit as st
from queries import get_metadata

st.set_page_config(page_title="Sensor Analytics", page_icon="📈", layout="wide")
st.title("📈 Sensor Analytics")
st.caption("Tendances et distributions à partir des mesures chargées.")

try:
    df = get_metadata()
except Exception as exc:
    st.error("Impossible de lire metadata.")
    st.exception(exc)
    st.stop()

if df.empty:
    st.info("Aucune mesure dans metadata.")
    st.stop()

candidates = {
    "Température": ["temperature", "temperature_c", "temp_c"],
    "Vibration": ["vibration", "vibration_mm_s", "vib_m_s", "vibration_m_s"],
    "RPM": ["rpm", "rotation_rpm"],
}
available = {label: next((c for c in names if c in df.columns), None) for label, names in candidates.items()}
available = {label: col for label, col in available.items() if col}
if not available:
    st.error(f"Colonnes de mesures non reconnues : {list(df.columns)}")
    st.stop()

label = st.selectbox("Mesure", list(available))
metric = available[label]
df[metric] = pd.to_numeric(df[metric], errors="coerce")
time_col = "measured_at" if "measured_at" in df.columns else ("timestamp" if "timestamp" in df.columns else None)

if time_col:
    df[time_col] = pd.to_datetime(df[time_col], errors="coerce")
    valid = df.dropna(subset=[time_col, metric])
    if "machine_id" in valid.columns:
        ids = sorted(valid["machine_id"].dropna().astype(str).unique())
        selected = st.multiselect("Machines", ids, default=ids[:min(8, len(ids))])
        valid = valid[valid["machine_id"].astype(str).isin(selected)]
    if not valid.empty:
        fig = px.line(valid.sort_values(time_col), x=time_col, y=metric, color="machine_id" if "machine_id" in valid.columns and valid["machine_id"].nunique() > 1 else None)
        st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.plotly_chart(px.histogram(df.dropna(subset=[metric]), x=metric, nbins=30, title=f"Distribution : {label}"), use_container_width=True)
with right:
    st.dataframe(df[metric].describe().rename_axis("Statistique").reset_index(name="Valeur"), use_container_width=True, hide_index=True)

if "machine_id" in df.columns:
    summary = df.groupby("machine_id")[metric].agg(["count", "mean", "min", "max"]).reset_index()
    summary.columns = ["Machine", "Nombre de mesures", "Moyenne", "Minimum", "Maximum"]
    st.subheader("Comparaison par machine")
    st.dataframe(summary.sort_values("Moyenne", ascending=False), use_container_width=True, hide_index=True)
