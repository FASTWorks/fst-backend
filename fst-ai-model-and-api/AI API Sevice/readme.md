# 🧾 Receipt OCR API

Aplikasi OCR struk belanja berbasis AI yang dapat mendeteksi, mengekstrak, dan menganalisis informasi dari gambar struk belanja menggunakan model deteksi, EasyOCR, dan LLM (Llama via HuggingFace).

---

## 📁 Struktur File

```
├── main.py                      # FastAPI endpoint untuk tim backend
├── ocr_pipeline.py              # Pipeline OCR + LLM untuk Streamlit
├── app_streamlit.py             # UI Streamlit (frontend)
├── schemas.py                   # Pydantic schemas (Item, OCRResponse)
├── best_detection_model.keras   # Model deteksi lokasi struk
└── requirements.txt             # Dependencies
```

---

## ⚙️ Cara Install

```bash
# Clone repo
git clone <url-repo>
cd <nama-folder>

# Buat virtual environment
python -m venv venv

# Aktivasi venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Cara Menjalankan

### FastAPI (Backend)
```bash
uvicorn main:app --host 0.0.0.0 --port 8001
```
Akses dokumentasi API di: `http://localhost:8001/docs`

### Streamlit (Frontend)
```bash
streamlit run app_streamlit.py
```
Akses UI di: `http://localhost:8501`

---

## 📡 Endpoints

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/` | Info API |
| GET | `/health` | Cek status server & model |
| POST | `/predict` | Upload gambar struk → return JSON |

### Contoh Response `/predict`

```json
{
  "store_name": "Indomaret",
  "date": "2024-01-15",
  "total_amount": 75000.0,
  "items": [
    {
      "name": "Indomie Goreng",
      "price": 3500.0,
      "category": "Makanan"
    }
  ],
  "category_summary": "Belanja harian kebutuhan pokok rumah tangga",
  "confidence_score": 0.9
}
```

---

## 🗂️ Kategori Item

| Kategori | Contoh Produk |
|----------|--------------|
| Makanan | Indomie, beras, minyak goreng, snack |
| Minuman | Aqua, teh botol, susu, pocari |
| Kebersihan | Rinso, Sunlight, sabun, shampo |
| Perawatan Diri | Lotion, skincare, deodoran |
| Kesehatan | Paracetamol, vitamin, masker |
| Elektronik | Baterai, kabel, charger |
| Rumah Tangga | Piring, ember, kantong plastik |
| Pakaian | Baju, kaos kaki, pakaian dalam |
| Alat Tulis | Pulpen, buku tulis, pensil |
| Lainnya | Item di luar kategori di atas |

---

## 🛠️ Tech Stack

- **TensorFlow** — Model deteksi lokasi struk
- **EasyOCR** — Ekstraksi teks dari gambar
- **Llama 3.3 70B** (via HuggingFace) — Parsing & analisis teks struk
- **FastAPI** — REST API backend
- **Streamlit** — UI frontend
- **Pydantic** — Schema validasi data

