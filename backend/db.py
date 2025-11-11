# backend/db.py
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "health_insights.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            bmi REAL,
            blood_pressure REAL,
            cholesterol REAL,
            glucose REAL,
            smoking INTEGER,
            exercise_level INTEGER,
            risk_proba REAL,
            risk_label TEXT,
            lifestyle_text TEXT,
            lifestyle_sentiment TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()
    conn.close()


def insert_record(
    age: int,
    bmi: float,
    blood_pressure: float,
    cholesterol: float,
    glucose: float,
    smoking: int,
    exercise_level: int,
    risk_proba: float,
    risk_label: str,
    lifestyle_text: str | None,
    lifestyle_sentiment: str | None,
):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO health_records (
            age, bmi, blood_pressure, cholesterol, glucose,
            smoking, exercise_level, risk_proba, risk_label,
            lifestyle_text, lifestyle_sentiment
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            age,
            bmi,
            blood_pressure,
            cholesterol,
            glucose,
            smoking,
            exercise_level,
            risk_proba,
            risk_label,
            lifestyle_text,
            lifestyle_sentiment,
        ),
    )
    conn.commit()
    conn.close()


def get_records(limit: int = 50):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            id, age, bmi, blood_pressure, cholesterol, glucose,
            smoking, exercise_level, risk_proba, risk_label,
            lifestyle_text, lifestyle_sentiment, created_at
        FROM health_records
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
