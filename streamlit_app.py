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
Upload a file to predict **multiple batches**, or fill in values manually to predict a **single batch**.
""")

# -----------------------------
# File upload option
# -----------------------------
uploaded_file = st.file_uploader("Upload CSV or Excel file for batch prediction", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.write("✅ File uploaded successfully.")
        st.write("Preview of uploaded data:")
        st.dataframe(df.head())

        # Ensure correct column alignment
        missing_cols = [c for c in columns if c not in df.columns]
        extra_cols = [c for c in df.columns if c not in columns]

        if missing_cols:
            st.warning(f"The following required columns are missing: {missing_cols}")
        else:
            df = df[columns]  # keep only correct order
            preds = model.predict(df)
            df["Predicted Friability"] = preds

            st.success("✅ Predictions complete!")
            st.dataframe(df[["Predicted Friability"]])

            # Download results
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download Predictions as CSV", csv, "friability_predictions.csv", "text/csv")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")

else:
    # -----------------------------
    # Manual single batch input
    # -----------------------------
    st.subheader("Or enter a single batch manually")

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

    with st.expander("Pre-Steep Features", expanded=True):
        for feat in pre_steep_features:
            inputs[feat] = st.number_input(f"{feat}", value=0.0)

    with st.expander("Steeping Features", expanded=False):
        for feat in steeping_features:
            inputs[feat] = st.number_input(f"{feat}", value=0.0)

    with st.expander("Germination Features", expanded=False):
        for feat in germination_features:
            inputs[feat] = st.number_input(f"{feat}", value=0.0)

    if st.button("Predict Friability"):
        try:
            input_df = pd.DataFrame([inputs], columns=columns)
            prediction = model.predict(input_df)
            st.success(f"Predicted Malt Friability: **{prediction[0]:.2f}**")
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
