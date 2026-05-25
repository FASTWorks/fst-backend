import io
import json
import re
import cv2
import numpy as np
import easyocr
import tensorflow as tf
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from huggingface_hub import InferenceClient
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# ─────────────────────────────────────────────
# Pydantic Schemas
# ─────────────────────────────────────────────

class Item(BaseModel):
    name: str
    price: Optional[float] = 0.0
    category: Optional[str] = "Lainnya"

class OCRResponse(BaseModel):
    store_name: Optional[str] = "Tidak Diketahui"
    date: Optional[str] = None
    total_amount: Optional[float] = 0.0
    items: List[Item] = []
    category_summary: Optional[str] = None
    confidence_score: Optional[float] = 0.0

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────

HF_TOKEN = "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"
MODEL_PATH = "best_detection_model.keras"
INPUT_SHAPE = (224, 224)

# ─────────────────────────────────────────────
# Load Model Deteksi
# ─────────────────────────────────────────────

detector = None
try:
    detector = tf.keras.models.load_model(MODEL_PATH, compile=False)
    print(f"✅ Model deteksi berhasil dimuat!")
except Exception as e:
    print(f"❌ Gagal load model: {e}")

# ─────────────────────────────────────────────
# EasyOCR
# ─────────────────────────────────────────────

reader = easyocr.Reader(['id'], gpu=False)

# ─────────────────────────────────────────────
# LLM Parser
# ─────────────────────────────────────────────

SYSTEM_PROMPT = """Kamu adalah sistem ekstraksi dan analisis data struk belanja yang sangat teliti dan cerdas.
Tugasmu adalah mengubah teks mentah hasil OCR dari struk belanja menjadi JSON terstruktur.

Kembalikan HANYA objek JSON yang valid, tanpa penjelasan, tanpa markdown, tanpa backtick.

Schema yang harus diikuti:
{
  "store_name": "string atau null",
  "date": "string format YYYY-MM-DD atau null jika tidak ada",
  "total_amount": float atau 0.0,
  "items": [
    {"name": "string", "price": float atau 0.0, "category": "string"}
  ],
  "category_summary": "string deskriptif atau null",
  "confidence_score": float antara 0.0-1.0
}

═══════════════════════════════════════
PANDUAN KATEGORISASI ITEM (category)
═══════════════════════════════════════
Tentukan kategori berdasarkan nama item. Gunakan pengetahuanmu tentang produk Indonesia.
Pilih SATU kategori yang paling tepat dari daftar berikut:

• Makanan          → beras, mie instan, roti, snack, kerupuk, biskuit, kecap, saos, bumbu masak,
                     minyak goreng, gula, garam, tepung, telur, daging, ikan, sayur, buah,
                     frozen food, indomie, supermi, pop mie, chitato, taro, dll.

• Minuman          → air mineral, aqua, susu, teh, kopi, jus, sirup, minuman energi, softdrink,
                     coca-cola, sprite, fanta, ultra milk, indomilk, teh botol, pocari, dll.

• Kebersihan       → sabun mandi, shampo, pasta gigi, sikat gigi, sabun cuci, detergen, pewangi,
                     pembersih lantai, tisu, toilet paper, pembalut, popok, hand sanitizer,
                     sunlight, so klin, rinso, attack, lifebuoy, dove, pantene, dll.

• Perawatan Diri   → pelembap, lotion, sunscreen, deodoran, parfum, kapas, cotton bud,
                     lipstik, bedak, makeup, skincare, body lotion, hand cream, dll.

• Kesehatan        → obat-obatan, vitamin, suplemen, masker medis, termometer, plester,
                     antiseptik, minyak kayu putih, tolak angin, antangin, paracetamol, dll.

• Elektronik       → baterai, lampu, kabel, charger, earphone, flashdisk, bolam, dll.

• Rumah Tangga     → peralatan dapur, piring, gelas, sendok, ember, sapu, pel, kain lap,
                     kantong plastik, aluminium foil, plastik wrap, lilin, korek api, dll.

• Pakaian          → baju, celana, kaos, jaket, sepatu, sandal, kaos kaki, pakaian dalam, dll.

• Alat Tulis       → pulpen, pensil, buku tulis, kertas, penggaris, stabilo, dll.

• Lainnya          → item yang tidak cocok dengan kategori di atas.

Panduan tambahan:
- Nama produk sering disingkat di struk (contoh: "INDO MIE GRG" = Indomie Goreng → Makanan)
- Kode produk/barcode di depan nama item → abaikan, fokus ke nama produknya
- Kalau ragu antara 2 kategori, pilih yang paling dominan fungsinya

═══════════════════════════════════════
PANDUAN CATEGORY SUMMARY
═══════════════════════════════════════
Buat ringkasan belanja yang DESKRIPTIF dan KONTEKSTUAL berdasarkan pola item yang dibeli.
Bukan hanya sebutkan kategorinya, tapi deskripsikan TUJUAN atau KARAKTER belanja ini.

Contoh pola dan summary yang baik:
- Mayoritas beras, minyak, bumbu, sayur, protein → "Belanja bulanan kebutuhan dapur dan bahan masak"
- Banyak snack, minuman, frozen food → "Belanja camilan dan makanan siap saji"
- Detergen, sabun, shampo, tisu → "Belanja perlengkapan kebersihan dan perawatan rumah"
- Obat, vitamin, masker → "Belanja kebutuhan kesehatan dan pertolongan pertama"
- Campuran sembako + sabun + snack → "Belanja harian kebutuhan pokok rumah tangga"
- Mayoritas satu kategori → sebutkan kategori itu secara spesifik
- Belanja sangat sedikit (1-3 item) → "Belanja cepat untuk kebutuhan mendesak"

Aturan summary:
- Maksimal 10 kata, padat dan informatif
- Gunakan bahasa natural Indonesia, tidak kaku
- Jangan hanya tulis "Belanja makanan dan minuman" kalau bisa lebih spesifik
- Cerminkan konteks nyata dari isi struk

═══════════════════════════════════════
ATURAN UMUM
═══════════════════════════════════════
- Harga dalam float tanpa simbol mata uang (contoh: 15000.0 bukan "Rp 15.000")
- total_amount harus dijumlahkan dari semua item yang sudah dikonversi ke rupiah penuh.
  Jangan ambil angka total mentah dari teks jika terlihat terpotong.
- Harga di struk Indonesia umumnya dalam satuan RUPIAH penuh (bukan ribuan).
  Titik (.) di harga struk Indonesia adalah pemisah ribuan, BUKAN desimal (contoh: 36.000 = 36000.0, bukan 36.0).
  Jika harga terdeteksi < 500, kemungkinan besar terpotong (misal 36 → 36000, 7 → 7000).
  Coba baca ulang konteks sekitar angka tersebut untuk memastikan nilai yang benar.
- Jika teks OCR rusak atau tidak jelas, tetap ekstrak semaksimal mungkin
- confidence_score: 1.0 = teks sangat jelas, 0.5 = ada bagian tidak terbaca, 0.2 = banyak yang rusak
"""

