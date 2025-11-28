# Panduan Database & Seed

Proyek ini menggunakan **SQLite** untuk setiap microservice. Database disimpan terpisah pada folder `microservices/<nama-service>/instance/`. Dokumen ini melengkapi requirement tugas terkait _schema_, _seed_, serta cara menjalankannya.

## 📁 Struktur Folder

```
database/
├── README.md
├── schema/
│   ├── user_service.sql
│   ├── restaurant_service.sql
│   ├── order_service.sql
│   ├── delivery_service.sql
│   └── payment_service.sql
└── seed/
    ├── run_seed.py
    ├── user_service_seed.sql (digenerate oleh script)
    └── ...
```

- Direktori `schema/` berisi definisi tabel untuk masing-masing service.
- Script `seed/run_seed.py` otomatis:
  1. Menghapus database lama (jika ada)
  2. Menerapkan schema sesuai service
  3. Mengisi contoh data (_seed_) yang konsisten antar-service.

## Cara Mengimpor Schema & Seed

> **Catatan:** Pastikan semua service dalam keadaan berhenti sebelum menjalankan seeding ulang.

### 1. Aktifkan Virtual Environment (opsional tapi disarankan)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# atau
source venv/bin/activate
```

### 2. Jalankan Script Seed

```bash
python database/seed/run_seed.py
```

Output yang diharapkan:

```
🧹 Menghapus database lama...
🧱 Memuat schema user-service ...
🌱 Menanam data user-service ...
...
Semua database berhasil dibuat ulang dan di-seed!
```

Script akan menghasilkan file SQLite baru di:

- `microservices/user-service/instance/user_service.db`
- `microservices/restaurant-service/instance/restaurant.db`
- `microservices/order-service/instance/order_service.db`
- `microservices/delivery-service/instance/delivery_service.db`
- `microservices/payment-service/instance/payment_service.db`

### 3. Verifikasi (Opsional)

Gunakan perintah berikut untuk mengecek tabel/data:

```bash
sqlite3 microservices/user-service/instance/user_service.db ".tables"
sqlite3 microservices/user-service/instance/user_service.db "SELECT * FROM user;"
```

### 4. Jalankan Service Seperti Biasa

Setelah schema & seed selesai diterapkan, jalankan kembali urutan:

1. API Gateway (`microservices/api-gateway`)
2. Masing-masing service (`user-service` → `payment-service`)
3. Frontend static server

## ℹ️ Informasi Tambahan

- Schema dapat digunakan sebagai referensi dokumentasi migrasi/DDL resmi.
- Jika ingin menambahkan data seed sendiri, cukup edit fungsi di `run_seed.py`.
- Untuk lingkungan production, ganti `sqlite:///...` pada masing-masing `app.py` dengan koneksi RDBMS pilihan (MySQL/PostgreSQL) lalu adaptasikan schema/seed sesuai kebutuhan.

Selamat mencoba! 

