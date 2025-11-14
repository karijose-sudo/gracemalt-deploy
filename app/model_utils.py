import joblib
import pandas as pd
import os

MODEL_PATH = os.path.join("models/ensemble_gracemalt.pkl")
COLUMNS_PATH = os.path.join("models", "train_columns.pkl")

gracemalt_model = joblib.load(MODEL_PATH)
train_columns = joblib.load(COLUMNS_PATH)

def align_features(input_data: pd.DataFrame) -> pd.DataFrame:
    """Align new data with training columns."""
    return input_data.reindex(columns=train_columns, fill_value=0)

def predict_quality(data: pd.DataFrame):
    """Run predictions."""
    aligned = align_features(data)
    preds = gracemalt_model.predict(aligned)
    return preds.tolist()

