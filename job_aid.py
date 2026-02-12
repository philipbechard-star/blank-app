import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- APP CONFIG ---
st.set_page_config(page_title="Field Pro Job Aid", layout="centered")

# --- DATA STORAGE ---
LOG_FILE = "job_history.csv"

def log_data(status, lat, lon):
    now = datetime.now()
    new_entry = pd.DataFrame([{
        "Timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "Status": status,
        "Latitude": lat,
        "Longitude": lon
    }])
    # Save to CSV
    new_entry.to_csv(LOG_FILE, mode='a', header=not os.path.exists(LOG_FILE), index=False)

# --- UI HEADER ---
st.title("🛠️ Repair Tech Assistant")
st.write("HVAC • Electronics • Appliances")

# --- SECTION 1: JOB TRACKER ---
st.header("Job Timer & Location")

# Initialize session state for the toggle
if 'on_job' not in st.session_state:
    st.session_state.on_job = False

# Placeholder for GPS (In a real browser, this uses the streamlit-js-eval component)
# For this IDE base code, we will simulate the coordinates
lat, lon = 40.7128, -74.0060 

if not st.session_state.on_job:
    if st.button("▶️ START JOB", use_container_width=True, type="primary"):
        st.session_state.on_job = True
        log_data("START", lat, lon)
        st.success(f"Started at {datetime.now().strftime('%H:%M:%S')}")
else:
    if st.button("🛑 END JOB", use_container_width=True, type="secondary"):
        st.session_state.on_job = False
        log_data("END", lat, lon)
        st.warning(f"Ended at {datetime.now().strftime('%H:%M:%S')}")

# --- SECTION 2: CALCULATIONS ---
st.divider()
st.header("Calculations")

tab1, tab2 = st.tabs(["Ohm's Law", "HVAC Heat"])

with tab1:
    st.subheader("Power & Resistance")
    volts = st.number_input("Voltage (V)", value=120.0)
    amps = st.number_input("Amperage (A)", value=0.0)
    if amps > 0:
        watts = volts * amps
        ohms = volts / amps
        st.metric("Power (Watts)", f"{watts} W")
        st.metric("Resistance", f"{ohms:.2f} Ω")

with tab2:
    st.subheader("Sensible Heat Formula")
    cfm = st.number_input("Airflow (CFM)", value=400)
    delta_t = st.number_input("Temp Rise/Drop (ΔT)", value=20)
    btuh = 1.08 * cfm * delta_t
    st.metric("Total BTU/h", f"{btuh:,.0f}")

# --- SECTION 3: RECENT LOGS ---
st.divider()
if os.path.exists(LOG_FILE):
    st.subheader("Recent Activity")
    df = pd.read_csv(LOG_FILE)
    st.dataframe(df.tail(5), use_container_width=True)
