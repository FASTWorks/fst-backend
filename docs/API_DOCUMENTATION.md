# FAST API Documentation

> **Base URL:** `http://localhost:3000`  
> **Auth:** Bearer Token (JWT) — kecuali endpoint publik  
> **Content-Type:** `application/json` (kecuali OCR: `multipart/form-data`)

---

## Daftar Isi

1. [API Gateway](#1-api-gateway)
2. [Auth](#2-auth)
   - [Login](#21-login)
   - [Register](#22-register)
   - [User Account Service](#23-user-account-service)
3. [Profile](#3-profile)
4. [Finance](#4-finance)
   - [Catatan Pemasukan](#41-catatan-pemasukan)
   - [Catatan Pengeluaran — Quick Input](#42-catatan-pengeluaran--quick-input)
   - [Catatan Pengeluaran — Receipts Manual](#43-catatan-pengeluaran--receipts-manual)
   - [Catatan Pengeluaran — Receipts OCR](#44-catatan-pengeluaran--receipts-ocr)
   - [Tabungan](#45-tabungan)
5. [Analytics](#5-analytics)
6. [Aggregator](#6-aggregator)

---

## 1. API Gateway

Endpoint untuk mengecek status health dari seluruh service yang terdaftar.

---

### Check Health Gateway

```
GET /health
```

**Auth:** Tidak diperlukan

**Response 200:**
```json
{
  "status": "ok",
  "service": "API Gateway",
  "timestamp": "2026-05-25T10:00:00.000Z"
}
```

---

### Check Health Auth Service

```
GET /health/auth
```

**Response 200:**
```json
{
  "status": "ok",
  "service": "Auth Service"
}
```

---

### Check Health Aggregator Service

```
GET /health/aggregator
```

**Response 200:**
```json
{
  "status": "ok",
  "service": "Aggregator Service"
}
```

---

### Check Health Finance Service

```
GET /health/finance
```

**Response 200:**
```json
{
  "status": "ok",
  "service": "Finance Service"
}
```

---

### Check Health Analytics Service

```
GET /health/analytics
```

**Response 200:**
```json
{
  "status": "ok",
  "service": "Analytics Service"
}
```

---

## 2. Auth

### 2.1 Login

#### Login dengan Email

```
POST /api/auth/login
```

**Auth:** Tidak diperlukan

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "Password123!"
}
```

| Field      | Type   | Required | Keterangan             |
|------------|--------|----------|------------------------|
| `email`    | string | ✅        | Email terdaftar        |
| `password` | string | ✅        | Password akun          |

**Response 200:**
```json
{
  "status": "success",
  "message": "Login berhasil",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "userId": "ec4ed35c-3aa5-4349-8350-afbc285fdae1",
      "name": "Abdurrahman",
      "email": "user@example.com",
      "role": "user"
    }
  }
}
```

**Response 401:**
```json
{
  "status": "error",
  "message": "Email atau password salah"
}
```

---

#### Login dengan Google

```
POST /api/auth/google
```

**Auth:** Tidak diperlukan

**Request Body:**
```json
{
  "code": "<google_oauth_authorization_code>",
  "authType": "login"
}
```

| Field      | Type   | Required | Keterangan                              |
|------------|--------|----------|-----------------------------------------|
| `code`     | string | ✅        | Authorization code dari Google OAuth    |
| `authType` | string | ✅        | Nilai: `"login"` atau `"register"`      |

**Response 200:**
```json
{
  "status": "success",
  "message": "Login Google berhasil",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "userId": "ec4ed35c-3aa5-4349-8350-afbc285fdae1",
      "name": "Abdurrahman",
      "email": "user@example.com",
      "role": "user"
    }
  }
}
```

---

#### Logout

```
POST /api/auth/logout
```

**Auth:** Bearer Token

**Request Body:**
```json
{
  "refreshToken": "<refresh_token_or_access_token>"
}
```

| Field          | Type   | Required | Keterangan                   |
|----------------|--------|----------|------------------------------|
| `refreshToken` | string | ✅        | Refresh token yang aktif     |

**Response 200:**
```json
{
  "status": "success",
  "message": "Logout berhasil"
}
```

---

### 2.2 Register

#### Register dengan Email

```
POST /api/auth/register
```

**Auth:** Tidak diperlukan

**Request Body:**
```json
{
  "name": "Abdurrahman",
  "email": "user@example.com",
  "password": "Password123!"
}
```

| Field      | Type   | Required | Keterangan                                      |
|------------|--------|----------|-------------------------------------------------|
| `name`     | string | ✅        | Nama lengkap pengguna                           |
| `email`    | string | ✅        | Email valid dan belum terdaftar                 |
| `password` | string | ✅        | Min 8 karakter, kombinasi huruf & angka         |

**Response 201:**
```json
{
  "status": "success",
  "message": "Registrasi berhasil. Silakan cek email untuk verifikasi.",
  "data": {
    "userId": "ec4ed35c-3aa5-4349-8350-afbc285fdae1",
    "name": "Abdurrahman",
    "email": "user@example.com"
  }
}
```

**Response 409:**
```json
{
  "status": "error",
  "message": "Email sudah terdaftar"
}
```

---

#### Register dengan Google

```
POST /api/auth/google
```

**Auth:** Tidak diperlukan

**Request Body:**
```json
{
  "code": "<google_oauth_authorization_code>",
  "authType": "register"
}
```

| Field      | Type   | Required | Keterangan                              |
|------------|--------|----------|-----------------------------------------|
| `code`     | string | ✅        | Authorization code dari Google OAuth    |
| `authType` | string | ✅        | Nilai: `"register"`                     |

**Response 201:**
```json
{
  "status": "success",
  "message": "Registrasi Google berhasil",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "userId": "ec4ed35c-3aa5-4349-8350-afbc285fdae1",
      "name": "Abdurrahman",
      "email": "user@example.com",
      "role": "user"
    }
  }
}
```

---

### 2.3 User Account Service

#### Verify Email

```
GET /api/auth/verify-email?token=<verification_token>
```

**Auth:** Tidak diperlukan

**Query Parameter:**

| Parameter | Type   | Required | Keterangan                              |
|-----------|--------|----------|-----------------------------------------|
| `token`   | string | ✅        | Token verifikasi yang dikirim via email |

**Contoh:**
```
GET http://localhost:3000/api/auth/verify-email?token=<token>
```

**Response 200:**
```json
{
  "status": "success",
  "message": "Email berhasil diverifikasi"
}
```

**Response 400:**
```json
{
  "status": "error",
  "message": "Token verifikasi tidak valid atau sudah kadaluarsa"
}
```

---

#### Resend Verify

```
POST /api/auth/resend-verification
```

**Auth:** Tidak diperlukan

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

| Field   | Type   | Required | Keterangan                      |
|---------|--------|----------|---------------------------------|
| `email` | string | ✅        | Email yang belum terverifikasi  |

**Response 200:**
```json
{
  "status": "success",
  "message": "Email verifikasi berhasil dikirim ulang"
}
```

---

#### Lupa Akun (Forgot Password)

```
POST /api/auth/forgot-password
```

**Auth:** Tidak diperlukan

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

| Field   | Type   | Required | Keterangan              |
|---------|--------|----------|-------------------------|
| `email` | string | ✅        | Email akun terdaftar    |

**Response 200:**
```json
{
  "status": "success",
  "message": "Link reset password telah dikirim ke email Anda"
}
```

---

#### Reset Password

```
POST /api/auth/reset-password
```

**Auth:** Tidak diperlukan

**Request Body:**
```json
{
  "token": "<token>",
  "email": "user@example.com",
  "password": "PasswordBaru123"
}
```

| Field      | Type   | Required | Keterangan                              |
|------------|--------|----------|-----------------------------------------|
| `token`    | string | ✅        | Token reset yang dikirim via email      |
| `email`    | string | ✅        | Email akun yang melakukan reset         |
| `password` | string | ✅        | Password baru (min 8 karakter)          |

**Response 200:**
```json
{
  "status": "success",
  "message": "Password berhasil direset"
}
```

**Response 400:**
```json
{
  "status": "error",
  "message": "Token reset tidak valid atau sudah kadaluarsa"
}
```

---

#### Refresh Token

```
POST /api/auth/refresh
```

**Auth:** Tidak diperlukan

**Request Body:**
```json
{
  "refreshToken": "<refresh_token_or_access_token>"
}
```

| Field          | Type   | Required | Keterangan                       |
|----------------|--------|----------|----------------------------------|
| `refreshToken` | string | ✅        | Refresh token yang masih berlaku |

**Response 200:**
```json
{
  "status": "success",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Response 401:**
```json
{
  "status": "error",
  "message": "Refresh token tidak valid atau sudah kadaluarsa"
}
```

---

## 3. Profile

### Get User Profile

```
GET /api/auth/profile
```

**Auth:** Bearer Token ✅

**Response 200:**
```json
{
  "status": "success",
  "data": {
    "userId": "ec4ed35c-3aa5-4349-8350-afbc285fdae1",
    "name": "Abdurrahman",
    "email": "user@example.com",
    "role": "user",
    "isVerified": true,
    "createdAt": "2026-05-01T00:00:00.000Z"
  }
}
```

---

### Change Password

```
PUT /api/auth/profile/password
```

**Auth:** Bearer Token ✅

**Request Body:**
```json
{
  "currentPassword": "Password123!",
  "newPassword": "NewSecurePassword456!"
}
```

| Field             | Type   | Required | Keterangan                    |
|-------------------|--------|----------|-------------------------------|
| `currentPassword` | string | ✅        | Password lama yang aktif      |
| `newPassword`     | string | ✅        | Password baru (min 8 karakter) |

**Response 200:**
```json
{
  "status": "success",
  "message": "Password berhasil diubah"
}
```

**Response 401:**
```json
{
  "status": "error",
  "message": "Password saat ini salah"
}
```

---

### Delete Account

```
DELETE /api/auth/profile
```

**Auth:** Bearer Token ✅

**Request Body:**
```json
{
  "password": "NewSecurePassword456!"
}
```

| Field      | Type   | Required | Keterangan                             |
|------------|--------|----------|----------------------------------------|
| `password` | string | ✅        | Password aktif untuk konfirmasi hapus  |

**Response 200:**
```json
{
  "status": "success",
  "message": "Akun berhasil dihapus"
}
```

**Response 401:**
```json
{
  "status": "error",
  "message": "Password salah"
}
```

---

## 4. Finance

### 4.1 Catatan Pemasukan

#### Pemasukan dengan Tabungan Aktif (ke Saving Goal Spesifik)

```
POST /api/finance/incomes
```

**Auth:** Bearer Token ✅

**Request Body:**
```json
{
  "amount": 10000000,
  "alloc_kebutuhan_primer": 5000000,
  "alloc_kebutuhan_sekunder": 3000000,
  "alloc_dana_darurat": 1000000,
  "alloc_tabungan": 1000000,
  "is_saving_active": true,
  "saving_goal_id": "84047016-e37c-42a1-9c41-fa9297a22c13",
  "income_date": "2026-05-20T00:00:00.000Z",
  "note": "Gaji Bulanan"
}
```

| Field                      | Type    | Required | Keterangan                                          |
|----------------------------|---------|----------|-----------------------------------------------------|
| `amount`                   | number  | ✅        | Total pemasukan                                     |
| `alloc_kebutuhan_primer`   | number  | ✅        | Alokasi kebutuhan primer                            |
| `alloc_kebutuhan_sekunder` | number  | ✅        | Alokasi kebutuhan sekunder                          |
| `alloc_dana_darurat`       | number  | ✅        | Alokasi dana darurat                                |
| `alloc_tabungan`           | number  | ✅        | Alokasi tabungan                                    |
| `is_saving_active`         | boolean | ✅        | `true` jika alokasi tabungan diaktifkan             |
| `saving_goal_id`           | string  | ❌        | UUID saving goal tujuan (jika `is_saving_active` true) |
| `income_date`              | string  | ✅        | Tanggal pemasukan format ISO 8601                   |
| `note`                     | string  | ❌        | Catatan tambahan                                    |

**Response 201:**
```json
{
  "status": "success",
  "message": "Pemasukan berhasil dicatat",
  "data": {
    "incomeId": "7d4d7b45-dcab-407c-aa74-1d9a6df94ff4",
    "amount": 10000000,
    "alloc_kebutuhan_primer": 5000000,
    "alloc_kebutuhan_sekunder": 3000000,
    "alloc_dana_darurat": 1000000,
    "alloc_tabungan": 1000000,
    "is_saving_active": true,
    "saving_goal_id": "84047016-e37c-42a1-9c41-fa9297a22c13",
    "income_date": "2026-05-20T00:00:00.000Z",
    "note": "Gaji Bulanan",
    "createdAt": "2026-05-20T08:00:00.000Z"
  }
}
```

---

#### Pemasukan dengan Tabungan Aktif (Tabungan Umum)

```
POST /api/finance/incomes
```

**Auth:** Bearer Token ✅

**Request Body:**
```json
{
  "amount": 10000000,
  "alloc_kebutuhan_primer": 5000000,
  "alloc_kebutuhan_sekunder": 3000000,
  "alloc_dana_darurat": 1000000,
  "alloc_tabungan": 1000000,
  "is_saving_active": true,
  "income_date": "2026-05-20T00:00:00.000Z",
  "note": "Gaji Bulanan - Nabung umum dulu"
}
```

> `saving_goal_id` tidak disertakan — tabungan masuk ke tabungan umum.

---

#### Pemasukan Tanpa Tabungan

```
POST /api/finance/incomes
```

**Auth:** Bearer Token ✅

**Request Body:**
```json
{
  "amount": 10000000,
  "alloc_kebutuhan_primer": 5000000,
  "alloc_kebutuhan_sekunder": 3000000,
  "alloc_dana_darurat": 1000000,
  "alloc_tabungan": 0,
  "is_saving_active": false,
  "income_date": "2026-05-20T00:00:00.000Z",
  "note": "Gaji Bulanan - Lagi banyak pengeluaran"
}
```

> `is_saving_active: false` dan `alloc_tabungan: 0` — tidak ada dana yang dialokasikan ke tabungan.

---

#### Lihat Daftar Pemasukan

```
GET /api/finance/incomes
```

**Auth:** Bearer Token ✅

**Response 200:**
```json
{
  "status": "success",
  "data": [
    {
      "incomeId": "7d4d7b45-dcab-407c-aa74-1d9a6df94ff4",
      "amount": 10000000,
      "alloc_kebutuhan_primer": 5000000,
      "alloc_kebutuhan_sekunder": 3000000,
      "alloc_dana_darurat": 1000000,
      "alloc_tabungan": 1000000,
      "is_saving_active": true,
      "saving_goal_id": "84047016-e37c-42a1-9c41-fa9297a22c13",
      "income_date": "2026-05-20T00:00:00.000Z",
      "note": "Gaji Bulanan",
      "createdAt": "2026-05-20T08:00:00.000Z"
    }
  ]
}
```

---

#### Edit Pemasukan

```
PUT /api/finance/incomes/:id
```

**Auth:** Bearer Token ✅

**Path Parameter:**

| Parameter | Type   | Required | Keterangan          |
|-----------|--------|----------|---------------------|
| `id`      | string | ✅        | UUID income yang diedit |

**Request Body:**
```json
{
  "amount": 10000000,
  "alloc_kebutuhan_primer": 5000000,
  "alloc_kebutuhan_sekunder": 3000000,
  "alloc_dana_darurat": 1000000,
  "alloc_tabungan": 1000000,
  "is_saving_active": true,
  "new_saving_goal": {
    "goal_name": "Gak Tau",
    "target_amount": 20000000,
    "saving_frequency": "monthly",
    "saving_amount": 2000000
  },
  "income_date": "2026-05-20T00:00:00.000Z",
  "note": "Gaji Bulanan"
}
```

| Field                           | Type    | Required | Keterangan                                       |
|---------------------------------|---------|----------|--------------------------------------------------|
| `amount`                        | number  | ✅        | Total pemasukan                                  |
| `alloc_kebutuhan_primer`        | number  | ✅        | Alokasi kebutuhan primer                         |
| `alloc_kebutuhan_sekunder`      | number  | ✅        | Alokasi kebutuhan sekunder                       |
| `alloc_dana_darurat`            | number  | ✅        | Alokasi dana darurat                             |
| `alloc_tabungan`                | number  | ✅        | Alokasi tabungan                                 |
| `is_saving_active`              | boolean | ✅        | Status aktif tabungan                            |
| `new_saving_goal`               | object  | ❌        | Buat saving goal baru sekaligus                  |
| `new_saving_goal.goal_name`     | string  | ✅*       | Nama goal baru                                   |
| `new_saving_goal.target_amount` | number  | ✅*       | Target nominal                                   |
| `new_saving_goal.saving_frequency` | string | ✅*    | `"monthly"` / `"weekly"` / `"daily"`             |
| `new_saving_goal.saving_amount` | number  | ✅*       | Jumlah yang disisihkan per periode               |
| `income_date`                   | string  | ✅        | Tanggal pemasukan ISO 8601                       |
| `note`                          | string  | ❌        | Catatan tambahan                                 |

> *Wajib jika `new_saving_goal` disertakan.

**Response 200:**
```json
{
  "status": "success",
  "message": "Pemasukan berhasil diperbarui",
  "data": {
    "incomeId": "7d4d7b45-dcab-407c-aa74-1d9a6df94ff4",
    "amount": 10000000,
    "note": "Gaji Bulanan",
    "updatedAt": "2026-05-25T10:00:00.000Z"
  }
}
```

---

#### Hapus Pemasukan

```
DELETE /api/finance/incomes/7d4d7b45-dcab-407c-aa74-1d9a6df94ff4
```

**Auth:** Bearer Token ✅

**Path Parameter:**

| Parameter | Type   | Required | Keterangan              |
|-----------|--------|----------|-------------------------|
| `id`      | string | ✅        | UUID income yang dihapus |

**Response 200:**
```json
{
  "status": "success",
  "message": "Pemasukan berhasil dihapus"
}
```

---

### 4.2 Catatan Pengeluaran — Quick Input

#### Catat Pengeluaran

```
POST /api/finance/transactions
```

**Auth:** Bearer Token ✅

**Request Body:**
```json
{
  "type": "expense",
  "amount": 150000,
  "name": "Beli Kopi dan Cemilan",
  "parent_category": "kebutuhan_sekunder",
  "transaction_date": "2026-05-25T10:00:00.000Z"
}
```

| Field              | Type   | Required | Keterangan                                                         |
|--------------------|--------|----------|--------------------------------------------------------------------|
| `type`             | string | ✅        | Tipe transaksi: `"expense"`                                        |
| `amount`           | number | ✅        | Nominal pengeluaran                                                |
| `name`             | string | ✅        | Nama / deskripsi transaksi                                         |
| `parent_category`  | string | ✅        | Kategori: `"kebutuhan_primer"` / `"kebutuhan_sekunder"` / `"dana_darurat"` |
| `transaction_date` | string | ✅        | Tanggal transaksi format ISO 8601                                  |

**Response 201:**
```json
{
  "status": "success",
  "message": "Pengeluaran berhasil dicatat",
  "data": {
    "transactionId": "6318a378-96fa-4897-a4ea-29ea03443d29",
    "type": "expense",
    "amount": 150000,
    "name": "Beli Kopi dan Cemilan",
    "parent_category": "kebutuhan_sekunder",
    "transaction_date": "2026-05-25T10:00:00.000Z",
    "createdAt": "2026-05-25T10:05:00.000Z"
  }
}
```

---

#### Histori Pengeluaran

```
GET /api/finance/transactions
```

**Auth:** Bearer Token ✅

**Response 200:**
```json
{
  "status": "success",
  "data": [
    {
      "transactionId": "6318a378-96fa-4897-a4ea-29ea03443d29",
      "type": "expense",
      "amount": 150000,
      "name": "Beli Kopi dan Cemilan",
      "parent_category": "kebutuhan_sekunder",
      "transaction_date": "2026-05-25T10:00:00.000Z",
      "createdAt": "2026-05-25T10:05:00.000Z"
    }
  ]
}
```

---

#### Edit Pengeluaran

```
PUT /api/finance/transactions/:id
```

**Auth:** Bearer Token ✅

**Path Parameter:**

| Parameter | Type   | Required | Keterangan                  |
|-----------|--------|----------|-----------------------------|
| `id`      | string | ✅        | UUID transaksi yang diedit  |

**Request Body:**
```json
{
  "type": "expense",
  "amount": 150000,
  "name": "Beli Kopi dan Cemilan",
  "parent_category": "kebutuhan_sekunder",
  "transaction_date": "2026-05-25T10:00:00.000Z"
}
```

**Response 200:**
```json
{
  "status": "success",
  "message": "Pengeluaran berhasil diperbarui",
  "data": {
    "transactionId": "6318a378-96fa-4897-a4ea-29ea03443d29",
    "amount": 150000,
    "name": "Beli Kopi dan Cemilan",
    "updatedAt": "2026-05-25T11:00:00.000Z"
  }
}
```

---

#### Hapus Pengeluaran

```
DELETE /api/finance/transactions/6318a378-96fa-4897-a4ea-29ea03443d29
```

**Auth:** Bearer Token ✅

**Path Parameter:**

| Parameter | Type   | Required | Keterangan                    |
|-----------|--------|----------|-------------------------------|
| `id`      | string | ✅        | UUID transaksi yang dihapus   |

**Response 200:**
```json
{
  "status": "success",
  "message": "Pengeluaran berhasil dihapus"
}
```

---

### 4.3 Catatan Pengeluaran — Receipts Manual

#### Catat Struk Manual

```
POST /api/finance/receipts/manual
```

**Auth:** Bearer Token ✅

**Request Body:**
```json
{
  "store_name": "Baji Cafe",
  "receipt_date": "2026-05-20T00:00:00.000Z",
  "subtotal": 300000,
  "tax": 0,
  "discount": 0,
  "total": 300000,
  "source": "manual",
  "items": [
    {
      "item_name": "Avocado Toast",
      "qty": 1,
      "unit_price": 300000,
      "total_price": 300000
    }
  ]
}
```

| Field           | Type   | Required | Keterangan                            |
|-----------------|--------|----------|---------------------------------------|
| `store_name`    | string | ✅        | Nama toko / merchant                  |
| `receipt_date`  | string | ✅        | Tanggal struk ISO 8601                |
| `subtotal`      | number | ✅        | Subtotal sebelum pajak & diskon       |
| `tax`           | number | ✅        | Nominal pajak (0 jika tidak ada)      |
| `discount`      | number | ✅        | Nominal diskon (0 jika tidak ada)     |
| `total`         | number | ✅        | Total akhir yang dibayarkan           |
| `source`        | string | ✅        | Nilai: `"manual"`                     |
| `items`         | array  | ✅        | Daftar item dalam struk               |
| `items[].item_name` | string | ✅ | Nama item                             |
| `items[].qty` | number | ✅ | Jumlah item                           |
| `items[].unit_price` | number | ✅ | Harga satuan                          |
| `items[].total_price` | number | ✅ | Total harga item (`qty × unit_price`) |

**Response 201:**
```json
{
  "status": "success",
  "message": "Struk manual berhasil dicatat",
  "data": {
    "receiptId": "28e6459b-570b-4136-8a72-7df224506693",
    "store_name": "Baji Cafe",
    "receipt_date": "2026-05-20T00:00:00.000Z",
    "subtotal": 300000,
    "tax": 0,
    "discount": 0,
    "total": 300000,
    "source": "manual",
    "items": [
      {
        "item_name": "Avocado Toast",
        "qty": 1,
        "unit_price": 300000,
        "total_price": 300000
      }
    ],
    "createdAt": "2026-05-25T10:00:00.000Z"
  }
}
```

---

#### Detail Struk

```
GET /api/finance/receipts/28e6459b-570b-4136-8a72-7df224506693
```

**Auth:** Bearer Token ✅

**Path Parameter:**

| Parameter | Type   | Required | Keterangan           |
|-----------|--------|----------|----------------------|
| `id`      | string | ✅        | UUID receipt         |

**Response 200:**
```json
{
  "status": "success",
  "data": {
    "receiptId": "28e6459b-570b-4136-8a72-7df224506693",
    "store_name": "Baji Cafe",
    "receipt_date": "2026-05-20T00:00:00.000Z",
    "subtotal": 300000,
    "tax": 0,
    "discount": 0,
    "total": 300000,
    "source": "manual",
    "items": [
      {
        "item_name": "Avocado Toast",
        "qty": 1,
        "unit_price": 300000,
        "total_price": 300000
      }
    ]
  }
}
```

---

#### Histori Pengeluaran (dari Receipts Manual)

```
GET /api/finance/transactions
```

> Sama dengan endpoint histori transaksi di Quick Input — mengembalikan semua transaksi termasuk yang berasal dari struk.

---

#### Hapus Pengeluaran (dari Receipts Manual)

```
DELETE /api/finance/transactions/6318a378-96fa-4897-a4ea-29ea03443d29
```

> Sama dengan endpoint hapus transaksi di Quick Input.

---

### 4.4 Catatan Pengeluaran — Receipts OCR

#### Catat Struk OCR

```
POST /api/finance/receipts/ocr
```

**Auth:** Bearer Token ✅  
**Content-Type:** `multipart/form-data`

**Request Body (Form Data):**

| Field   | Type | Required | Keterangan                       |
|---------|------|----------|----------------------------------|
| `image` | file | ✅        | File gambar struk (jpg/png/webp) |

**Contoh di Hoppscotch:**
- Content Type: `multipart/form-data`
- Key: `image`
- Value: pilih file gambar struk

**Response 200:**
```json
{
  "status": "success",
  "message": "OCR berhasil diproses. Silakan konfirmasi hasilnya.",
  "data": {
    "receiptId": "74bf8cee-95bb-4b34-9419-a33515f9acf3",
    "store_name": "Baji Cafe",
    "receipt_date": "2026-05-20T00:00:00.000Z",
    "subtotal": 300000,
    "tax": 0,
    "discount": 0,
    "total": 300000,
    "source": "ocr",
    "items": [
      {
        "item_name": "Avocado Toast",
        "qty": 1,
        "unit_price": 300000,
        "total_price": 300000
      }
    ],
    "ocr_confidence": 0.94
  }
}
```

---

#### Konfirmasi Hasil OCR

```
POST /api/finance/receipts/74bf8cee-95bb-4b34-9419-a33515f9acf3/confirm
```

**Auth:** Bearer Token ✅

**Path Parameter:**

| Parameter | Type   | Required | Keterangan                     |
|-----------|--------|----------|--------------------------------|
| `id`      | string | ✅        | UUID receipt hasil OCR         |

**Request Body:**
```json
{
  "store_name": "Baji Cafe",
  "receipt_date": "2026-05-20T00:00:00.000Z",
  "subtotal": 300000,
  "tax": 0,
  "discount": 0,
  "total": 300000,
  "source": "manual",
  "items": [
    {
      "item_name": "Avocado Toast",
      "qty": 1,
      "unit_price": 300000,
      "total_price": 300000
    }
  ]
}
```

> Data yang dikirim adalah hasil koreksi / konfirmasi dari hasil OCR. Field sama dengan Catat Struk Manual.

**Response 200:**
```json
{
  "status": "success",
  "message": "Struk OCR berhasil dikonfirmasi dan dicatat",
  "data": {
    "receiptId": "74bf8cee-95bb-4b34-9419-a33515f9acf3",
    "store_name": "Baji Cafe",
    "total": 300000,
    "confirmedAt": "2026-05-25T11:00:00.000Z"
  }
}
```

---

#### Detail Struk (dari OCR)

```
GET /api/finance/receipts/28e6459b-570b-4136-8a72-7df224506693
```

> Sama dengan endpoint Detail Struk di Receipts Manual.

---

#### Histori Pengeluaran (dari OCR)

```
GET /api/finance/transactions
```

> Sama dengan endpoint histori transaksi global.

---

#### Hapus Pengeluaran (dari OCR)

```
DELETE /api/finance/transactions/6318a378-96fa-4897-a4ea-29ea03443d29
```

> Sama dengan endpoint hapus transaksi global.

---

### 4.5 Tabungan

#### Buat Saving Goal

```
POST /api/finance/saving-goals
```

**Auth:** Bearer Token ✅

**Request Body:**
```json
{
  "goal_name": "Beli Laptop",
  "target_amount": 15000000,
  "saving_frequency": "monthly",
  "saving_amount": 3000000
}
```

| Field              | Type   | Required | Keterangan                                            |
|--------------------|--------|----------|-------------------------------------------------------|
| `goal_name`        | string | ✅        | Nama tujuan tabungan                                  |
| `target_amount`    | number | ✅        | Target nominal yang ingin dicapai                     |
| `saving_frequency` | string | ✅        | Frekuensi: `"daily"` / `"weekly"` / `"monthly"`       |
| `saving_amount`    | number | ✅        | Jumlah yang disisihkan per frekuensi                  |

**Response 201:**
```json
{
  "status": "success",
  "message": "Saving goal berhasil dibuat",
  "data": {
    "goalId": "a9dabe68-c604-4444-a544-9b0d04e0dd2c",
    "goal_name": "Beli Laptop",
    "target_amount": 15000000,
    "current_amount": 0,
    "saving_frequency": "monthly",
    "saving_amount": 3000000,
    "createdAt": "2026-05-25T10:00:00.000Z"
  }
}
```

---

#### Tambah Dana ke Saving Goal

```
POST /api/finance/saving-goals/:id/add-money
```

**Auth:** Bearer Token ✅

**Path Parameter:**

| Parameter | Type   | Required | Keterangan            |
|-----------|--------|----------|-----------------------|
| `id`      | string | ✅        | UUID saving goal      |

**Request Body:**
```json
{
  "amount": 2500000,
  "note": "Uang arisan"
}
```

| Field    | Type   | Required | Keterangan                   |
|----------|--------|----------|------------------------------|
| `amount` | number | ✅        | Nominal yang ditambahkan     |
| `note`   | string | ❌        | Catatan sumber dana          |

**Response 200:**
```json
{
  "status": "success",
  "message": "Dana berhasil ditambahkan ke saving goal",
  "data": {
    "goalId": "a9dabe68-c604-4444-a544-9b0d04e0dd2c",
    "goal_name": "Beli Laptop",
    "target_amount": 15000000,
    "current_amount": 2500000,
    "remaining_amount": 12500000,
    "note": "Uang arisan",
    "updatedAt": "2026-05-25T12:00:00.000Z"
  }
}
```

---

#### Lihat Semua Saving Goals

```
GET /api/finance/saving-goals
```

**Auth:** Bearer Token ✅

**Response 200:**
```json
{
  "status": "success",
  "data": [
    {
      "goalId": "a9dabe68-c604-4444-a544-9b0d04e0dd2c",
      "goal_name": "Beli Laptop",
      "target_amount": 15000000,
      "current_amount": 2500000,
      "saving_frequency": "monthly",
      "saving_amount": 3000000,
      "createdAt": "2026-05-25T10:00:00.000Z"
    }
  ]
}
```

---

#### Edit Saving Goal

```
PUT /api/finance/saving-goals/a9dabe68-c604-4444-a544-9b0d04e0dd2c
```

**Auth:** Bearer Token ✅

**Path Parameter:**

| Parameter | Type   | Required | Keterangan               |
|-----------|--------|----------|--------------------------|
| `id`      | string | ✅        | UUID saving goal         |

**Request Body:**
```json
{
  "goal_name": "Beli Laptop",
  "target_amount": 15000000,
  "saving_frequency": "monthly",
  "saving_amount": 3000000
}
```

**Response 200:**
```json
{
  "status": "success",
  "message": "Saving goal berhasil diperbarui",
  "data": {
    "goalId": "a9dabe68-c604-4444-a544-9b0d04e0dd2c",
    "goal_name": "Beli Laptop",
    "target_amount": 15000000,
    "saving_frequency": "monthly",
    "saving_amount": 3000000,
    "updatedAt": "2026-05-25T13:00:00.000Z"
  }
}
```

---

#### Hapus Saving Goal

```
DELETE /api/finance/saving-goals/29f5ae12-0b2d-4fcb-80f6-f52e6a906b42
```

**Auth:** Bearer Token ✅

**Path Parameter:**

| Parameter | Type   | Required | Keterangan               |
|-----------|--------|----------|--------------------------|
| `id`      | string | ✅        | UUID saving goal         |

**Response 200:**
```json
{
  "status": "success",
  "message": "Saving goal berhasil dihapus"
}
```

---

#### Budget Summary

```
GET /api/finance/budget/summary
```

**Auth:** Bearer Token ✅

**Response 200:**
```json
{
  "status": "success",
  "data": {
    "total_income": 10000000,
    "alloc_kebutuhan_primer": 5000000,
    "alloc_kebutuhan_sekunder": 3000000,
    "alloc_dana_darurat": 1000000,
    "alloc_tabungan": 1000000,
    "spent_kebutuhan_primer": 2500000,
    "spent_kebutuhan_sekunder": 150000,
    "spent_dana_darurat": 0,
    "remaining_kebutuhan_primer": 2500000,
    "remaining_kebutuhan_sekunder": 2850000,
    "remaining_dana_darurat": 1000000,
    "period": "2026-05"
  }
}
```

---

## 5. Analytics

### Data Keuangan (Summary)

```
GET /api/analytics/summary
```

**Auth:** Bearer Token ✅

**Response 200:**
```json
{
  "status": "success",
  "data": {
    "total_income": 10000000,
    "total_expense": 650000,
    "total_saving": 2500000,
    "net_balance": 9350000,
    "period": "2026-05"
  }
}
```

---

### Skor Kesehatan Keuangan

```
GET /api/analytics/health
```

**Auth:** Bearer Token ✅

**Response 200:**
```json
{
  "status": "success",
  "data": {
    "health_score": 82,
    "category": "Sehat",
    "details": {
      "saving_ratio": 0.25,
      "expense_ratio": 0.065,
      "emergency_fund_ratio": 0.1
    },
    "recommendation": "Keuangan Anda dalam kondisi baik. Pertahankan konsistensi tabungan."
  }
}
```

---

### Recent Transactions

```
GET /api/analytics/recent
```

**Auth:** Bearer Token ✅

**Response 200:**
```json
{
  "status": "success",
  "data": [
    {
      "transactionId": "6318a378-96fa-4897-a4ea-29ea03443d29",
      "type": "expense",
      "amount": 150000,
      "name": "Beli Kopi dan Cemilan",
      "parent_category": "kebutuhan_sekunder",
      "transaction_date": "2026-05-25T10:00:00.000Z"
    }
  ]
}
```

---

### AI Insight

```
GET /api/analytics/insight
```

**Auth:** Bearer Token ✅

**Response 200:**
```json
{
  "status": "success",
  "data": {
    "insights": [
      {
        "type": "warning",
        "title": "Pengeluaran Sekunder Meningkat",
        "description": "Pengeluaran kebutuhan sekunder Anda minggu ini meningkat 30% dibanding rata-rata bulan lalu.",
        "suggestion": "Pertimbangkan untuk mengurangi pengeluaran non-esensial seperti kopi dan hiburan."
      },
      {
        "type": "positive",
        "title": "Tabungan On Track",
        "description": "Saving goal 'Beli Laptop' sudah mencapai 16.67% dari target.",
        "suggestion": "Pertahankan konsistensi menabung setiap bulan."
      }
    ],
    "generated_at": "2026-05-25T10:00:00.000Z"
  }
}
```

---

## 6. Aggregator

### Dashboard

```
GET /api/aggregator/dashboard
```

**Auth:** Bearer Token ✅

**Response 200:**
```json
{
  "status": "success",
  "data": {
    "user": {
      "name": "Abdurrahman",
      "email": "user@example.com"
    },
    "finance_summary": {
      "total_income": 10000000,
      "total_expense": 650000,
      "total_saving": 2500000,
      "net_balance": 9350000
    },
    "budget": {
      "kebutuhan_primer": {
        "allocated": 5000000,
        "spent": 2500000,
        "remaining": 2500000
      },
      "kebutuhan_sekunder": {
        "allocated": 3000000,
        "spent": 150000,
        "remaining": 2850000
      },
      "dana_darurat": {
        "allocated": 1000000,
        "spent": 0,
        "remaining": 1000000
      }
    },
    "saving_goals": [
      {
        "goalId": "a9dabe68-c604-4444-a544-9b0d04e0dd2c",
        "goal_name": "Beli Laptop",
        "target_amount": 15000000,
        "current_amount": 2500000,
        "progress_percent": 16.67
      }
    ],
    "recent_transactions": [
      {
        "transactionId": "6318a378-96fa-4897-a4ea-29ea03443d29",
        "name": "Beli Kopi dan Cemilan",
        "amount": 150000,
        "transaction_date": "2026-05-25T10:00:00.000Z"
      }
    ],
    "health_score": 82,
    "period": "2026-05"
  }
}
```

---

## Referensi Cepat — Seluruh Endpoint

| Method   | Endpoint                                         | Keterangan                         | Auth |
|----------|--------------------------------------------------|------------------------------------|------|
| GET      | `/health`                                        | Health Gateway                     | ❌    |
| GET      | `/health/auth`                                   | Health Auth Service                | ❌    |
| GET      | `/health/aggregator`                             | Health Aggregator Service          | ❌    |
| GET      | `/health/finance`                                | Health Finance Service             | ❌    |
| GET      | `/health/analytics`                              | Health Analytics Service           | ❌    |
| POST     | `/api/auth/login`                                | Login dengan Email                 | ❌    |
| POST     | `/api/auth/google`                               | Login / Register via Google        | ❌    |
| POST     | `/api/auth/logout`                               | Logout                             | ✅    |
| POST     | `/api/auth/register`                             | Register dengan Email              | ❌    |
| GET      | `/api/auth/verify-email`                         | Verifikasi Email                   | ❌    |
| POST     | `/api/auth/resend-verification`                  | Kirim ulang email verifikasi       | ❌    |
| POST     | `/api/auth/forgot-password`                      | Lupa password                      | ❌    |
| POST     | `/api/auth/reset-password`                       | Reset password                     | ❌    |
| POST     | `/api/auth/refresh`                              | Refresh token                      | ❌    |
| GET      | `/api/auth/profile`                              | Get profil user                    | ✅    |
| PUT      | `/api/auth/profile/password`                     | Ganti password                     | ✅    |
| DELETE   | `/api/auth/profile`                              | Hapus akun                         | ✅    |
| POST     | `/api/finance/incomes`                           | Catat pemasukan                    | ✅    |
| GET      | `/api/finance/incomes`                           | Lihat daftar pemasukan             | ✅    |
| PUT      | `/api/finance/incomes/:id`                       | Edit pemasukan                     | ✅    |
| DELETE   | `/api/finance/incomes/:id`                       | Hapus pemasukan                    | ✅    |
| POST     | `/api/finance/transactions`                      | Catat pengeluaran (quick input)    | ✅    |
| GET      | `/api/finance/transactions`                      | Histori transaksi                  | ✅    |
| PUT      | `/api/finance/transactions/:id`                  | Edit transaksi                     | ✅    |
| DELETE   | `/api/finance/transactions/:id`                  | Hapus transaksi                    | ✅    |
| POST     | `/api/finance/receipts/manual`                   | Catat struk manual                 | ✅    |
| GET      | `/api/finance/receipts/:id`                      | Detail struk                       | ✅    |
| POST     | `/api/finance/receipts/ocr`                      | Upload & proses struk OCR          | ✅    |
| POST     | `/api/finance/receipts/:id/confirm`              | Konfirmasi hasil OCR               | ✅    |
| POST     | `/api/finance/saving-goals`                      | Buat saving goal                   | ✅    |
| GET      | `/api/finance/saving-goals`                      | Lihat semua saving goals           | ✅    |
| PUT      | `/api/finance/saving-goals/:id`                  | Edit saving goal                   | ✅    |
| DELETE   | `/api/finance/saving-goals/:id`                  | Hapus saving goal                  | ✅    |
| POST     | `/api/finance/saving-goals/:id/add-money`        | Tambah dana ke saving goal         | ✅    |
| GET      | `/api/finance/budget/summary`                    | Budget summary                     | ✅    |
| GET      | `/api/analytics/summary`                         | Data keuangan ringkas              | ✅    |
| GET      | `/api/analytics/health`                          | Skor kesehatan keuangan            | ✅    |
| GET      | `/api/analytics/recent`                          | Transaksi terbaru                  | ✅    |
| GET      | `/api/analytics/insight`                         | AI Insight keuangan                | ✅    |
| GET      | `/api/aggregator/dashboard`                      | Dashboard agregat lengkap          | ✅    |

---

*FAST API Documentation — v1.0.0 | Last updated: 2026-05-25*
