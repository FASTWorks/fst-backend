# Fast Finance Backend API Documentation

## 1. Overview

Fast Finance Backend diimplementasikan menggunakan arsitektur **Microservices**. Seluruh komunikasi antara klien (seperti aplikasi *mobile* atau web) dengan layanan backend diatur secara terpusat melalui **API Gateway**.

### API Gateway sebagai Entry Point Utama
API Gateway berfungsi sebagai *Reverse Proxy* tunggal yang menerima semua permintaan HTTP dari luar. Gateway bertanggung jawab untuk:
1. Validasi Autentikasi (JWT Verification) secara global.
2. Melakukan perlindungan dengan *Rate Limiting* (termasuk limit ketat untuk endpoint berat seperti OCR).
3. Meneruskan request yang valid ke service internal (downstream) yang sesuai dan menyisipkan header `x-internal-auth`.

### Service-Service yang Tersedia
Proyek ini terdiri dari beberapa *microservices* mandiri:
- **API Gateway** (`fst-gateway-service`): Pintu gerbang utama.
- **Auth Service** (`fst-auth-service`): Menangani registrasi, login, verifikasi email, dan manajemen profil.
- **Finance Service** (`fst-finance-service`): Mengelola pencatatan pemasukan, pengeluaran, anggaran (budget), tabungan (saving), dan validasi struk.
- **Analytics Service** (`fst-analytics-service`): Menyediakan data statistik, grafik ringkasan keuangan, dan analitik.
- **Aggregator Service** (`fst-aggregator-service`): Bertugas menggabungkan data dari berbagai service (seperti gabungan data profile + dashboard) untuk *Home Screen* klien sehingga hanya butuh satu kali *request*.
- **AI/OCR Service** (`fst-ai-service`): Layanan berbasis Python/FastAPI untuk mengekstrak teks dari foto struk dan mengkategorikan pembelanjaan menggunakan LLM (Hugging Face).

### Pola Autentikasi
1. **Public Routes**: Dapat diakses tanpa token (contoh: Login, Register).
2. **Protected Routes**: Harus diakses menggunakan header `Authorization: Bearer <jwt_token>`. Token ini divalidasi oleh Gateway.
3. **Internal Auth**: Service *downstream* (Auth, Finance, dll) memvalidasi keaslian *request* dari Gateway melalui header `x-internal-auth` (berisi secret key) dan payload konteks pengguna (seperti `x-user-id`, `x-user-email`).

### Format Response Umum
Seluruh endpoint secara konsisten mengembalikan struktur JSON standar berikut:

**Sukses:**
```json
{
  "success": true,
  "message": "Deskripsi sukses",
  "data": { ... } // Objek atau array data
}
```

**Gagal / Error (Divalidasi oleh Zod atau Error Handler):**
```json
{
  "success": false,
  "message": "Deskripsi error (misalnya: Email sudah terdaftar atau Token tidak valid)"
}
```

---

## 2. API Gateway Routes (`fst-gateway-service`)

Gateway bertugas mem-proxy semua rute ke layanan masing-masing.

- `/api/auth/*` ➔ Diteruskan ke **Auth Service**
- `/api/finance/*` ➔ Diteruskan ke **Finance Service**
- `/api/analytics/*` ➔ Diteruskan ke **Analytics Service**
- `/api/aggregator/*` ➔ Diteruskan ke **Aggregator Service**
- `/api/health` ➔ Status gateway itu sendiri
- `/api-docs` ➔ Swagger UI Documentation

---

## 3. Auth Service Endpoints

Semua request dialamatkan ke `/api/auth/...` melalui Gateway.

### Public Endpoints
- **POST `/register`**
  - **Body JSON**: `{"email": "user@mail.com", "password": "...", "name": "..."}`
  - **Fungsi**: Mendaftarkan pengguna baru.

- **POST `/login`**
  - **Body JSON**: `{"email": "user@mail.com", "password": "..."}`
  - **Fungsi**: Otentikasi pengguna dan mengembalikan JWT *access token* dan *refresh token*.

- **POST `/refresh`**
  - **Body JSON**: `{"refreshToken": "..."}`
  - **Fungsi**: Mendapatkan *access token* baru.

- **GET `/verify-email?token=...`**
  - **Fungsi**: Memverifikasi email pengguna menggunakan token dari email.

- **POST `/resend-verification`**
  - **Body JSON**: `{"email": "user@mail.com"}`
  - **Fungsi**: Mengirim ulang email verifikasi.

- **POST `/google`**
  - **Body JSON**: `{"idToken": "..."}`
  - **Fungsi**: Login menggunakan akun Google.

- **POST `/forgot-password`**
  - **Body JSON**: `{"email": "user@mail.com"}`
  - **Fungsi**: Meminta link reset password.

- **POST `/reset-password`**
  - **Body JSON**: `{"token": "...", "newPassword": "..."}`
  - **Fungsi**: Mereset password.

### Protected Endpoints (Butuh JWT Token)
- **GET `/profile`**
  - **Fungsi**: Mendapatkan detail profil pengguna yang sedang login.

- **PUT `/profile/password`**
  - **Body JSON**: `{"currentPassword": "...", "newPassword": "..."}`
  - **Fungsi**: Mengubah password pengguna.

- **DELETE `/profile`**
  - **Body JSON**: `{"password": "..."}`
  - **Fungsi**: Menghapus akun pengguna (permanen).

- **POST `/logout`**
  - **Body JSON**: `{"refreshToken": "..."}`
  - **Fungsi**: Melakukan logout dan mencabut validitas refresh token.

---

## 4. Finance Service Endpoints

Semua request dialamatkan ke `/api/finance/...` melalui Gateway. Seluruh rute **wajib** menggunakan *access token*.

