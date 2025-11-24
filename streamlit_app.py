import streamlit as st
import pandas as pd
import joblib

# ----------------------------------------------
# Load model and columns
# ----------------------------------------------

model = joblib.load("models/ensemble_gracemalt.pkl")
columns = joblib.load("models/train_columns.pkl")

st.set_page_config(page_title="Grace Malt Friability Predictor")
st.title("Grace Malt Friability Predictor")
st.write("Enter your malt batch parameters below to predict friability.")

# ----------------------------------------------
# Minimum Realistic Values
# ----------------------------------------------

min_values = {
    'Grain Germinatio %': 98.0,
    'Germination Capacity': 96.0,
    'Germination Energy ': 44.0,
    'Germination Energy 8mls': 5.0,
    'water Sensity ': 1.0,
    'Screens - eaml': 0.1,
    '1000 corn Weight *c wgt': 31.0,
    'Grain Nitrogen % N2': 1.25,
    'Rubbish %': 0.1,
    'Moisture Content': 10.7,
    'First wet steep water temp ': 10.0,
    'Second wet water temp  ': 9.0,
    'End of Steep Mositure  Content ': 38.0,
    'Hydration Index based on 50 Grains ': 70.0,
    'End of steep Chit Count)': 40.0,
    'MC after  48 Hours Post casting  - (GBK)': 39.0,
    'Chit Count  48hrs Post casting (GBK)': 82.0,
    'Chit count   72hrs': 91.0,
    'MC after 72hrs Post casting': 35.9,
    'Chit Count  120hrs Post casting (Non GrwOn)-  GBK': 1.0,
    'Chit Count  120hrs Post casting (1/4 to 1/2)-  GBK': 2.0,
    'Chit Count  120hrs Post casting (1/2 to 3/4)-  GBK': 6.0,
    'Chit Count  120hrs Post casting (3/4 to Full (F) in GBK': 21.0,
    'Chit Count  120hrs Post casting (Full Plus F+) in GBK': 1.0,
    'End of germination  Moisture ': 34.2
}

# ----------------------------------------------
# Feature Groups
# ----------------------------------------------

pre_steep_features = [
    'Grain Germinatio %', 'Germination Capacity', 'Germination Energy ',
    'Germination Energy 8mls', 'water Sensity ', 'Screens - eaml',
    '1000 corn Weight *c wgt', 'Grain Nitrogen % N2', 'Rubbish %',
    'Moisture Content'
]

steeping_features = [
    'first wet phase',
    'first dry phase',
    'second wet phase',
    'second dry phase',
    'Steeping Duration',
    'First wet steep water temp ',
    'Second wet water temp  ',
    'End of Steep Mositure  Content ',
    'Hydration Index based on 50 Grains ',
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

inputs = {}

# ----------------------------------------------
# Function to input a feature with min validation
# ----------------------------------------------

def validated_number_input(label, default=0.0):
    val = st.number_input(label, value=default)
    min_val = min_values.get(label, None)
    if min_val is not None and val < min_val:
        st.warning(
            f"⚠️ {label} is below typical operating minimum ({min_val}). "
            f"Prediction may be inaccurate."
        )
    return val

# ----------------------------------------------
# PRE-STEEP SECTION UI
# ----------------------------------------------

with st.expander("Pre-Steep Features", expanded=True):
    cols = st.columns(2)
    for i, feat in enumerate(pre_steep_features):
        if feat != 'water Sensity ':
            with cols[i % 2]:
                inputs[feat] = validated_number_input(feat, 0.0)

    # Auto-calc water sensity
    inputs['water Sensity '] = (
        inputs.get('Germination Energy ', 0)
        - inputs.get('Germination Energy 8mls', 0)
    )
    with st.columns(2)[0]:
        st.number_input(
            "water Sensity (calculated)",
            value=float(inputs['water Sensity ']),
            disabled=True
        )

# ----------------------------------------------
# STEEPING SECTION UI
# ----------------------------------------------

with st.expander("Steeping Features", expanded=False):
    cols = st.columns(2)

    # First four durations
    for i, feat in enumerate(steeping_features[:4]):
        with cols[i % 2]:
            inputs[feat] = validated_number_input(feat, 0.0)

    # Auto-calc duration
    inputs['Steeping Duration'] = (
        inputs.get('first wet phase', 0)
        + inputs.get('first dry phase', 0)
        + inputs.get('second wet phase', 0)
        + inputs.get('second dry phase', 0)
    )
    with st.columns(2)[0]:
        st.number_input(
            "Steeping Duration (calculated)",
            value=float(inputs['Steeping Duration']),
            disabled=True
        )

    # Remaining steeping features
    for feat in steeping_features[5:]:
        with cols[steeping_features.index(feat) % 2]:
            inputs[feat] = validated_number_input(feat, 0.0)

# ----------------------------------------------
# GERMINATION SECTION UI
# ----------------------------------------------

with st.expander("Germination Features", expanded=False):
    cols = st.columns(2)
    for i, feat in enumerate(germination_features):
        with cols[i % 2]:
            inputs[feat] = validated_number_input(feat, 0.0)

# ----------------------------------------------
# PREDICTION
# ----------------------------------------------

if st.button("Predict Friability"):
    try:
        df = pd.DataFrame([inputs], columns=columns)
        df = df.apply(pd.to_numeric, errors='coerce')
        df = df.fillna(df.mean())
        pred = model.predict(df)
        st.success(f"Predicted Friability: **{pred[0]:.2f}**")
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
