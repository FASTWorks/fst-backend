# Panduan Menjalankan FAST Backend Monorepo

Selamat datang! Panduan ini dibuat khusus untuk pemula. Anda akan dituntun langkah demi langkah ("step-by-step") cara menjalankan seluruh layanan (microservices) yang ada di dalam proyek ini dari nol.

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
- **Node.js** (Versi 18 atau lebih baru)
- **Python** (Versi 3.10 atau lebih baru)
- **Docker Desktop** (Hanya jika Anda ingin menggunakan Cara 1 yang lebih praktis)

Ada **2 cara** untuk menjalankan proyek ini. Silakan pilih salah satu saja:
1. **Cara Menggunakan Docker** (Sangat praktis, tinggal satu klik).
2. **Cara Manual Lokal** (Bagus jika Anda ingin mengedit kode (development) dan melihat terminal).

---

## 🚀 CARA 1: Menjalankan dengan Docker (Paling Praktis)

Jika Anda sudah menginstal Docker Desktop dan membiarkannya menyala, ini adalah cara paling mudah karena Docker akan mengurus semuanya secara otomatis.

1. Buka Terminal (Command Prompt / PowerShell / Terminal VS Code).
2. Arahkan direktori terminal agar berada di dalam folder `fast-backend`.
3. Jalankan perintah ajaib ini:
   ```bash
   docker-compose up -d --build
   ```
4. **Selesai!** Tunggu proses *build* selesai. Semua layanan akan langsung menyala di belakang layar.
5. **Cara mematikannya:** Jika sudah selesai bekerja, ketik `docker-compose down` di terminal.

---

## 💻 CARA 2: Menjalankan Secara Manual (Tanpa Docker)

Gunakan cara ini jika Anda ingin melihat langsung *log* program berjalan di terminal Anda atau sedang ingin "ngoding" (development).

Karena kita menggunakan **Python** (untuk *AI Service*) dan **Node.js** (untuk layanan lainnya), kita harus menyiapkan keduanya. 

*(Catatan: Anda hanya perlu melakukan **Langkah 1** dan **Langkah 2** ini **satu kali saja** di awal, bukan setiap kali mau menyalakan program).*

### Langkah 1: Siapkan Python untuk AI Service
Kita perlu membuat lingkungan terisolasi agar instalasi Python tidak berantakan.

1. Buka Terminal dan pastikan berada di folder `fast-backend`.
2. Masuk ke folder layanan AI:
   ```bash
   cd fst-ai-service
   ```
3. Buat ruang terisolasi (*virtual environment*) bernama `venv`:
   ```bash
   python -m venv venv
   ```
4. Aktifkan *virtual environment* tersebut (Perintah untuk pengguna Windows):
   ```bash
   venv\Scripts\activate
   ```
   *(Tanda berhasil: Akan muncul tulisan `(venv)` di sebelah paling kiri ketikan terminal Anda).*
5. Instal semua pustaka/library AI yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```
6. Jika sudah selesai, kembali mundur ke folder utama `fast-backend`:
   ```bash
   cd ..
   ```

### Langkah 2: Siapkan Node.js untuk Semua Layanan Lainnya
1. Pastikan posisi terminal Anda sekarang berada di folder root `fast-backend`.
2. Jalankan perintah instalasi utama:
   ```bash
   npm install
   ```
   *(Duduk manis dan tunggu! Perintah ini akan menginstal alat bantu, lalu secara ajaib berkeliling ke seluruh 5 folder layanan Node.js Anda untuk menginstal semua `node_modules` mereka secara otomatis).*

### Langkah 3: Nyalakan Semua Service Bersamaan! (Tahap Akhir)
Jika Langkah 1 dan 2 sudah beres, ini adalah satu-satunya perintah yang perlu Anda jalankan setiap harinya.

1. Di terminal yang berada di folder `fast-backend`, ketikkan:
   ```bash
   npm run dev:all
   ```
2. **Selesai!** Terminal Anda akan terbelah menjadi berbagai warna cantik. Masing-masing warna mewakili laporan langsung (*live log*) dari *service* yang berbeda. Keenam layanan Anda berjalan serentak!
3. **Cara mematikannya:** Cukup tekan tombol `Ctrl + C` pada keyboard Anda di terminal tersebut, lalu jika ditanya, ketik `Y` dan `Enter`.

---

## 🔗 Daftar Alamat (Endpoints) Utama
Setelah layanan menyala, Anda bisa mengaksesnya di aplikasi **Postman** atau **Browser** melalui alamat berikut:

- **Gateway API** (Gerbang Utama API): `http://localhost:3000`
- **Auth API** (Layanan Login): `http://localhost:3001`
- **Aggregator API** (Layanan Penggabung Data): `http://localhost:3002`
- **Finance API** (Layanan Keuangan): `http://localhost:3003`
- **Analytics API** (Layanan Grafik & Data): `http://localhost:3004`
- **AI API Docs** (Halaman Coba-coba AI): `http://localhost:8001/docs`

Selamat Mengembangkan Proyek! 🚀
