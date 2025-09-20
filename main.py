from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI()

# ✅ Define model/scaler paths
MODEL_PATH = os.path.join("backend", "stream_model.pkl")
SCALER_PATH = os.path.join("backend", "scaler.pkl")

# ✅ Load trained model and scaler
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    raise RuntimeError(f"Error loading model or scaler: {e}")

# ✅ Input schema
class QuizInput(BaseModel):
    logical: int
    numerical: int
    verbal: int
    medical: int
    nonmedical: int
    commerce: int
    arts: int
    vocational: int

# ✅ Preprocessing (same as during training)
def preprocess_input(data: dict):
    df = pd.DataFrame([data])
    df["total_aptitude"] = df[["logical", "numerical", "verbal"]].sum(axis=1)
    df["total_interest"] = df[["medical", "nonmedical", "commerce", "arts", "vocational"]].sum(axis=1)
    df["sci_bias"] = df["medical"] - df["nonmedical"]
    df["arts_vs_com"] = df["arts"] - df["commerce"]
    return df

# ✅ Prediction endpoint
@app.post("/predict_stream")
def predict_stream(quiz: QuizInput):
    try:
        data = quiz.dict()
        df = preprocess_input(data)
        X_scaled = scaler.transform(df)
        prediction = model.predict(X_scaled)[0]
        proba = model.predict_proba(X_scaled)[0].max()
        return {
            "predicted_stream": str(prediction),
            "confidence": round(float(proba), 3)
        }
    except Exception as e:
        return {"error": str(e)}
