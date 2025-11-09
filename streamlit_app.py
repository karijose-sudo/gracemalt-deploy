import streamlit as st
import pandas as pd
import joblib
import numpy as np

# -----------------------------
# Load model and training columns
# -----------------------------
ensemble = joblib.load("models/ensemble_gracemalt.pkl")
train_columns = joblib.load("models/train_columns.pkl")

# -----------------------------
# Preprocessing function (same as training)
# -----------------------------
def preprocess_germination(df):
    df = df.copy()
    # Correct 120h chit count
    df["ChitCount_120"] = 100 - df["Chit Count  120hrs Post casting (Non GrwOn)-  GBK"]
    # Δ moisture
    df["ΔMC_48_72"] = df["MC after 72hrs Post casting"] - df["MC after  48 Hours Post casting  - (GBK)"]
    df["ΔMC_72_120"] = df["End of germination  Moisture "] - df["MC after 72hrs Post casting"]
    # Δ chit counts
    df["ΔChit_48_72"] = df["Chit count   72hrs"] - df["Chit Count  48hrs Post casting (GBK)"]
    df["ΔChit_72_120"] = df["ChitCount_120"] - df["Chit count   72hrs"]
    # Uniformity
    df["Uniformity_MC"] = df["ΔMC_72_120"] / df["ΔMC_48_72"].replace(0, np.nan)
    df["Uniformity_Chit"] = df["ΔChit_72_120"] / df["ΔChit_48_72"].replace(0, np.nan)
    # Coefficient of variation
    chit_cols = ["Chit Count  48hrs Post casting (GBK)", "Chit count   72hrs", "ChitCount_120"]
    df["Chit_CV"] = df[chit_cols].std(axis=1) / df[chit_cols].mean(axis=1) * 100
    # Efficiency
    df["Efficiency_48_72"] = df["ΔChit_48_72"] / df["ΔMC_48_72"].replace(0, np.nan)
    df["Efficiency_72_120"] = df["ΔChit_72_120"] / df["ΔMC_72_120"].replace(0, np.nan)
    # Drop raw columns no longer needed
    df = df.drop(columns=chit_cols + [
        "MC after  48 Hours Post casting  - (GBK)",
        "MC after 72hrs Post casting",
        "End of germination  Moisture "
    ])
    df = df.fillna(df.median())
    return df

# -----------------------------
# Streamlit UI with Accordion
# -----------------------------
st.set_page_config(page_title="Malt Friability Predictor", layout="centered")
st.title("🌾 Malt Friability Predictor")
st.markdown("Enter process parameters below to predict **Friability**")

# Collect user input
user_input = {}

# --- Pre-Steep ---
with st.expander("Pre-Steep Parameters", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        user_input['Grain Germinatio %'] = st.number_input('Grain Germinatio %', 0.0, 100.0, 98.0)
        user_input['Germination Capacity'] = st.number_input('Germination Capacity', 0.0, 100.0, 99.0)
        user_input['Germination Energy '] = st.number_input('Germination Energy', 0.0, 100.0, 96.0)
        user_input['Germination Energy 8mls'] = st.number_input('Germination Energy 8mls', 0.0, 100.0, 92.0)
        user_input['water Sensity '] = user_input['Germination Energy '] - user_input['Germination Energy 8mls']
        st.text(f"Calculated Water Sensitivity: {user_input['water Sensity ']:.2f}")
    with col2:
        user_input['Screens - eaml'] = st.number_input('Screens - eaml', 0.0, 10.0, 2.0)
        user_input['1000 corn Weight *c wgt'] = st.number_input('1000 Corn Weight (c wgt)', 0.0, 100.0, 38.0)
        user_input['Grain Nitrogen % N2'] = st.number_input('Grain Nitrogen % N2', 0.0, 10.0, 1.7)
        user_input['Rubbish %'] = st.number_input('Rubbish %', 0.0, 20.0, 0.5)
        user_input['Moisture Content'] = st.number_input('Moisture Content', 0.0, 50.0, 12.0)

# --- Steeping ---
with st.expander("Steeping Parameters", expanded=False):
    col3, col4 = st.columns(2)
    with col3:
        user_input['first wet phase'] = st.number_input('First wet phase (hrs)', 0.0, 20.0, 6.0)
        user_input['first dry phase'] = st.number_input('First dry phase (hrs)', 0.0, 25.0, 4.0)
        user_input['second wet phase'] = st.number_input('Second wet phase (hrs)', 0.0, 20.0, 5.5)
        user_input['second dry phase'] = st.number_input('Second dry phase (hrs)', 0.0, 20.0, 3.5)
        user_input['Steeping Duration'] = (
            user_input['first wet phase'] + user_input['first dry phase'] +
            user_input['second wet phase'] + user_input['second dry phase']
        )
        st.text(f"Calculated Total Steeping Duration: {user_input['Steeping Duration']:.2f} hrs")
    with col4:
        user_input['1st wet steep water temp '] = st.number_input('1st wet steep water temp (°C)', 0.0, 100.0, 18.0)
        user_input['2nd wet water temp  '] = st.number_input('2nd wet water temp (°C)', 0.0, 100.0, 20.0)
        user_input['End of Steep Mositure  Content '] = st.number_input('End of Steep Moisture Content (%)', 0.0, 50.0, 42.0)
        user_input['Hydration Index based on 50 Grains '] = st.number_input('Hydration Index (50 Grains)', 0.0, 100.0, 0.9)
        user_input['End of steep Chit Count)'] = st.number_input('End of Steep Chit Count (%)', 0.0, 100.0, 28.0)

# --- Germination ---
with st.expander("Germination Measurements", expanded=False):
    col5, col6 = st.columns(2)
    with col5:
        user_input['MC after  48 Hours Post casting  - (GBK)'] = st.number_input('MC 48 hrs (%)', 0.0, 100.0, 43.0)
        user_input['MC after 72hrs Post casting'] = st.number_input('MC 72 hrs (%)', 0.0, 100.0, 41.8)
        user_input['End of germination  Moisture '] = st.number_input('MC 120 hrs (%)', 0.0, 100.0, 37.8)
    with col6:
        user_input['Chit Count  48hrs Post casting (GBK)'] = st.number_input('Chit 48 hrs (%)', 0.0, 100.0, 95.0)
        user_input['Chit count   72hrs'] = st.number_input('Chit 72 hrs (%)', 0.0, 100.0, 97.0)
        user_input['Chit Count  120hrs Post casting (Non GrwOn)-  GBK'] = st.number_input('Chit 120 hrs (%)', 0.0, 100.0, 98.0)

# -----------------------------
# Preprocess and align input
# -----------------------------
input_df = pd.DataFrame([user_input])
input_df = preprocess_germination(input_df)
input_df = input_df[train_columns]

# -----------------------------
# Predict Friability
# -----------------------------
if st.button("Predict Friability"):
    prediction = ensemble.predict(input_df)
    st.success(f"Predicted Malt Friability: {prediction[0]:.2f}")
