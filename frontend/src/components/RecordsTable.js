import React from "react";

const RecordsTable = ({ records }) => {
  if (!records || records.length === 0) {
    return <p>Henüz kayıt bulunmuyor. Bir tahmin yaptıktan sonra burada gözükecek.</p>;
  }

  return (
    <div className="records-table-wrapper">
      <table className="records-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Yaş</th>
            <th>BMI</th>
            <th>Tansiyon</th>
            <th>Kolesterol</th>
            <th>Glukoz</th>
            <th>Sigara</th>
            <th>Egzersiz</th>
            <th>Risk</th>
            <th>Olasılık</th>
            <th>Sentiment</th>
            <th>Tarih</th>
          </tr>
        </thead>
        <tbody>
          {records.map((r) => (
            <tr key={r.id}>
              <td>{r.id}</td>
              <td>{r.age}</td>
              <td>{r.bmi}</td>
              <td>{r.blood_pressure}</td>
              <td>{r.cholesterol}</td>
              <td>{r.glucose}</td>
              <td>{r.smoking === 1 ? "Evet" : "Hayır"}</td>
              <td>{r.exercise_level}</td>
              <td>{r.risk_label}</td>
              <td>{(r.risk_proba * 100).toFixed(1)}%</td>
              <td>{r.lifestyle_sentiment || "-"}</td>
              <td>{r.created_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RecordsTable;
