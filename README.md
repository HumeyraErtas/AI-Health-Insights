# AI Health Insights

Bu depo, demo amaçlı bir sağlık riski tahmin uygulamasıdır. Sentetik verilerle eğitilmiş bir makine öğrenimi modeli ile kullanıcı sağlık parametrelerine göre risk olasılığı tahmin edilir. Ayrıca bir Streamlit arayüzü ve bir REST API (Flask) içerir.

Dil: Türkçe

## Özet

- Backend: Flask tabanlı API (backend/app.py) — model tahmini, kayıt saklama, basit sentiment analizi (opsiyonel).
- Model eğitimi: `backend/train_model.py` — sentetik veri üretir, StandardScaler ile ölçekleme ve LogisticRegression ile model eğitir; `backend/models/` dizinine `health_risk_model.pkl` ve `scaler.pkl` kaydeder.
- Frontend: (opsiyonel) React tarzı bir frontend klasörü mevcut olabilir (`frontend/`) — yerel olarak başlatılabilir.
- Streamlit UI: `streamlit_app.py` — API ile konuşan basit bir gösterge paneli.
- Veri tabanı: SQLite (basit, dosya tabanlı) — `backend/db.py` kullanılır.

## Depo yapısı (özet)

```
AI-Health-Insights/
├─ backend/
│  ├─ app.py               # Flask API
│  ├─ db.py                # Basit SQLite yardımcıları
│  ├─ train_model.py       # Modeli eğitir ve kaydeder
│  ├─ models/              # Eğitilmiş model ve scaler (.pkl)
│  └─ requirements.txt     # Backend bağımlılıkları
├─ frontend/               # (varsa) React uygulaması
├─ streamlit_app.py        # Streamlit arayüzü
└─ README.md
```

## Gereksinimler

Backend için (backend/requirements.txt):

- flask
- flask-cors
- joblib
- scikit-learn
- pandas
- numpy
- transformers
- torch
- streamlit
- plotly
- requests

Not: `transformers` model indirme için internet bağlantısı gerektirir. Uygulamada sentiment pipeline lazy-load şeklinde kullanılır; eğer internet yoksa sentiment analizi devre dışı bırakılır ve API çalışmaya devam eder.

## Hızlı kurulum (Windows, PowerShell örneği)

Aşağıdaki adımlar projeyi yerelde çalıştırmak için yeterlidir.

1) Depoyu klonlayın veya zaten bulunuyorsa dizine gidin:

```powershell
cd "C:\Users\humeyra\OneDrive\Belgeler\GitHub\AI-Health-Insights"
```

2) (İsteğe bağlı) Conda/venv oluşturun ve etkinleştirin

Conda örneği:

```powershell
conda create -n ai-health python=3.10 -y
conda activate ai-health
```

Venv örneği:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3) Backend bağımlılıklarını yükleyin

```powershell
cd backend
pip install -r requirements.txt
```

(Alternatif: `pip install flask flask-cors joblib scikit-learn pandas numpy transformers torch streamlit plotly requests`)

4) Modeli eğit (ilk defa çalıştırırken veya model dosyası eksikse)

```powershell
python train_model.py
```

Bu komut `backend/models/` dizinine `health_risk_model.pkl` ve `scaler.pkl` dosyalarını koyar.

5) Backend API'yi başlat

```powershell
python app.py
```

- Sunucu varsayılan olarak `http://127.0.0.1:5000` üzerinde çalışır.
- `GET /` endpoint'i kısa bir hoşgörü mesajı ve mevcut endpoint'leri döndürür.

6) Streamlit arayüzünü çalıştır (isteğe bağlı)

Projodaki ana dizinde (depo kökünde):

```powershell
streamlit run streamlit_app.py
```

Streamlit arayüzü `http://localhost:8501` üzerinde açılır ve backend API ile konuşur. API localhost:5000 üzerinde çalışıyor olmalıdır.

7) Frontend (varsa)

Eğer projede bir `frontend/` klasörü varsa, büyük ihtimalle React tabanlıdır. Aşağıdaki genel adımlar uygulanır:

```powershell
cd frontend
npm install
npm start
```

