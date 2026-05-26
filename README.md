# Panduan Menjalankan FAST Backend Monorepo

Selamat datang! Panduan ini dibuat untuk menuntun Anda langkah demi langkah (*step-by-step*) cara meng-clone, menyiapkan, dan menjalankan seluruh layanan (*microservices*) di dalam proyek ini dari nol, baik di sistem operasi **Windows** maupun **Linux / macOS**.

Proyek ini terdiri dari beberapa *service* (layanan) yang saling terhubung:
1. **Gateway Service** (Node.js) - Port: `3000`
2. **Auth Service** (Node.js) - Port: `3001`
3. **Aggregator Service** (Node.js) - Port: `3002`
4. **Finance Service** (Node.js) - Port: `3003`
5. **Analytics Service** (Node.js) - Port: `3004`
6. **AI Service** (Python) - Port: `8001`

---

## 🛠️ Persiapan Awal (Wajib Ada)
Sebelum mulai, pastikan laptop/komputer Anda sudah terinstal:
* **Node.js** (Versi 18 atau lebih baru)
* **Python** (Versi 3.10 atau lebih baru)
* **Docker Desktop** (Hanya jika Anda ingin menggunakan Cara 1 yang lebih praktis)
* **Git**

---

## 📥 LANGKAH 1: Clone Repositori & Submodule (Sangat Penting!)
Karena proyek ini terdiri dari beberapa repositori Git terpisah yang disatukan (*Git Submodules*), ikuti salah satu langkah berikut untuk melakukan clone agar folder layanan tidak kosong:

### Pilihan A: Jika Belum Pernah Melakukan Clone
Jalankan perintah ini di terminal Anda untuk meng-clone repositori utama beserta seluruh isi submodule-nya secara otomatis:
```bash
git clone --recursive https://github.com/FASTWorks/fst-backend.git
```

### Pilihan B: Jika Sudah Terlanjur Melakukan Clone (Tapi Folder Service Kosong)
Masuk ke dalam folder hasil clone Anda, kemudian jalankan perintah sinkronisasi ini:
```bash
cd fst-backend
git submodule update --init --recursive
```

---

## 🚀 CARA 1: Menjalankan Menggunakan Docker (Paling Praktis & Lintas Platform)
Jika Anda sudah menginstal Docker Desktop, cara ini adalah yang paling mudah dan dapat dijalankan di **Windows, Linux, maupun macOS** dengan perintah yang sama:

1. Buka Terminal Anda.
2. Pastikan posisi terminal berada di dalam direktori root `fst-backend` (atau `fast-backend`).
3. Jalankan perintah ini:
   ```bash
   docker-compose up -d --build
   ```
4. **Selesai!** Tunggu proses *build* selesai. Semua layanan akan langsung berjalan aktif di latar belakang.
5. **Cara Mematikannya:** Ketik `docker-compose down` di terminal.

---

## 💻 CARA 2: Menjalankan Secara Manual (Tanpa Docker)
Gunakan cara ini jika Anda ingin melihat langsung *live log* program berjalan di terminal atau sedang dalam tahap pengembangan kode (*development*).

---

### 🪟 PANDUAN KHUSUS WINDOWS

#### 1. Setup Python untuk AI Service (Hanya 1x di awal)
Buka terminal dan pastikan berada di folder utama proyek, lalu ketikkan:
```bash
cd fst-ai-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd ..
```
*(Tanda berhasil: Muncul tulisan `(venv)` di sebelah paling kiri baris terminal).*

#### 2. Setup Node.js untuk Semua Service Lainnya (Hanya 1x di awal)
Pastikan posisi terminal berada di root folder utama proyek, lalu jalankan:
```bash
npm install
```
*(Perintah ini akan secara otomatis berkeliling ke seluruh folder service Node.js untuk meng-install dependensinya).*

#### 3. Nyalakan Semua Service Bersamaan (Windows)
Di terminal folder root proyek, jalankan:
```bash
npm run dev:all
```
Semua 6 service akan langsung aktif bersamaan di satu layar terminal!

---

### 🐧 PANDUAN KHUSUS LINUX / macOS

#### 1. Setup Python untuk AI Service (Hanya 1x di awal)
Buka terminal dan pastikan berada di folder utama proyek, lalu ketikkan:
```bash
cd fst-ai-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
```
*(Tanda berhasil: Muncul tulisan `(venv)` di sebelah paling kiri baris terminal).*

#### 2. Setup Node.js untuk Semua Service Lainnya (Hanya 1x di awal)
Pastikan posisi terminal berada di root folder utama proyek, lalu jalankan:
```bash
npm install
```
*(Perintah ini akan secara otomatis berkeliling ke seluruh folder service Node.js untuk meng-install dependensinya).*

#### 3. Nyalakan Semua Service Bersamaan (Linux / macOS)
Di terminal folder root proyek, jalankan:
```bash
npm run dev:all:nix
```
Semua 6 service akan langsung aktif bersamaan di satu layar terminal!

---

## 🔗 Daftar Alamat (Endpoints) Utama
Setelah layanan menyala, Anda bisa mengaksesnya di aplikasi **Postman** atau **Browser** melalui alamat berikut:

* **Gateway API** (Gerbang Utama API): `http://localhost:3000`
* **Auth API** (Layanan Login): `http://localhost:3001`
* **Aggregator API** (Layanan Penggabung Data): `http://localhost:3002`
* **Finance API** (Layanan Keuangan): `http://localhost:3003`
* **Analytics API** (Layanan Grafik & Data): `http://localhost:3004`
* **AI API Docs** (Halaman Coba-coba AI): `http://localhost:8001/docs`

Selamat Mengembangkan Proyek! 🚀
