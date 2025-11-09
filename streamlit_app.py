import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# Load model and columns
# -----------------------------
model = joblib.load("models/ensemble_gracemalt.pkl")
columns = joblib.load("models/train_columns.pkl")

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Grace Malt Friability Predictor")
st.title("Grace Malt Friability Predictor")

st.write("""
Predict malt friability based on raw malting and germination features.
Fill in values for each section below.
""")

# Define feature sections
pre_steep_features = [
    'Grain Germinatio %', 'Germination Capacity', 'Germination Energy ',
    'Germination Energy 8mls', 'water Sensity ', 'Screens - eaml',
    '1000 corn Weight *c wgt', 'Grain Nitrogen % N2', 'Rubbish %',
    'Moisture Content'
]

steeping_features = [
    'first wet phase', 'first dry phase', 'second wet phase', 'second dry phase',
    'Steeping Duration', '1st wet steep water temp ', '2nd wet water temp  ',
    'End of Steep Mositure  Content ', 'Hydration Index based on 50 Grains ',
    'End of steep Chit Count)'
]

germination_features = [
    'MC after  48 Hours Post casting  - (GBK)', 'Chit Count  48hrs Post casting (GBK)',
    'Chit count   72hrs', 'MC after 72hrs Post casting',
    'Chit Count  120hrs Post casting (Non GrwOn)-  GBK',
    'Chit Count  120hrs Post casting (1/4 to 1/2)-  GBK',
    'Chit Count  120hrs Post casting (1/2 to 3/4)-  GBK',
    'Chit Count  120hrs Post casting (3/4 to Full (F) in GBK',
    'Chit Count  120hrs Post casting (Full Plus F+) in GBK',
    'End of germination  Moisture '
]

# Input dictionary
inputs = {}

with st.expander("Pre-Steep Features", expanded=True):
    for feat in pre_steep_features:
        inputs[feat] = st.number_input(f"{feat}", value=0.0)

with st.expander("Steeping Features", expanded=False):
    for feat in steeping_features:
        inputs[feat] = st.number_input(f"{feat}", value=0.0)

with st.expander("Germination Features", expanded=False):
    for feat in germination_features:
        inputs[feat] = st.number_input(f"{feat}", value=0.0)

# Predict button
if st.button("Predict Friability"):
    try:
        input_df = pd.DataFrame([inputs], columns=columns)
        prediction = model.predict(input_df)
        st.success(f"Predicted Malt Friability: {prediction[0]:.2f}")
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
