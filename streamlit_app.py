import streamlit as st
import pandas as pd
import joblib
import time

# -----------------------------
# Load the trained model
# -----------------------------
model = joblib.load("models/ensemble_gracemalt.pkl")

# -----------------------------
# Feature names (match training)
# -----------------------------
columns = [
    'Grain Germinatio %', 'Germination Capacity', 'Germination Energy ',
    'Germination Energy 8mls', 'water Sensity ', 'Screens - eaml',
    '1000 corn Weight *c wgt', 'Grain Nitrogen % N2', 'Rubbish %',
    'Moisture Content', 'first wet phase', 'first dry phase',
    'second wet phase', 'second dry phase', 'Steeping Duration',
    '1st wet steep water temp ', '2nd wet water temp  ',
    'End of Steep Mositure  Content ', 'Hydration Index based on 50 Grains ',
    'End of steep Chit Count)',
    'ΔMC_48_72', 'ΔMC_72_120', 'Uniformity_MC',
    'ΔChit_48_72', 'ΔChit_72_120', 'Uniformity_Chit',
    'Chit_CV', 'Efficiency_48_72', 'Efficiency_72_120'
]

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Malt Friability Predictor", layout="centered")
st.title("🌾 Malt Friability Predictor")
st.markdown("Enter process parameters below to predict **Friability**")

# Collect user inputs
user_input = {}

# --- Pre-Steep ---
with st.expander("Pre-Steep Parameters", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        user_input['Grain Germinatio %'] = st.number_input('Grain Germinatio %', 0.0, 100.0, 98.0)
        user_input['Germination Capacity'] = st.number_input('Germination Capacity', 0.0, 100.0, 99.0)
        user_input['Germination Energy '] = st.number_input('Germination Energy', 0.0, 100.0, 96.0)
        user_input['Germination Energy 8mls'] = st.number_input('Germination Energy 8mls', 0.0, 100.0, 92.0)
        # Auto-calculate water sensitivity
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
        # Auto-calculate total steeping duration
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

# --- Germination Inputs ---
with st.expander("Germination Measurements", expanded=False):
    col5, col6 = st.columns(2)
    with col5:
        mc_48 = st.number_input('MC 48 hrs (%)', 0.0, 100.0, 43.0)
        mc_72 = st.number_input('MC 72 hrs (%)', 0.0, 100.0, 41.8)
        mc_120 = st.number_input('MC 120 hrs (%)', 0.0, 100.0, 37.8)
    with col6:
        chit_48 = st.number_input('Chit Count 48 hrs (%)', 0.0, 100.0, 95.0)
        chit_72 = st.number_input('Chit Count 72 hrs (%)', 0.0, 100.0, 97.0)
        chit_120 = st.number_input('Chit Count 120 hrs (%)', 0.0, 100.0, 98.0)

# --- Auto-calculate derived germination dynamics ---
user_input['ΔMC_48_72'] = mc_72 - mc_48
user_input['ΔMC_72_120'] = mc_120 - mc_72
user_input['ΔChit_48_72'] = chit_72 - chit_48
user_input['ΔChit_72_120'] = chit_120 - chit_72

mc_list = [mc_48, mc_72, mc_120]
chit_list = [chit_48, chit_72, chit_120]

user_input['Uniformity_MC'] = (pd.Series(mc_list).std() / pd.Series(mc_list).mean()) * 100
user_input['Uniformity_Chit'] = (pd.Series(chit_list).std() / pd.Series(chit_list).mean()) * 100
user_input['Chit_CV'] = (pd.Series(chit_list).std() / pd.Series(chit_list).mean()) * 100
user_input['Efficiency_48_72'] = user_input['ΔChit_48_72'] / user_input['ΔMC_48_72'] if user_input['ΔMC_48_72'] != 0 else 0
user_input['Efficiency_72_120'] = user_input['ΔChit_72_120'] / user_input['ΔMC_72_120'] if user_input['ΔMC_72_120'] != 0 else 0

# Display calculated germination dynamics
st.subheader("Calculated Derived Germination Dynamics")
st.write({
    'ΔMC 48–72 (%)': user_input['ΔMC_48_72'],
    'ΔMC 72–120 (%)': user_input['ΔMC_72_120'],
    'ΔChit 48–72 (%)': user_input['ΔChit_48_72'],
    'ΔChit 72–120 (%)': user_input['ΔChit_72_120'],
    'Uniformity (Moisture)': user_input['Uniformity_MC'],
    'Uniformity (Chit)': user_input['Uniformity_Chit'],
    'Chit CV (%)': user_input['Chit_CV'],
    'Efficiency 48–72': user_input['Efficiency_48_72'],
    'Efficiency 72–120': user_input['Efficiency_72_120']
})

# -----------------------------
# Predict Button
# -----------------------------
if st.button("Predict Friability"):
    try:
        input_df = pd.DataFrame([user_input], columns=columns)
        prediction = model.predict(input_df)
        st.success(f"Predicted Malt Friability: **{prediction[0]:.2f}**")
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
