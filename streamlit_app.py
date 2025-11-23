import streamlit as st
import numpy as np
import joblib

# -------------------------
# Load Model
# -------------------------
model = joblib.load("friability_model.pkl")

# -------------------------
# Minimum Allowed Values
# -------------------------
min_values = {
    "Grain Germinatio %": 98.0,
    "Germination Capacity": 96.0,
    "Germination Energy": 44.0,
    "Germination Energy 8mls": 5.0,
    "water Sensity": 1.0,
    "Screens - eaml": 0.1,
    "1000 corn Weight *c wgt": 31.0,
    "Grain Nitrogen % N2": 1.25,
    "Rubbish %": 0.1,
    "Moisture Content": 10.7,
    "First wet steep water temp": 10.0,
    "Second wet water temp": 9.0,
    "End of Steep Mositure Content": 38.0,
    "Hydration Index based on 50 Grains": 70.0,
    "End of steep Chit Count": 40.0,
    "MC after 48 Hours Post casting - (GBK)": 39.0,
    "Chit Count 48hrs Post casting (GBK)": 82.0,
    "Chit count 72hrs": 91.0,
    "MC after 72hrs Post casting": 35.9,
    "Chit Count 120hrs Post casting (Non GrwOn)- GBK": 1.0,
    "Chit Count 120hrs Post casting (1/4 to 1/2)- GBK": 2.0,
    "Chit Count 120hrs Post casting (1/2 to 3/4)- GBK": 6.0,
    "Chit Count 120hrs Post casting (3/4 to Full (F) in GBK": 21.0,
    "Chit Count 120hrs Post casting (Full Plus F+) in GBK": 1.0,
    "End of germination Moisture": 34.2
}

# Feature order MUST match model training
feature_order = list(min_values.keys())

st.title("Friability Prediction with Minimum Input Rules")

st.write("Enter malting process measurements below. Values below the valid minimum will trigger a warning.")

input_values = {}

# -------------------------
# Input Form
# -------------------------
for feature in feature_order:
    default = min_values[feature]
    value = st.number_input(
        feature,
        min_value=0.0,
        value=float(default),
        step=0.1
    )
    input_values[feature] = value

# -------------------------
# Validate Minimums
# -------------------------
below_min = [
    f"{feat} (entered {input_values[feat]}, minimum {min_values[feat]})"
    for feat in feature_order
    if input_values[feat] < min_values[feat]
]

if below_min:
    st.error(
        "⚠️ The following inputs are below the minimum values seen in training, "
        "meaning predictions may be unreliable:\n\n"
        + "\n".join(f"- {item}" for item in below_min)
    )

# -------------------------
# Create Prediction Vector
# -------------------------
if st.button("Predict Friability"):

    row = np.array([[input_values[f] for f in feature_order]])

    prediction = model.predict(row)[0]

    st.subheader("Predicted Friability")
    st.success(f"{prediction:.2f}")

    if below_min:
        st.warning(
            "⚠️ Because one or more values were below training minimums, "
            "treat this prediction with caution."
        )
