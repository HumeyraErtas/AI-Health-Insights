# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import numpy as np
import joblib

from transformers import pipeline

from db import init_db, insert_record, get_records

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"

model = joblib.load(MODELS_DIR / "health_risk_model.pkl")
scaler = joblib.load(MODELS_DIR / "scaler.pkl")

# Sentiment modeli lazy loading (ağ bağlantı hatası yaşanırsa kullanılmayacak)
sentiment_pipe = None

def get_sentiment_pipe():
    global sentiment_pipe
    if sentiment_pipe is None:
        try:
            sentiment_pipe = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
        except Exception as e:
            print(f"Uyarı: Sentiment modeli yüklenemedi: {e}")
            print("Sentiment analizi kapatılmıştır.")
            return None
    return sentiment_pipe

app = Flask(__name__)
CORS(app)


def map_risk_label(proba: float) -> str:
    if proba < 0.33:
        return "Low"
    elif proba < 0.66:
        return "Medium"
    return "High"


@app.route("/api/health/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)

    try:
        age = int(data["age"])
        bmi = float(data["bmi"])
        blood_pressure = float(data["blood_pressure"])
        cholesterol = float(data["cholesterol"])
        glucose = float(data["glucose"])
        smoking = int(data["smoking"])          # 0 / 1
        exercise_level = int(data["exercise_level"])  # 0–3
    except (KeyError, ValueError, TypeError) as e:
        return jsonify({"error": f"Geçersiz veya eksik parametre: {e}"}), 400

    features = np.array([[age, bmi, blood_pressure, cholesterol, glucose, smoking, exercise_level]])
    features_scaled = scaler.transform(features)
    proba = float(model.predict_proba(features_scaled)[0][1])
    risk_label = map_risk_label(proba)

    lifestyle_text = data.get("lifestyle_text") or ""
    lifestyle_sentiment = None

    if lifestyle_text.strip():
        try:
            pipe = get_sentiment_pipe()
            if pipe is not None:
                result = pipe(lifestyle_text[:512])[0]
                lifestyle_sentiment = result["label"]
            else:
                lifestyle_sentiment = "UNAVAILABLE"
        except Exception as e:
            print(f"Sentiment analizi hatası: {e}")
            lifestyle_sentiment = "ERROR"

    # DB'ye kaydet
    insert_record(
        age=age,
        bmi=bmi,
        blood_pressure=blood_pressure,
        cholesterol=cholesterol,
        glucose=glucose,
        smoking=smoking,
        exercise_level=exercise_level,
        risk_proba=proba,
        risk_label=risk_label,
        lifestyle_text=lifestyle_text,
        lifestyle_sentiment=lifestyle_sentiment,
    )

    return jsonify(
        {
            "risk_proba": proba,
            "risk_label": risk_label,
            "features": {
                "age": age,
                "bmi": bmi,
                "blood_pressure": blood_pressure,
                "cholesterol": cholesterol,
                "glucose": glucose,
                "smoking": smoking,
                "exercise_level": exercise_level,
            },
            "lifestyle_text": lifestyle_text,
            "lifestyle_sentiment": lifestyle_sentiment,
        }
    )


@app.route("/api/health/records", methods=["GET"])
def list_records():
    try:
        limit = int(request.args.get("limit", 50))
    except ValueError:
        limit = 50

    records = get_records(limit=limit)
    return jsonify(records)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
