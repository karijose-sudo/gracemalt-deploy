import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load your trained model
model_path = os.path.join("models", "gracemalt_model.pkl")
with open(model_path, "rb") as file:
    model = pickle.load(file)

# -----------------------------
# Streamlit App UI
# -----------------------------
st.set_page_config(page_title="Malt Friability Predictor", layout="centered")
st.title("🌾 Malt Friability Predictor")
st.markdown("Enter process parameters below to predict **Friability**")

# -----------------------------
# Pre-Steep Section (Collapsible)
# -----------------------------
with st.expander("Pre-Steep Section", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        grain_germination = st.number_input("Grain Germination %", 0.0, 100.0, 95.0)
        germ_capacity = st.number_input("Germination Capacity", 0.0, 100.0, 98.0)
        germ_energy = st.number_input("Germination Energy", 0.0, 100.0, 97.0)
        germ_energy_8ml = st.number_input("Germination Energy (8ml)", 0.0, 100.0, 95.0)
        water_sensitivity = st.number_input("Water Sensitivity", 0.0, 100.0, 3.0)
    with col2:
        screens = st.number_input("Screens - eaml", 0.0, 100.0, 2.0)
        thousand_cw = st.number_input("1000 Corn Weight *c wgt", 0.0, 60.0, 45.0)
        grain_nitrogen = st.number_input("Grain Nitrogen % N2", 0.0, 3.0, 1.5)
        rubbish = st.number_input("Rubbish %", 0.0, 10.0, 1.0)
        moisture = st.number_input("Moisture Content", 0.0, 20.0, 12.0)

# -----------------------------
# Steeping Section (Collapsible)
# -----------------------------
with st.expander("Steeping Section", expanded=False):
    col3, col4 = st.columns(2)
    with col3:
        first_wet = st.number_input("First Wet Phase (hrs)", 0.0, 24.0, 8.0)
        first_dry = st.number_input("First Dry Phase (hrs)", 0.0, 24.0, 8.0)
        second_wet = st.number_input("Second Wet Phase (hrs)", 0.0, 24.0, 8.0)
        second_dry = st.number_input("Second Dry Phase (hrs)", 0.0, 24.0, 4.0)
        steep_duration = st.number_input("Steeping Duration (hrs)", 0.0, 72.0, 48.0)
    with col4:
        wet_temp1 = st.number_input("1st Wet Water Temp (°C)", 0.0, 50.0, 16.0)
        wet_temp2 = st.number_input("2nd Wet Water Temp (°C)", 0.0, 50.0, 16.0)
        end_moisture = st.number_input("End of Steep Moisture Content (%)", 0.0, 50.0, 44.0)
        hydration_index = st.number_input("Hydration Index (50 Grains)", 0.0, 100.0, 48.0)
        chit_count_steep = st.number_input("End of Steep Chit Count", 0.0, 100.0, 70.0)

# -----------------------------
# Germination Section (Collapsible)
# -----------------------------
with st.expander("Germination Section", expanded=False):
    col5, col6 = st.columns(2)
    with col5:
        mc_48 = st.number_input("MC after 48 Hours Post Casting", 0.0, 100.0, 45.0)
        chit_48 = st.number_input("Chit Count 48hrs Post Casting", 0.0, 100.0, 80.0)
        chit_72 = st.number_input("Chit Count 72hrs", 0.0, 100.0, 85.0)
        mc_72 = st.number_input("MC after 72hrs Post Casting", 0.0, 100.0, 46.0)
        chit_120_ng = st.number_input("Chit Count 120hrs (Non GrwOn)", 0.0, 100.0, 5.0)
    with col6:
        chit_120_qh = st.number_input("Chit Count 120hrs (1/4 to 1/2)", 0.0, 100.0, 15.0)
        chit_120_hq = st.number_input("Chit Count 120hrs (1/2 to 3/4)", 0.0, 100.0, 30.0)
        chit_120_3qf = st.number_input("Chit Count 120hrs (3/4 to Full)", 0.0, 100.0, 45.0)
        chit_120_fp = st.number_input("Chit Count 120hrs (Full Plus F+)", 0.0, 100.0, 5.0)
        end_moisture_germ = st.number_input("End of Germination Moisture", 0.0, 100.0, 46.0)

# -----------------------------
# Prepare input for prediction
# -----------------------------
features = np.array([[ 
    grain_germination, germ_capacity, germ_energy, germ_energy_8ml, water_sensitivity,
    screens, thousand_cw, grain_nitrogen, rubbish, moisture,
    first_wet, first_dry, second_wet, second_dry, steep_duration,
    wet_temp1, wet_temp2, end_moisture, hydration_index, chit_count_steep,
    mc_48, chit_48, chit_72, mc_72, chit_120_ng, chit_120_qh,
    chit_120_hq, chit_120_3qf, chit_120_fp, end_moisture_germ
]])

# -----------------------------
# Prediction Button
# -----------------------------
if st.button("Predict Friability"):
    try:
        prediction = model.predict(features)
        st.success(f"Predicted Friability: **{prediction[0]:.2f}**")
    except Exception as e:
        st.error(f"An error occurred: {e}")
