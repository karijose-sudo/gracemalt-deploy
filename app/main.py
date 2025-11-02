from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from app.model_utils import predict_quality
import os
import uvicorn

app = FastAPI(title="GraceMalt Quality Predictor")

# --- CORS middleware to allow Swagger UI to fetch openapi.json ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # can restrict to your Render URL if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to the GraceMalt Prediction API"}

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    preds = predict_quality(df)
    return {"prediction": preds}  # preds is already a list


# --- Run the app on the port provided by Render ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)



