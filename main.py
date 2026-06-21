import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
import time

# --- STAGE 1: DATABASE CONNECTION ---
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",          
            password="Jabeen@57",  
            database="EV_BMS_DB"
        )
    except mysql.connector.Error as err:
        st.error(f"Database Connection Error: {err}")
        return None

# --- STAGE 2: MATHEMATICAL / ML ESTIMATION LOGIC ---
def estimate_soc(voltage):
    """
    Simulates an Lithium-Ion OCV-SOC curve estimation.
    For a single cell: ~4.2V is 100%, ~3.0V is 0%.
    """
    # Normalized linear-interpolation fallback for simulation
    soc = ((voltage - 3.0) / (4.2 - 3.0)) * 100
    return max(0.0, min(100.0, round(soc, 2)))

def predict_thermal_status(temp, current):
    """
    Predictive Safety Rule Engine (Representing AI Boundary logic)
    """
    if temp > 45.0 or (abs(current) > 15.0 and temp > 40.0):
        return "CRITICAL: High Thermal Runaway Risk!", "🔴"
    elif temp > 38.0:
        return "WARNING: Elevated Temperature - Cooling Initiated", "🟡"
    else:
        return "HEALTHY: Nominal Operating Range", "🟢"

# --- STAGE 3: STREAMLIT FRONTEND DASHBOARD ---
st.set_page_config(page_title="AI-BMS Dashboard", page_icon="⚡", layout="wide")

st.title("⚡ AI-Driven EV Battery Management System (BMS)")
st.markdown("### Next-Gen Zero-Hardware Battery Simulation & Analytics Platform")
st.write("---")

# Sidebar for Hardware Simulation Controls
st.sidebar.header("🚗 Virtual Hardware Simulator")
st.sidebar.info("Adjust the sliders below to simulate live EV driving telemetry data writing directly to MySQL.")

sim_voltage = st.sidebar.slider("Cell Voltage (V)", 3.0, 4.2, 3.8, 0.05)
sim_current = st.sidebar.slider("Current Load (A)", -20.0, 20.0, -5.0, 0.5)
sim_temp = st.sidebar.slider("Cell Temperature (°C)", 20.0, 60.0, 35.0, 0.5)

if st.sidebar.button("Push Telemetry to MySQL"):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO BatteryTelemetry (voltage, current, temperature) VALUES (%s, %s, %s)"
        cursor.execute(query, (sim_voltage, sim_current, sim_temp))
        conn.commit()
        cursor.close()
        conn.close()
        st.sidebar.success("Telemetry Logged to Database!")

# Fetch Latest Data from MySQL for the Live Monitor
conn = get_db_connection()
if conn:
    query = "SELECT * FROM BatteryTelemetry ORDER BY id DESC LIMIT 10"
    df = pd.read_sql(query, conn)
    conn.close()

    if not df.empty:
        latest_entry = df.iloc[0]
        
        # Run AI/Estimation Algorithms on the fetched data
        computed_soc = estimate_soc(latest_entry['voltage'])
        status_msg, status_icon = predict_thermal_status(latest_entry['temperature'], latest_entry['current'])

        # KPI Layout Metrics Display
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="🔋 Estimated State of Charge (SOC)", value=f"{computed_soc} %")
        col2.metric(label="🔌 Live Voltage", value=f"{latest_entry['voltage']} V")
        col3.metric(label="📉 Current Draw", value=f"{latest_entry['current']} A")
        col4.metric(label="🌡️ Temperature", value=f"{latest_entry['temperature']} °C")

        # System Safety Banner Announcement
        st.write("---")
        st.subheader("System Health Status")
        if "CRITICAL" in status_msg:
            st.error(f"{status_icon} {status_msg}")
        elif "WARNING" in status_msg:
            st.warning(f"{status_icon} {status_msg}")
        else:
            st.success(f"{status_icon} {status_msg}")

        # Live Graphical Analytics
        st.write("---")
        st.subheader("📊 Telemetry History Logs (Pulled from MySQL)")
        
        # Formatting data frame for clean charting
        chart_data = df.copy().sort_values(by="id")
        
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.markdown("**Voltage Performance Profile Over Time**")
            st.line_chart(chart_data.set_index('timestamp')['voltage'])
            
        with col_chart2:
            st.markdown("**Thermal Fluctuations Profile Over Time**")
            st.line_chart(chart_data.set_index('timestamp')['temperature'])

        # Raw Data View
        with st.expander("📂 View Raw MySQL Log Table"):
            st.dataframe(df, use_container_width=True)
    else:
        st.info("Database is connected, but no logging history is present yet. Push data via the sidebar simulator.")
else:
    st.error("Please ensure your MySQL server is running locally and credentials match up inside the script.")