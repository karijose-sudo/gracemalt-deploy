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

st.write("Enter your malt batch parameters below to predict **friability**.")

# -----------------------------
# Manual single batch input
# -----------------------------
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

inputs = {}

# -----------------------------
# Pre-Steep Section
# -----------------------------
with st.expander("Pre-Steep Features", expanded=True):
    cols = st.columns(2)
    for i, feat in enumerate(pre_steep_features):
        with cols[i % 2]:
            # leave 'water Sensity' for later (auto-calculated)
            if feat != 'water Sensity ':
                inputs[feat] = st.number_input(f"{feat}", value=0.0)

# -----------------------------
# Steeping Section
# -----------------------------
with st.expander("Steeping Features", expanded=False):
    cols = st.columns(2)
    # Input first four phases
    for i, feat in enumerate(steeping_features[:4]):
        with cols[i % 2]:
            inputs[feat] = st.number_input(f"{feat}", value=0.0)

    # Compute Steeping Duration automatically
    inputs['Steeping Duration'] = (
        inputs['first wet phase']
        + inputs['first dry phase']
        + inputs['second wet phase']
        + inputs['second dry phase']
    )

    with st.columns(2)[0]:
        st.number_input(
            "Steeping Duration (calculated)",
            value=float(inputs['Steeping Duration']),
            disabled=True
        )

    # Continue with the rest
    for feat in steeping_features[5:]:
        with cols[steeping_features.index(feat) % 2]:
            inputs[feat] = st.number_input(f"{feat}", value=0.0)

# -----------------------------
# Germination Section
# -----------------------------
with st.expander("Germination Features", expanded=False):
    cols = st.columns(2)
    for i, feat in enumerate(germination_features):
        with cols[i % 2]:
            inputs[feat] = st.number_input(f"{feat}", value=0.0)

# -----------------------------
# Auto-calculate Water Sensity
# -----------------------------
inputs['water Sensity '] = (
    inputs['Germination Energy '] - inputs['Germination Energy 8mls']
)

with st.columns(2)[0]:
    st.number_input(
        "Water Sensity (calculated)",
        value=float(inputs['water Sensity ']),
        disabled=True
    )

# -----------------------------
# Prediction
# -----------------------------
if st.button("Predict Friability"):
    try:
        # add missing calculated fields into dataframe
        input_df = pd.DataFrame([inputs], columns=columns)
        prediction = model.predict(input_df)
        st.success(f"Predicted Malt Friability: **{prediction[0]:.2f}**")
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
