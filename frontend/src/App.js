import React, { useEffect, useState } from "react";
import HealthForm from "./components/HealthForm";
import RecordsTable from "./components/RecordsTable";

const API_BASE_URL = "http://127.0.0.1:5000";

function App() {
  const [records, setRecords] = useState([]);
  const [lastResult, setLastResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const fetchRecords = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/health/records?limit=100`);
      if (!res.ok) {
        throw new Error("Kayıtlar çekilemedi");
      }
      const data = await res.json();
      setRecords(data);
    } catch (err) {
      console.error(err);
      setErrorMsg("Geçmiş kayıtlar alınırken hata oluştu.");
    }
  };

  useEffect(() => {
    fetchRecords();
  }, []);

  const handlePredict = async (formData) => {
    setLoading(true);
    setErrorMsg("");
    try {
      const res = await fetch(`${API_BASE_URL}/api/health/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "Tahmin isteği başarısız");
      }

      const data = await res.json();
      setLastResult(data);
      await fetchRecords(); // yeni kaydı listeye eklemek için tekrar çek
    } catch (err) {
      console.error(err);
      setErrorMsg("Tahmin yapılırken hata oluştu. Backend çalışıyor mu?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🧠 AI Health Insights</h1>
        <p>
          Yapay zekâ destekli sağlık verisi analizi ve risk tahmini demo
          uygulaması.
        </p>
      </header>

      <main className="app-main">
        <section className="app-section">
          <h2>🔢 Girdi Formu</h2>
          <HealthForm onPredict={handlePredict} loading={loading} />
          {errorMsg && <p className="error-msg">{errorMsg}</p>}

          {lastResult && (
            <div className="result-card">
              <h3>📌 Tahmin Sonucu</h3>
              <p>
                <strong>Risk Seviyesi:</strong> {lastResult.risk_label}
              </p>
              <p>
                <strong>Olasılık:</strong>{" "}
                {(lastResult.risk_proba * 100).toFixed(1)}%
              </p>
              {lastResult.lifestyle_sentiment && (
                <p>
                  <strong>Yaşam Tarzı Sentiment (demo):</strong>{" "}
                  {lastResult.lifestyle_sentiment}
                </p>
              )}
            </div>
          )}
        </section>

        <section className="app-section">
          <h2>📊 Geçmiş Kayıtlar</h2>
          <RecordsTable records={records} />
        </section>
      </main>

      <footer className="app-footer">
        <small>AI Health Insights · Demo Proje · Python + Flask + React</small>
      </footer>
    </div>
  );
}

export default App;
