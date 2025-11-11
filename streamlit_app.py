# streamlit_app.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="AI Health Insights", layout="wide")

st.title("🧠 AI Health Insights – Sağlık Verisi Analiz ve Tahmin Platformu")
st.write(
    "Bu demo, kullanıcı sağlık verilerini kullanarak yaklaşık bir risk tahmini yapar "
    "ve yaşam tarzı metnini basit sentiment analiziyle değerlendirir."
)

st.sidebar.header("🔢 Girdi Parametreleri")

age = st.sidebar.number_input("Yaş", min_value=18, max_value=100, value=30, step=1)
bmi = st.sidebar.number_input("BMI (Vücut Kitle İndeksi)", min_value=10.0, max_value=60.0, value=25.0, step=0.1)
blood_pressure = st.sidebar.number_input("Tansiyon (Sistolik)", min_value=80.0, max_value=220.0, value=120.0, step=1.0)
cholesterol = st.sidebar.number_input("Kolesterol", min_value=100.0, max_value=400.0, value=200.0, step=1.0)
glucose = st.sidebar.number_input("Glukoz", min_value=60.0, max_value=300.0, value=100.0, step=1.0)
smoking = st.sidebar.selectbox("Sigara Kullanımı", options=[0, 1], format_func=lambda x: "Hayır" if x == 0 else "Evet")
exercise_level = st.sidebar.slider(
    "Egzersiz Düzeyi (0: yok, 3: yüksek)", min_value=0, max_value=3, value=1
)

st.sidebar.markdown("---")
lifestyle_text = st.sidebar.text_area(
    "Yaşam Tarzı Notu (Opsiyonel)",
    placeholder="Beslenme, uyku, günlük hareketliliğin hakkında kısa bir not yazabilirsin (EN/TR)...",
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Tahmin Sonucu")

    if st.button("Risk Tahmini Yap", use_container_width=True):
        payload = {
            "age": age,
            "bmi": bmi,
            "blood_pressure": blood_pressure,
            "cholesterol": cholesterol,
            "glucose": glucose,
            "smoking": smoking,
            "exercise_level": exercise_level,
            "lifestyle_text": lifestyle_text,
        }

        try:
            resp = requests.post(f"{API_BASE_URL}/api/health/predict", json=payload, timeout=20)
            if resp.status_code == 200:
                result = resp.json()
                risk_proba = result["risk_proba"]
                risk_label = result["risk_label"]

                st.metric(
                    label="Tahmini Risk Seviyesi",
                    value=risk_label,
                    delta=f"%{risk_proba * 100:.1f} olasılık",
                )

                if result.get("lifestyle_sentiment"):
                    st.write(f"**Yaşam Tarzı Sentiment (demo):** {result['lifestyle_sentiment']}")

                st.success("Kayıt veritabanına kaydedildi.")
            else:
                st.error(f"API hatası: {resp.status_code} - {resp.text}")
        except Exception as e:
            st.error(f"Sunucuya bağlanırken hata oluştu: {e}")

with col2:
    st.subheader("📊 Geçmiş Kayıtlar ve Görselleştirme")

    try:
        resp_records = requests.get(f"{API_BASE_URL}/api/health/records?limit=100", timeout=20)
        if resp_records.status_code == 200:
            records = resp_records.json()
            if records:
                df = pd.DataFrame(records)
                st.dataframe(df)

                # Basit bir grafik: yaş vs risk_proba
                fig = px.scatter(
                    df,
                    x="age",
                    y="risk_proba",
                    color="risk_label",
                    title="Yaş vs. Risk Olasılığı",
                    size_max=10,
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Henüz kayıt bulunmuyor. Tahmin yaptıktan sonra kayıtlar burada görünecek.")
        else:
            st.error(f"Kayıtları çekerken API hatası: {resp_records.status_code}")
    except Exception as e:
        st.error(f"Kayıtları çekerken bağlantı hatası: {e}")