(Not: `frontend/package.json` yoksa veya proje farklıysa frontend yönergelerini ona göre uyarlayın.)

## API Kullanımı

1) Health predict

- Endpoint: `POST /api/health/predict`
- JSON gövdesi (örnek):

```json
{
  "age": 30,
  "bmi": 25.0,
  "blood_pressure": 120.0,
  "cholesterol": 200.0,
  "glucose": 100.0,
  "smoking": 0,
  "exercise_level": 1,
  "lifestyle_text": "I walk 30 minutes daily and eat vegetables."  
}
```

- curl (bash) örnek:

```bash
curl -X POST http://127.0.0.1:5000/api/health/predict \
  -H "Content-Type: application/json" \
  -d '{"age":30,"bmi":25.0,"blood_pressure":120.0,"cholesterol":200.0,"glucose":100.0,"smoking":0,"exercise_level":1,"lifestyle_text":"I walk daily"}'
```

- PowerShell (Invoke-RestMethod) örnek:

```powershell
$body = @{ age=30; bmi=25.0; blood_pressure=120.0; cholesterol=200.0; glucose=100.0; smoking=0; exercise_level=1; lifestyle_text="I walk daily" } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/health/predict -Method Post -Body $body -ContentType 'application/json'
```

- Dönen örnek cevap:

```json
{
  "risk_proba": 0.12,
  "risk_label": "Low",
  "features": { ... },
  "lifestyle_text": "...",
  "lifestyle_sentiment": "UNAVAILABLE"  
}
```

2) Kayıtları listele

- Endpoint: `GET /api/health/records?limit=50`
- Örnek:

```bash
curl http://127.0.0.1:5000/api/health/records?limit=10
```

## Notlar ve Sık Karşılaşılan Sorunlar

- Hugging Face / Transformers model indirme hatası:
  - Eğer makine internete çıkamıyorsa veya Hugging Face'e erişilemiyorsa, `transformers` paketinin model dosyalarını indirmeye çalışması sırasında hata ile karşılaşabilirsiniz. `app.py` içinde sentiment pipeline lazy-load olarak uygulanmıştır; indirme başarısız olursa uygulama çalışmaya devam eder ve sentiment sonucu `UNAVAILABLE` veya `ERROR` dönebilir.
  - Offline kullanım: Önceden gerekli model dosyalarını indip yerel cache'e koyabilir veya `transformers` için offline mod yönergelerini takip edebilirsiniz: https://huggingface.co/docs/transformers/installation#offline-mode

- 404 hatası root (`/`) çağrıldığında:
  - `app.py` içinde artık `/` endpoint'i bulunduğu için `GET /` çağrıldığında API açıklaması dönecektir. Eğer hala 404 alıyorsanız, doğru sunucu adresinde çalışıp çalışmadığını doğrulayın.

- Port çakışmaları:
  - Eğer 5000 portu başka bir süreç tarafından kullanılıyorsa Flask farklı portta başlatılabilir veya başlatılamaz. Başlatırken farklı port belirtmek için `app.run(port=5001)` ya da ortam değişkenleri kullanın.

- Model dosyaları eksik hatası:
  - Eğer `backend/models/health_risk_model.pkl` bulunmuyorsa `python train_model.py` çalıştırın.

## Güvenlik ve Performans

- Bu proje demo amaçlıdır. Üretim dağıtımı için:
  - Flask geliştirme sunucusu yerine bir WSGI sunucusu (gunicorn, uvicorn, nginx + uwsgi gibi) kullanın.
  - Girdi doğrulama/sınırlandırma, rate-limiting, TLS/HTTPS, kimlik doğrulama gibi önlemler ekleyin.
  - Modelin ve bağımlılıkların versiyonlarını sabitleyin.

## Lisans

Bu depo `LICENSE` dosyası içeriyorsa ona göre lisanslanmıştır. (Repo kökünde `LICENSE` dosyasını kontrol edin.)

## Yardım / Daha Fazlası

Sorularınız varsa veya README'de görmek istediğiniz ek bilgiler varsa bana söyleyin; örnek istekler, docker desteği veya CI entegrasyonu gibi ek bölümler ekleyebilirim.