llm_client = InferenceClient(token=HF_TOKEN)

def parse_with_llm(raw_text: str) -> OCRResponse:
    if not raw_text or not raw_text.strip():
        return OCRResponse()

    raw_json_str = ""
    try:
        response = llm_client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Ekstrak informasi dari teks struk berikut:\n\n---\n{raw_text}\n---"},
            ],
            max_tokens=1024,
            temperature=0.1,
        )

        raw_json_str = response.choices[0].message.content.strip()
        raw_json_str = re.sub(r"^```(?:json)?\s*", "", raw_json_str)
        raw_json_str = re.sub(r"\s*```$", "", raw_json_str)

        parsed_dict = json.loads(raw_json_str)
        return OCRResponse(**parsed_dict)

    except json.JSONDecodeError as e:
        print(f"[LLM] Gagal parse JSON: {e} | raw: {raw_json_str[:300]}")
        return OCRResponse()
    except Exception as e:
        print(f"[LLM] Error: {e}")
        return OCRResponse()

# ─────────────────────────────────────────────
# Image Processing
# ─────────────────────────────────────────────

def get_bounding_box(image):
    h_orig, w_orig = image.shape[:2]
    resized = cv2.resize(image, (INPUT_SHAPE[1], INPUT_SHAPE[0]))
    normalized = resized.astype(np.float32) / 255.0
    input_batch = np.expand_dims(normalized, axis=0)

    preds = detector.predict(input_batch, verbose=0)[0]
    x1 = max(0, int(preds[0] * w_orig))
    y1 = max(0, int(preds[1] * h_orig))
    x2 = min(w_orig, int(preds[2] * w_orig))
    y2 = min(h_orig, int(preds[3] * h_orig))

    return [x1, y1, x2, y2]

def preprocess_for_ocr(image, bbox):
    x1, y1, x2, y2 = bbox
    cropped = image[y1:y2, x1:x2]

    if cropped is None or cropped.size == 0:
        return None

    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    h, w = gray.shape
    if h < 64:
        scale_factor = 64 / h
        gray = cv2.resize(gray, (int(w * scale_factor), 64), interpolation=cv2.INTER_LANCZOS4)

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        15, 2
    )
    return thresh

def extract_text(processed_img) -> str:
    if processed_img is None:
        return ""
    results = reader.readtext(processed_img, detail=0, paragraph=True)
    return " ".join(results)

# ─────────────────────────────────────────────
# FastAPI
# ─────────────────────────────────────────────

app = FastAPI(title="Receipt OCR API")

@app.get("/")
async def root():
    return {
        "message": "Receipt OCR API is running 🚀",
        "version": "2.0.0",
        "endpoints": {
            "GET  /": "Info API",
            "GET  /health": "Cek status server & model",
            "POST /predict": "Upload gambar struk untuk di-OCR"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "model_loaded": detector is not None,
        "model_path": MODEL_PATH,
    }

@app.post("/predict", response_model=OCRResponse)
async def predict(file: UploadFile = File(...)):
    if detector is None:
        raise HTTPException(status_code=503, detail="Model belum berhasil dimuat.")

    try:
        # 1. Baca gambar
        contents = await file.read()
        pil_image = Image.open(io.BytesIO(contents)).convert('RGB')
        image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # 2. Deteksi bounding box
        bbox = get_bounding_box(image)

        # 3. Crop + preprocessing
        processed_img = preprocess_for_ocr(image, bbox)

        # 4. Ekstraksi teks
        raw_text = extract_text(processed_img)
        print(f"[OCR] Raw text: {raw_text[:200]}")

        # 5. LLM Parsing
        result = parse_with_llm(raw_text)
        return result

    except Exception as e:
        import traceback
        print(f"FULL ERROR:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
