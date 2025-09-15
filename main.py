from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# ✅ Load trained model and scaler
model = joblib.load("backend/stream_model.pkl")
scaler = joblib.load("backend/scaler.pkl")

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

def preprocess_input(data: dict):
    """Apply same feature engineering as during training"""
    df = pd.DataFrame([data])
    df["total_aptitude"] = df[["logical", "numerical", "verbal"]].sum(axis=1)
    df["total_interest"] = df[["medical", "nonmedical", "commerce", "arts", "vocational"]].sum(axis=1)
    df["sci_bias"] = df["medical"] - df["nonmedical"]
    df["arts_vs_com"] = df["arts"] - df["commerce"]
    return df

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
