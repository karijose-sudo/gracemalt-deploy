import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("models/ensemble_gracemalt_raw.pkl")

# Feature names (raw features only)
columns = [
    'Grain Germinatio %', 'Germination Capacity', 'Germination Energy ',
    'Germination Energy 8mls', 'water Sensity ', 'Screens - eaml',
    '1000 corn Weight *c wgt', 'Grain Nitrogen % N2', 'Rubbish %',
    'Moisture Content', 'first wet phase', 'first dry phase',
    'second wet phase', 'second dry phase', 'Steeping Duration',
    '1st wet steep water temp ', '2nd wet water temp  ',
    'End of Steep Mositure  Content ', 'Hydration Index based on 50 Grains ',
    'End of steep Chit Count)', 'MC after  48 Hours Post casting  - (GBK)',
    'Chit Count  48hrs Post casting (GBK)', 'Chit count   72hrs',
    'MC after 72hrs Post casting', 'Chit Count  120hrs Post casting (Non GrwOn)-  GBK',
    'Chit Count  120hrs Post casting (1/4 to 1/2)-  GBK',
    'Chit Count  120hrs Post casting (1/2 to 3/4)-  GBK',
    'Chit Count  120hrs Post casting (3/4 to Full (F) in GBK',
    'Chit Count  120hrs Post casting (Full Plus F+) in GBK',
    'End of germination  Moisture '
]

st.set_page_config(page_title="Malt Friability Predictor", layout="centered")
st.title("🌾 Malt Friability Predictor")
st.markdown("Enter raw process parameters to predict **Friability**")

# -----------------------------
# Helper function for bounded input
# -----------------------------
def bounded_number_input(label, min_value=0.0, max_value=100.0, value=None):
    return st.number_input(label, min_value=min_value, max_value=max_value, value=value)

# --- Pre-Steep Parameters ---
with st.expander("Pre-Steep Parameters", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        grain_germ = bounded_number_input('Grain Germinatio %', value=98.0)
        germ_cap = bounded_number_input('Germination Capacity', value=99.0)
        germ_energy = bounded_number_input('Germination Energy', value=96.0)
        germ_energy_8ml = bounded_number_input('Germination Energy 8mls', value=92.0)
        water_sens = bounded_number_input('Water Sensitivity', min_value=0.0, max_value=10.0, value=1.2)
    with col2:
        screens = bounded_number_input('Screens - eaml', min_value=0.0, max_value=10.0, value=2.0)
        corn_weight = bounded_number_input('1000 Corn Weight *c wgt', min_value=0.0, max_value=100.0, value=35.0)
        nitrogen = bounded_number_input('Grain Nitrogen % N2', min_value=0.0, max_value=10.0, value=1.8)
        rubbish = bounded_number_input('Rubbish %', min_value=0.0, max_value=20.0, value=0.5)
        moisture = bounded_number_input('Moisture Content', min_value=0.0, max_value=50.0, value=12.0)

# --- Steeping Parameters ---
with st.expander("Steeping Parameters", expanded=False):
    col3, col4 = st.columns(2)
    with col3:
        first_wet = bounded_number_input('First wet phase (hrs)', min_value=0.0, max_value=20.0, value=6.0)
        first_dry = bounded_number_input('First dry phase (hrs)', min_value=0.0, max_value=25.0, value=4.0)
        second_wet = bounded_number_input('Second wet phase (hrs)', min_value=0.0, max_value=20.0, value=5.5)
        second_dry = bounded_number_input('Second dry phase (hrs)', min_value=0.0, max_value=20.0, value=3.5)
        steep_duration = first_wet + first_dry + second_wet + second_dry
        st.text(f"Total Steeping Duration: {steep_duration:.2f} hrs")
    with col4:
        wet_temp1 = bounded_number_input('1st wet steep water temp (°C)', min_value=0.0, max_value=100.0, value=18.0)
        wet_temp2 = bounded_number_input('2nd wet water temp (°C)', min_value=0.0, max_value=100.0, value=20.0)
        end_steep_moisture = bounded_number_input('End of Steep Moisture Content (%)', min_value=0.0, max_value=50.0, value=42.0)
        hydration_index = bounded_number_input('Hydration Index (50 Grains)', min_value=0.0, max_value=100.0, value=0.9)
        end_steep_chit = bounded_number_input('End of Steep Chit Count (%)', min_value=0.0, max_value=100.0, value=28.0)

# --- Germination Measurements ---
with st.expander("Germination Measurements", expanded=False):
    col5, col6 = st.columns(2)
    with col5:
        mc_48 = bounded_number_input('MC 48 hrs (%)', value=43.0)
        mc_72 = bounded_number_input('MC 72 hrs (%)', value=41.8)
        mc_120 = bounded_number_input('MC 120 hrs (%)', value=37.8)
    with col6:
        chit_48 = bounded_number_input('Chit Count 48 hrs (%)', value=95.0)
        chit_72 = bounded_number_input('Chit Count 72 hrs (%)', value=97.0)
        chit_120_non = bounded_number_input('Chit Count 120hrs (Non GrwOn)', value=98.0)
        chit_120_14 = bounded_number_input('Chit Count 120hrs (1/4 to 1/2)', value=5.0)
        chit_120_12 = bounded_number_input('Chit Count 120hrs (1/2 to 3/4)', value=7.0)
        chit_120_34 = bounded_number_input('Chit Count 120hrs (3/4 to Full F)', value=8.0)
        chit_120_full = bounded_number_input('Chit Count 120hrs (Full Plus F+)', value=12.0)
        end_germ_moist = bounded_number_input('End of germination Moisture (%)', value=37.0)

# -----------------------------
# Prepare input for prediction
# -----------------------------
user_input = [
    grain_germ, germ_cap, germ_energy, germ_energy_8ml, water_sens, screens,
    corn_weight, nitrogen, rubbish, moisture, first_wet, first_dry,
    second_wet, second_dry, steep_duration, wet_temp1, wet_temp2,
    end_steep_moisture, hydration_index, end_steep_chit,
    mc_48, chit_48, chit_72, mc_72,
    chit_120_non, chit_120_14, chit_120_12, chit_120_34, chit_120_full,
    end_germ_moist
]

input_df = pd.DataFrame([user_input], columns=columns)

# Predict button
if st.button("Predict Friability"):
    try:
        prediction = model.predict(input_df)
        st.success(f"Predicted Malt Friability: **{prediction[0]:.2f}**")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
