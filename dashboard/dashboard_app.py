import streamlit as st
import pandas as pd
import requests
import sqlite3
from datetime import datetime
import plotly.express as px
import pytz

# === PAGE CONFIG ===
st.set_page_config(page_title="Smart Energy Dashboard", layout="centered")

# === LANGUAGE SYSTEM ===
LANGS = {
    "en": {
        "title": "🏢 Smart Energy Monitoring Dashboard",
        "intro": "🔌 AI-Powered Prediction for Building Energy Usage",
        "temperature": "Temperature (°C)",
        "humidity": "Humidity (%)",
        "occupancy": "Occupancy",
        "hour": "Hour of Day",
        "day": "Day of Week",
        "occupied": "Occupied",
        "empty": "Empty",
        "submit": "🔮 Predict Energy Usage",
        "result": "⚡ Predicted Energy Consumption",
        "history": "📜 Prediction History",
        "chart": "📊 Energy Forecast Timeline",
        "api_error": "❌ API Error"
    },
    "ar": {
        "title": "🏢 لوحة مراقبة الطاقة الذكية",
        "intro": "🔌 التنبؤ الذكي باستهلاك الطاقة في المباني",
        "temperature": "درجة الحرارة (°م)",
        "humidity": "الرطوبة (%)",
        "occupancy": "الإشغال",
        "hour": "الساعة",
        "day": "اليوم",
        "occupied": "مشغول",
        "empty": "فارغ",
        "submit": "🔮 توقع استهلاك الطاقة",
        "result": "⚡ استهلاك الطاقة المتوقع",
        "history": "📜 سجل التنبؤات",
        "chart": "📊 الرسم البياني للتنبؤ بالطاقة",
        "api_error": "❌ خطأ في API"
    }
}

# === DATABASE SETUP ===
DB_PATH = "dashboard/history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            humidity REAL,
            occupancy INTEGER,
            hour INTEGER,
            dayofweek INTEGER,
            predicted_kwh REAL
        )
    """)
    conn.commit()
    conn.close()

def save_prediction(data, prediction):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions (timestamp, temperature, humidity, occupancy, hour, dayofweek, predicted_kwh)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data["temperature"],
        data["humidity"],
        data["occupancy"],
        data["hour"],
        data["dayofweek"],
        prediction
    ))
    conn.commit()
    conn.close()

def load_predictions():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM predictions ORDER BY timestamp DESC", conn)
    conn.close()
    return df

# === DASHBOARD START ===
# Language Switch
lang_code = st.sidebar.selectbox("🌐 Language / اللغة", options=["en", "ar"], index=0)
L = LANGS[lang_code]

st.title(L["title"])
st.caption(L["intro"])
st.markdown("---")

# Init DB
init_db()

# API endpoint
API_URL = "http://127.0.0.1:8000/predict"

# === INPUT FORM ===
st.subheader("📥 Input")
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        temperature = st.number_input(L["temperature"], min_value=10.0, max_value=40.0, value=26.0)
        occupancy = st.selectbox(L["occupancy"], [0, 1], format_func=lambda x: L["occupied"] if x else L["empty"])
    with col2:
        humidity = st.number_input(L["humidity"], min_value=10, max_value=90, value=50)
        hour = st.slider(L["hour"], 0, 23, datetime.now(pytz.timezone("Asia/Tehran")).hour)

    dayofweek = st.selectbox(L["day"], list(range(7)), format_func=lambda x: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][x])
    submitted = st.form_submit_button(L["submit"])

if submitted:
    input_data = {
        "temperature": temperature,
        "humidity": humidity,
        "occupancy": occupancy,
        "hour": hour,
        "dayofweek": dayofweek
    }

    try:
        response = requests.post(API_URL, json=input_data)
        result = response.json()
        predicted = result["predicted_energy_kwh"]

        st.success(f"{L['result']}: {predicted} kWh")

        save_prediction(input_data, predicted)

    except Exception as e:
        st.error(f"{L['api_error']}: {e}")

# === HISTORY & CHART ===
st.markdown("---")
st.subheader(L["history"])
df = load_predictions()

if df is not None and not df.empty:
    st.dataframe(df.head(10))

    st.subheader(L["chart"])
    fig = px.line(df.sort_values("timestamp"), x="timestamp", y="predicted_kwh",
                  labels={"timestamp": "Time", "predicted_kwh": "kWh"},
                  title="Energy Forecast Over Time")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No prediction history yet.")
