from pathlib import Path
import json
import pandas as pd
import streamlit as st
from src.predict import predict_risk, MODEL_PATH

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "iot_sensor_data.csv"
METRICS_PATH = ROOT / "outputs" / "metrics.json"

st.set_page_config(page_title="Predictive Maintenance Dashboard", page_icon="🛠️", layout="wide")
st.title("🛠️ AI-Powered Predictive Maintenance")
st.caption("Educational simulation dashboard — predictions are based on synthetic training data.")

if not MODEL_PATH.exists():
    st.warning("The model has not been trained yet. Stop the dashboard and run `python main.py` first.")
    st.stop()

st.sidebar.header("Simulated sensor readings")
temperature = st.sidebar.slider("Temperature (°C)", 20.0, 105.0, 65.0, 0.5)
vibration = st.sidebar.slider("Vibration (arbitrary units)", 0.0, 10.0, 2.5, 0.1)
current = st.sidebar.slider("Current (A)", 1.0, 18.0, 8.0, 0.1)

result = predict_risk(temperature, vibration, current)
left, middle, right = st.columns(3)
left.metric("Temperature", f"{temperature:.1f} °C")
middle.metric("Vibration", f"{vibration:.1f}")
right.metric("Current", f"{current:.1f} A")

if result["prediction"] == 1:
    st.error(f"⚠️ {result['risk']} RISK — {result['message']}")
else:
    st.success(f"✅ {result['risk']} RISK — {result['message']}")
st.progress(min(max(result["probability"], 0.0), 1.0), text=f"Model-estimated failure probability: {result['probability']:.1%}")

st.subheader("Training data overview")
if DATA_PATH.exists():
    df = pd.read_csv(DATA_PATH)
    a, b = st.columns(2)
    with a:
        st.write("Sample sensor data")
        st.dataframe(df.head(12), use_container_width=True)
    with b:
        st.write("Failure label counts")
        st.bar_chart(df["failure"].value_counts().sort_index().rename(index={0: "Normal", 1: "Failure risk"}))
else:
    st.info("Run `python main.py` to generate the dataset.")

if METRICS_PATH.exists():
    with open(METRICS_PATH, encoding="utf-8") as f:
        metrics = json.load(f)
    st.subheader("Model evaluation (held-out test split)")
    a, b, c, d = st.columns(4)
    a.metric("Accuracy", f"{metrics['accuracy']:.1%}")
    b.metric("Precision", f"{metrics['precision']:.1%}")
    c.metric("Recall", f"{metrics['recall']:.1%}")
    d.metric("F1 score", f"{metrics['f1_score']:.1%}")
    st.caption("These scores measure performance on a held-out portion of simulated data, not real industrial devices.")

for image_name, title in [
    ("confusion_matrix.png", "Confusion matrix"),
    ("feature_importance.png", "Feature importance"),
]:
    image_path = ROOT / "outputs" / image_name
    if image_path.exists():
        st.subheader(title)
        st.image(str(image_path), use_container_width=True)