### Income (Pemasukan)
- **GET `/incomes`** (Query params opsional: `startDate`, `endDate`, `page`, `limit`)
- **POST `/incomes`**
  - **Body JSON**: 
    ```json
    {
      "amount": 10000000,
      "alloc_kebutuhan_primer": 5000000,
      "alloc_kebutuhan_sekunder": 3000000,
      "alloc_dana_darurat": 1000000,
      "alloc_tabungan": 1000000,
      "is_saving_active": true,
      "saving_goal_id": "123e4567-e89b-12d3-a456-426614174000",
      "income_date": "2026-05-20T00:00:00.000Z",
      "note": "Gaji Bulanan"
    }
    ```
- **PUT `/incomes/:id`** (Body opsional sama seperti POST)
- **DELETE `/incomes/:id`**

### Transactions (Pengeluaran)
- **GET `/transactions`** (Query params opsional: `type`, `parent_category`, `sub_category`, `startDate`, `endDate`)
- **POST `/transactions`**
  - **Body JSON**:
    ```json
    {
      "type": "expense",
      "amount": 50000,
      "name": "Makan Siang",
      "parent_category": "kebutuhan_primer",
      "transaction_date": "2026-05-25T12:00:00Z"
    }
    ```
- **PUT `/transactions/:id`**
- **DELETE `/transactions/:id`**

### Budgets (Anggaran)
- **GET `/budget/summary`** 
  - **Fungsi**: Menampilkan kalkulasi *allocated* vs *spent* untuk seluruh kategori pada bulan ini.
- **PUT `/budget/:period`** (period: "YYYY-MM")
  - **Body JSON**: 
    ```json
    {
      "spent_kebutuhan_primer": 50000
    }
    ```

### Saving Goals (Tabungan Berjangka)
- **GET `/saving-goals`**
- **POST `/saving-goals`**
  - **Body JSON**:
    ```json
    {
      "goal_name": "Liburan ke Bali",
      "target_amount": 5000000,
      "saving_frequency": "monthly",
      "saving_amount": 500000
    }
    ```
- **PUT `/saving-goals/:id`**
- **DELETE `/saving-goals/:id`**
- **POST `/saving-goals/:id/add-money`** (Menambah saldo tabungan dari pemasukan/alokasi)

### Receipts (Bukti Struk & AI OCR)
- **POST `/receipts/manual`**
  - **Fungsi**: Memasukkan data struk secara manual (tanpa foto).
- **POST `/receipts/ocr`** (Rate Limit: 5x/menit)
  - **Tipe**: `multipart/form-data`
  - **Parameter**: `image` (File gambar JPG/PNG)
  - **Fungsi**: Mengupload foto struk. Service ini akan memanggil `fst-ai-service` di *background* untuk mengekstrak dan mengklasifikasikan barang (item).
- **GET `/receipts/:id`**
- **POST `/receipts/:id/confirm`**
  - **Body JSON**: Menyertakan item list final setelah di-*review* oleh pengguna.
- **POST `/receipts/:id/reject`**
- **PUT `/receipts/:receiptId/items/:itemId/category`** (Koreksi manual kategori AI)

---

## 5. Analytics Service Endpoints

Semua request dialamatkan ke `/api/analytics/...` melalui Gateway. Wajib menggunakan token.

- **GET `/dashboard`**
  - **Fungsi**: Menghasilkan insight dan metrik utama analitik pengguna secara komprehensif, mulai dari tren 7/30 hari, pengeluaran terbesar, hingga rasio tabungan.
  - **Response**: Mengembalikan ringkasan data yang bisa langsung diproses oleh library *Chart/Graph* di frontend.

---

## 6. Aggregator Service Endpoints

Semua request dialamatkan ke `/api/aggregator/...` melalui Gateway. Wajib menggunakan token.

- **GET `/home`**
  - **Fungsi**: *Orchestrator endpoint* yang secara paralel memanggil service internal (`Auth` untuk nama/profil, `Finance` untuk saldo budget dan saving, `Analytics` untuk *insight AI* harian).
  - **Tujuan**: Memungkinkan aplikasi *Mobile/Web* meload halaman depan secara instan dalam 1 *HTTP Request* tanpa harus *fetching* data ke 3 API terpisah.

---

## 7. AI Service Endpoints (Internal / Backend-to-Backend)

Service ini dibangun dengan **FastAPI (Python)**. Gateway TIDAK mem-proxy langsung rute ini ke klien luar. Service ini murni dipanggil oleh `Finance Service` atau `Analytics Service` di *background*.

- **GET `/health`**
  - **Fungsi**: Memeriksa status kesiapan *Worker AI* dan engine OCR.
  
- **POST `/predict`**
  - **Tipe**: `multipart/form-data` (File)
  - **Fungsi**: Memproses gambar mentah, menjalankan `EasyOCR` untuk membaca teks, dan `HuggingFace LLM` untuk merapikan teks kacau menjadi JSON array terstruktur.
  
- **POST `/ocr/classify-items`**
  - **Body JSON**: `{"items": [{"name": "Indomie", "price": 3000}]}`
  - **Fungsi**: Mengirim list nama barang ke LLM (Llama-3) untuk mengelompokkan barang tersebut ke dalam kategori pengeluaran standar (Makanan, Perawatan Diri, dll).

- **POST `/analytics/insight`**
  - **Body JSON**: `{"income": 100, "expense": 50, "trend": [...]}`
  - **Fungsi**: Mengembalikan satu kalimat cerdas rekomendasi *financial planner* dari LLM (contoh: "Pengeluaran Anda bulan ini sangat terkontrol, pertahankan!").
