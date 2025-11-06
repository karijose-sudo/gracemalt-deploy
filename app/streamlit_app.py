import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# Load the trained model
# -----------------------------
model = joblib.load("models/gracemalt_model.pkl")

# -----------------------------
# Feature names (must match training)
# -----------------------------
columns = [
    # Pre-Steep
    'Grain Germinatio %', 'Germination Capacity', 'Germination Energy ', 'Germination Energy 8mls',
    'water Sensity ', 'Screens - eaml', '1000 corn Weight *c wgt', 'Grain Nitrogen % N2',
    'Rubbish %', 'Moisture Content',
    # Steeping
    'first wet phase', 'first dry phase', 'second wet phase', 'second dry phase', 'Steeping Duration',
    '1st wet steep water temp ', '2nd wet water temp  ', 'End of Steep Mositure  Content ',
    'Hydration Index based on 50 Grains ', 'End of steep Chit Count)',
    # Germination
    'MC after  48 Hours Post casting  - (GBK)', 'Chit Count  48hrs Post casting (GBK)', 'Chit count   72hrs',
    'MC after 72hrs Post casting', 'Chit Count  120hrs Post casting (Non GrwOn)-  GBK',
    'Chit Count  120hrs Post casting (1/4 to 1/2)-  GBK', 'Chit Count  120hrs Post casting (1/2 to 3/4)-  GBK',
    'Chit Count  120hrs Post casting (3/4 to Full (F) in GBK', 'Chit Count  120hrs Post casting (Full Plus F+) in GBK',
    'End of germination  Moisture '
]

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Malt Friability Predictor", layout="centered")
st.title("🌾 Malt Friability Predictor")
st.markdown("Enter process parameters below to predict **Friability**")

# Dictionary to hold user inputs
user_input = {}

# -----------------------------
# Pre-Steep Section
# -----------------------------
with st.expander("Pre-Steep Parameters", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        user_input['Grain Germinatio %'] = st.number_input('Grain Germinatio %', 0.0, 100.0, 95.0)
        user_input['Germination Capacity'] = st.number_input('Germination Capacity', 0.0, 100.0, 98.0)
        user_input['Germination Energy '] = st.number_input('Germination Energy', 0.0, 100.0, 90.0)
        user_input['Germination Energy 8mls'] = st.number_input('Germination Energy 8mls', 0.0, 100.0, 85.0)
        user_input['water Sensity '] = st.number_input('Water Sensity', 0.0, 90.0, 1.2)
    with col2:
        user_input['Screens - eaml'] = st.number_input('Screens - eaml', 0.0, 10.0, 2.0)
        user_input['1000 corn Weight *c wgt'] = st.number_input('1000 corn Weight *c wgt', 0.0, 100.0, 35.0)
        user_input['Grain Nitrogen % N2'] = st.number_input('Grain Nitrogen % N2', 0.0, 10.0, 1.8)
        user_input['Rubbish %'] = st.number_input('Rubbish %', 0.0, 20.0, 0.5)
        user_input['Moisture Content'] = st.number_input('Moisture Content', 0.0, 50.0, 12.0)

# -----------------------------
# Steeping Section
# -----------------------------
with st.expander("Steeping Parameters", expanded=False):
    col3, col4 = st.columns(2)
    with col3:
        user_input['first wet phase'] = st.number_input('First wet phase', 0.0, 20.0, 6.0)
        user_input['first dry phase'] = st.number_input('First dry phase', 0.0, 20.0, 4.0)
        user_input['second wet phase'] = st.number_input('Second wet phase', 0.0, 20.0, 5.5)
        user_input['second dry phase'] = st.number_input('Second dry phase', 0.0, 20.0, 3.5)
        user_input['Steeping Duration'] = st.number_input('Steeping Duration', 0.0, 24.0, 12.5)
    with col4:
        user_input['1st wet steep water temp '] = st.number_input('1st wet steep water temp', 0.0, 100.0, 18.0)
        user_input['2nd wet water temp  '] = st.number_input('2nd wet water temp', 0.0, 100.0, 20.0)
        user_input['End of Steep Mositure  Content '] = st.number_input('End of Steep Moisture Content', 0.0, 50.0, 42.0)
        user_input['Hydration Index based on 50 Grains '] = st.number_input('Hydration Index (50 Grains)', 0.0, 5.0, 0.8)
        user_input['End of steep Chit Count)'] = st.number_input('End of Steep Chit Count', 0.0, 50.0, 25.0)

# -----------------------------
# Germination Section
# -----------------------------
with st.expander("Germination Parameters", expanded=False):
    col5, col6 = st.columns(2)
    with col5:
        user_input['MC after  48 Hours Post casting  - (GBK)'] = st.number_input('MC after 48 Hours Post Casting', 0.0, 50.0, 15.0)
        user_input['Chit Count  48hrs Post casting (GBK)'] = st.number_input('Chit Count 48hrs', 0.0, 50.0, 10.0)
        user_input['Chit count   72hrs'] = st.number_input('Chit count 72hrs', 0.0, 50.0, 8.0)
        user_input['MC after 72hrs Post casting'] = st.number_input('MC after 72hrs Post Casting', 0.0, 50.0, 16.0)
        user_input['Chit Count  120hrs Post casting (Non GrwOn)-  GBK'] = st.number_input('Chit Count 120hrs Non GrwOn', 0.0, 50.0, 5.0)
    with col6:
        user_input['Chit Count  120hrs Post casting (1/4 to 1/2)-  GBK'] = st.number_input('Chit Count 120hrs 1/4 to 1/2', 0.0, 50.0, 7.0)
        user_input['Chit Count  120hrs Post casting (1/2 to 3/4)-  GBK'] = st.number_input('Chit Count 120hrs 1/2 to 3/4', 0.0, 50.0, 9.0)
        user_input['Chit Count  120hrs Post casting (3/4 to Full (F) in GBK'] = st.number_input('Chit Count 120hrs 3/4 to Full', 0.0, 50.0, 12.0)
        user_input['Chit Count  120hrs Post casting (Full Plus F+) in GBK'] = st.number_input('Chit Count 120hrs Full Plus F+', 0.0, 50.0, 14.0)
        user_input['End of germination  Moisture '] = st.number_input('End of Germination Moisture', 0.0, 50.0, 38.0)

# -----------------------------
# Predict Button with Error Handling
# -----------------------------
if st.button("Predict Friability"):
    try:
        input_df = pd.DataFrame([user_input], columns=columns)
        prediction = model.predict(input_df)
        st.success(f"Predicted Malt Friability: {prediction[0]:.2f}")
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")


