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
# Feature Lists
# -----------------------------
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

# -----------------------------
# Pre-Steep Section
# -----------------------------
with st.expander("Pre-Steep Features", expanded=True):
    cols = st.columns(2)
    for i, feat in enumerate(pre_steep_features):
        if feat != 'water Sensity ':
            with cols[i % 2]:
                inputs[feat] = st.number_input(f"{feat}", value=0.0)

    # --- FIX #2: Correct calculated feature stored under exact model name ---
    inputs['water Sensity '] = (
        inputs.get('Germination Energy ', 0)
        - inputs.get('Germination Energy 8mls', 0)
    )

    # Display to the user but DO NOT create new incorrect column names
    with st.columns(2)[0]:
        st.number_input(
            "water Sensity (calculated)",
            value=float(inputs['water Sensity ']),
            disabled=True
        )

# -----------------------------
# Steeping Section
# -----------------------------
with st.expander("Steeping Features", expanded=False):
    cols = st.columns(2)

    # First four phases
    for i, feat in enumerate(steeping_features[:4]):
        with cols[i % 2]:
            inputs[feat] = st.number_input(f"{feat}", value=0.0)

    # --- FIX #2: Calculate under exact feature name expected by model ---
    inputs['Steeping Duration'] = (
        inputs.get('first wet phase', 0)
        + inputs.get('first dry phase', 0)
        + inputs.get('second wet phase', 0)
        + inputs.get('second dry phase', 0)
    )

    # Display to user only
    with st.columns(2)[0]:
        st.number_input(
            "Steeping Duration (calculated)",
            value=float(inputs['Steeping Duration']),
            disabled=True
        )

    # Remaining steeping inputs
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
# Prediction
# -----------------------------
if st.button("Predict Friability"):
    try:
        # Build DataFrame
        input_df = pd.DataFrame([inputs], columns=columns)

        # Clean numeric types
        input_df = input_df.apply(pd.to_numeric, errors='coerce')
        input_df = input_df.fillna(input_df.mean())  # safety impute

        # Predict
        prediction = model.predict(input_df)
        st.success(f"Predicted Malt Friability: **{prediction[0]:.2f}**")

    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")

