import React, { useState } from "react";

const HealthForm = ({ onPredict, loading }) => {
  const [formState, setFormState] = useState({
    age: 30,
    bmi: 25,
    blood_pressure: 120,
    cholesterol: 200,
    glucose: 100,
    smoking: 0,
    exercise_level: 1,
    lifestyle_text: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormState((prev) => ({
      ...prev,
      [name]:
        name === "age" ||
        name === "smoking" ||
        name === "exercise_level" ||
        name === "blood_pressure" ||
        name === "cholesterol" ||
        name === "glucose"
          ? Number(value)
          : name === "bmi"
          ? Number(value)
          : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onPredict(formState);
  };

  return (
    <form className="health-form" onSubmit={handleSubmit}>
      <div className="form-row">
        <label>Yaş</label>
        <input
          type="number"
          name="age"
          min="18"
          max="100"
          value={formState.age}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-row">
        <label>BMI (Vücut Kitle İndeksi)</label>
        <input
          type="number"
          step="0.1"
          name="bmi"
          min="10"
          max="60"
          value={formState.bmi}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-row">
        <label>Tansiyon (Sistolik)</label>
        <input
          type="number"
          name="blood_pressure"
          min="80"
          max="220"
          value={formState.blood_pressure}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-row">
        <label>Kolesterol</label>
        <input
          type="number"
          name="cholesterol"
          min="100"
          max="400"
          value={formState.cholesterol}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-row">
        <label>Glukoz</label>
        <input
          type="number"
          name="glucose"
          min="60"
          max="300"
          value={formState.glucose}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-row">
        <label>Sigara Kullanımı</label>
        <select
          name="smoking"
          value={formState.smoking}
          onChange={handleChange}
        >
          <option value={0}>Hayır</option>
          <option value={1}>Evet</option>
        </select>
      </div>

      <div className="form-row">
        <label>Egzersiz Düzeyi (0–3)</label>
        <select
          name="exercise_level"
          value={formState.exercise_level}
          onChange={handleChange}
        >
          <option value={0}>0 - Hiç</option>
          <option value={1}>1 - Düşük</option>
          <option value={2}>2 - Orta</option>
          <option value={3}>3 - Yüksek</option>
        </select>
      </div>

      <div className="form-row">
        <label>Yaşam Tarzı Notu (Opsiyonel)</label>
        <textarea
          name="lifestyle_text"
          rows={3}
          placeholder="Beslenme, uyku, hareketlilik hakkında kısa not (İngilizce yazarsan sentiment analizi daha anlamlı olur)..."
          value={formState.lifestyle_text}
          onChange={handleChange}
        />
      </div>

      <button className="btn-primary" type="submit" disabled={loading}>
        {loading ? "Hesaplanıyor..." : "Risk Tahmini Yap"}
      </button>
    </form>
  );
};

export default HealthForm;
