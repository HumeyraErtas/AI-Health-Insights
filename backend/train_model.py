# backend/train_model.py
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
import os


BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)


def generate_synthetic_data(n_samples: int = 2000, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    age = rng.integers(18, 80, size=n_samples)
    bmi = rng.normal(27, 5, size=n_samples).clip(16, 45)
    blood_pressure = rng.normal(120, 15, size=n_samples).clip(80, 200)
    cholesterol = rng.normal(200, 30, size=n_samples).clip(120, 320)
    glucose = rng.normal(100, 20, size=n_samples).clip(60, 220)
    smoking = rng.integers(0, 2, size=n_samples)  # 0/1
    exercise_level = rng.integers(0, 4, size=n_samples)  # 0: hiç, 3: yüksek

    # Basit risk fonksiyonu (gerçek veri değil, demo)
    risk_score = (
        0.03 * (age - 40) +
        0.07 * (bmi - 25) +
        0.04 * (blood_pressure - 120) +
        0.03 * (cholesterol - 200) +
        0.03 * (glucose - 100) +
        0.8 * smoking -
        0.4 * exercise_level
    )

    # Sigmoid ile 0–1 arası olasılık
    prob = 1 / (1 + np.exp(-risk_score / 10))
    # 0/1 etiket: >0.5 riskli
    label = (prob > 0.5).astype(int)

    df = pd.DataFrame({
        "age": age,
        "bmi": bmi,
        "blood_pressure": blood_pressure,
        "cholesterol": cholesterol,
        "glucose": glucose,
        "smoking": smoking,
        "exercise_level": exercise_level,
        "risk_label": label
    })
    return df


def train_and_save_model():
    df = generate_synthetic_data()

    X = df[["age", "bmi", "blood_pressure", "cholesterol", "glucose", "smoking", "exercise_level"]]
    y = df["risk_label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(max_iter=500)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    print("Classification report:\n")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, MODELS_DIR / "health_risk_model.pkl")
    joblib.dump(scaler, MODELS_DIR / "scaler.pkl")
    print(f"Model ve scaler {MODELS_DIR} altına kaydedildi.")


if __name__ == "__main__":
    train_and_save_model()
