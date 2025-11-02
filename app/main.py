from fastapi import FastAPI
import pandas as pd
from app.model_utils import predict_quality

app = FastAPI(title="GraceMalt Quality Predictor")

@app.get("/")
def home():
    return {"message": "Welcome to the GraceMalt Prediction API"}

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    preds = predict_quality(df)
    return {"prediction": preds}
