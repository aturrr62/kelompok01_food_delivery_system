# 🍕 Food Delivery System - Kelompok 01

Sistem food delivery berbasis microservices menggunakan Flask dan Python dengan arsitektur modern yang memungkinkan setiap anggota tim mengembangkan service secara independen.

---

## **TEAM ASSIGNMENTS**

| Nama | Port | Service | Jurusan | 
|------|------|---------|---------|
| **ARTHUR** | 5001 | User Service | Informatics |
| **rizki** | 5002 | Restaurant Service | Informatics |
| **Nadia** | 5003 | Order Service | Informatics |
| **aydin** | 5004 | Delivery Service | Informatics |
| **reza** | 5005 | Payment Service | Informatics |

---

## 📁 **STRUKTUR PROJECT LENGKAP**

```
food_delivery_system/
├── frontend/                      # Frontend web application
│   ├── index.html                # Halaman utama
│   ├── restaurant.html           # Halaman restaurant
│   ├── cart.html                 # Halaman keranjang
│   ├── checkout.html             # Halaman checkout
│   ├── order-tracking.html       # Halaman tracking order
│   ├── admin.html                # Halaman admin
│   └── js/                       # JavaScript modules
│       ├── main.js               # Main JavaScript file
│       ├── home.js               # Home page logic
│       ├── restaurant.js         # Restaurant page logic
│       ├── cart.js               # Cart page logic
│       ├── checkout.js           # Checkout page logic
│       ├── order-tracking.js     # Order tracking logic
│       └── admin.js              # Admin page logic
│
├── microservices/                # Backend microservices
│   ├── api-gateway/              # API Gateway (Port 5000)
│   │   ├── app.py                # Flask app untuk routing
│   │   ├── requirements.txt      # Dependencies
│   │   └── run.sh               # Run script
│   │
│   ├── service-template/         # Template untuk service baru
│   │   ├── app.py                # Template Flask app
│   │   ├── requirements.txt      # Dependencies
│   │   ├── run.sh               # Run script
│   │   └── README.md            # Template documentation
│   │
│   ├── user-service/             # 👤 ARTHUR (5001)
│   │   ├── app.py                # User management & auth
│   │   ├── requirements.txt      # Dependencies
│   │   └── run.sh               # Run script
│   │
│   ├── restaurant-service/       # 🍽️ rizki (5002)
│   │   ├── app.py                # Restaurant & menu management
│   │   ├── requirements.txt      # Dependencies
│   │   └── run.sh               # Run script
│   │
│   ├── order-service/            # Nadia (5003)
│   │   ├── app.py                # Order management
│   │   ├── requirements.txt      # Dependencies
│   │   └── run.sh               # Run script
│   │
│   ├── delivery-service/         # 🚚 aydin (5004)
│   │   ├── app.py                # Delivery tracking
│   │   ├── requirements.txt      # Dependencies
│   │   └── run.sh               # Run script
│   │
│   └── payment-service/          # 💳 reza (5005)
│       ├── app.py                # Payment processing
│       ├── requirements.txt      # Dependencies
│       └── run.sh               # Run script
│
├── scripts/                      # Utility scripts
│   ├── setup.sh                 # Setup environment
│   └── run-all.sh               # Start all services
│
├── logs/                        # Log files (auto-generated)
│   ├── gateway.log             # API Gateway logs
│   └── service-*.log           # Individual service logs
│
├── .gitignore                   # Git ignore file
└── README.md                    # 📖 This file
```

---

## 🧱 **Arsitektur Sistem**

```
Frontend (HTML/JS @8080)
        │ fetch API
        ▼
API Gateway (Flask @5000, JWT, Swagger)
        │ routing per prefix
        ▼
Microservices (Flask @5001-5005)
        │ SQLAlchemy ORM
        ▼
SQLite Database per service
```

Gateway menerima seluruh request dari frontend → memvalidasi token/headers → meneruskan ke service berdasarkan prefix (`/users`, `/restaurants`, dst). Setiap service bertanggung jawab penuh atas database-nya sendiri, sehingga tim dapat bekerja paralel.

---

## **Konfigurasi ENV & Port**

| Komponen | Port Default | ENV Penting | Keterangan |
|----------|--------------|-------------|------------|
| Frontend Static | 8080 | `API_GATEWAY` (di `frontend/js/main.js`) | Mengarah ke gateway `http://localhost:5000` |
| API Gateway | 5000 | `JWT_SECRET_KEY`, `GATEWAY_PORT` | JWT + proxy ke service |
| User Service | 5001 | `SQLALCHEMY_DATABASE_URI=sqlite:///user_service.db` | Manajemen user/auth |
| Restaurant Service | 5002 | `SQLALCHEMY_DATABASE_URI=sqlite:///restaurant.db` | Restoran & menu |
| Order Service | 5003 | `SQLALCHEMY_DATABASE_URI=sqlite:///order_service.db` | Order + history |
| Delivery Service | 5004 | `SQLALCHEMY_DATABASE_URI=sqlite:///delivery_service.db` | Kurir & tracking |
| Payment Service | 5005 | `SQLALCHEMY_DATABASE_URI=sqlite:///payment_service.db` | Pembayaran & refund |

> Set `JWT_SECRET_KEY` sesuai kebutuhan produksi (`set JWT_SECRET_KEY=...` di PowerShell / `export JWT_SECRET_KEY=...` di Unix).

---

## ▶️ **Urutan Start (Gateway → Services → Frontend)**

1. **API Gateway**
   ```bash
   cd microservices/api-gateway
   python app.py
   ```
2. **Microservices (5001-5005)** — masing-masing di terminal berbeda:
   ```bash
   cd microservices/user-service      && python app.py
   cd microservices/restaurant-service && python app.py
   cd microservices/order-service      && python app.py
   cd microservices/delivery-service   && python app.py
   cd microservices/payment-service    && python app.py
   ```
3. **Frontend Static Server**
   ```bash
   cd frontend
   python -m http.server 8080   # atau gunakan npm serve
   ```
4. **Akses**
   - Frontend konsumen: `http://localhost:8080`
   - API Gateway: `http://localhost:5000`
   - Swagger: `http://localhost:5000/api-docs/`

Pastikan langkah 1-2 selesai sebelum membuka frontend agar semua fetch ke gateway berhasil.

---

## **Ringkasan Endpoint & Dokumentasi**

| Service | Prefix Gateway | Contoh Endpoint | Dokumentasi |
|---------|----------------|-----------------|-------------|
| API Gateway | `/` | `GET /health`, `POST /auth/login` | Swagger UI (`/api-docs`), `docs/openapi-spec-api-gateway.yaml` |
| User | `/api/user-service` | `GET /api/user-service/api/users` | Swagger + Postman |
| Restaurant | `/api/restaurant-service` | `GET /api/restaurant-service/api/restaurants` | Swagger + Postman |
| Order | `/api/order-service` | `POST /api/order-service/api/orders` | Swagger + Postman |
| Delivery | `/api/delivery-service` | `GET /api/delivery-service/api/deliveries` | Swagger + Postman |
| Payment | `/api/payment-service` | `POST /api/payment-service/api/payments` | Swagger + Postman |

Detail lengkap (cara akses Swagger, cara import Postman, dsb) tersedia di `docs/api/README.md`. Sertakan juga environment `docs/POSTMAN_ENVIRONMENT.json` saat testing.

---

## **QUICK START GUIDE**

### **Langkah 1: Setup Environment**
```bash
# Clone repository (jika belum)
git clone https://github.com/aturrr62/kelompok01_food_delivery_system
cd food-delivery-system

# Setup environment (jalanin di root directory)
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### **Langkah 2: Jalankan System**
```bash
# Mulai API Gateway dulu
./scripts/run-all.sh

# 🚨 IMPORTANT: Setiap anggota tim jalankan service mereka masing-masing:
```

---

## 👥 **PANDUAN UNTUK SETIAP ANGGOTA TIM**

### 🔵 **ARTHUR (5001) - User Service**
```bash
# Buka terminal baru, jalankan:
cd microservices/user-service
python app.py

# Service akan berjalan di: http://localhost:5001
# API akan tersedia di: http://localhost:5000/users/*
```

**Fungsi User Service:**
- User registration & login
- Profile management
- Authentication & authorization
- User preferences

---

### 🟢 **rizki (5002) - Restaurant Service**
```bash
# Buka terminal baru, jalankan:
cd microservices/restaurant-service
python app.py

# Service akan berjalan di: http://localhost:5002
# API akan tersedia di: http://localhost:5000/restaurants/*
```

**Fungsi Restaurant Service:**
- Restaurant registration & management
- Menu management
- Restaurant categories
- Operating hours & location

---

### 🟡 **Nadia (5003) - Order Service**
```bash
# Buka terminal baru, jalankan:
cd microservices/order-service
python app.py

# Service akan berjalan di: http://localhost:5003
# API akan tersedia di: http://localhost:5000/orders/*
```

**Fungsi Order Service:**
- Order creation & management
- Order tracking
- Order history
- Order status updates

---

### 🟠 **aydin (5004) - Delivery Service**
```bash
# Buka terminal baru, jalankan:
cd microservices/delivery-service
python app.py

# Service akan berjalan di: http://localhost:5004
# API akan tersedia di: http://localhost:5000/deliveries/*
```

**Fungsi Delivery Service:**
- Delivery assignment
- Driver tracking
- Real-time location updates
- Delivery status

---

### 🔴 **reza (5005) - Payment Service**
```bash
# Buka terminal baru, jalankan:
cd microservices/payment-service
python app.py

# Service akan berjalan di: http://localhost:5005
# API akan tersedia di: http://localhost:5000/payments/*
```

**Fungsi Payment Service:**
- Payment processing
- Transaction management
- Payment history
- Refund handling

---

## **ACCESS POINTS**

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:8080 | Web Interface (static server) |
| **API Gateway** | http://localhost:5000/health | Health Check |
| **User Service** | http://localhost:5001 | ARTHUR |
| **Restaurant Service** | http://localhost:5002 | rizki |
| **Order Service** | http://localhost:5003 | Nadia |
| **Delivery Service** | http://localhost:5004 | aydin |
| **Payment Service** | http://localhost:5005 | reza |

---

## **API ROUTING**

API Gateway akan me-route request berdasarkan URL pattern:

- `GET/POST /users/*` → User Service (ARTHUR)
- `GET/POST /restaurants/*` → Restaurant Service (rizki)  
- `GET/POST /orders/*` → Order Service (Nadia)
- `GET/POST /deliveries/*` → Delivery Service (aydin)
- `GET/POST /payments/*` → Payment Service (reza)

---

## **DEVELOPMENT GUIDE**

### **Membuat Service Baru:**
1. Copy `microservices/service-template/` folder
2. Rename sesuai nama service
3. Ubah port di `app.py` (line 73)
4. Modifikasi model di `app.py` (line 13-25)
5. Ubah endpoint dan nama service
6. Update `requirements.txt` jika perlu dependencies tambahan

### **Service Requirements:**
Setiap service WAJIB memiliki:
- Endpoint `/health` untuk health check
- Menggunakan port yang sudah ditentukan
- Database model dengan method `to_dict()`
- CRUD endpoints (GET, POST, PUT, DELETE)
- Error handling yang proper
- Logging yang informatif

---

## 🚨 **TROUBLESHOOTING**

### **Port sudah digunakan:**
```bash
# Cari process yang menggunakan port
lsof -i :5001  # Ganti dengan port yang bermasalah

# Hentikan process
kill -9 <PID>
```

### **Database error:**
```bash
# Hapus database lama dan buat ulang
rm -f microservices/*/database.db
python app.py  # di masing-masing service
```

### **Dependencies error:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## **HEALTH CHECK**

Untuk mengecek semua service berfungsi:
```bash
# Cek API Gateway
curl http://localhost:5000/health

# Cek semua service
for port in 5001 5002 5003 5004 5005; do
  echo "Checking port $port:"
  curl http://localhost:$port/health
  echo ""
done
```

---

## **Database & Seed**

- **DB yang dipakai:** SQLite (1 file per service pada `microservices/<service>/instance/`).
- **Schema resmi:** `database/schema/*.sql`.
- **Seed otomatis:** jalankan `python database/seed/run_seed.py` untuk:
  1. Menghapus file database lama
  2. Menerapkan schema sesuai service
  3. Mengisi data contoh (user admin/customer, restoran, order, delivery, payment)
- Panduan lengkap + langkah verifikasi tersedia di `database/README.md`.

---

## **Frontend Build & Run**

1. Pastikan gateway + seluruh service (5000-5005) berjalan.
2. Jalankan server statis:
   ```bash
   cd frontend
   python -m http.server 8080   # atau gunakan npx serve .
   ```
3. Akses `http://localhost:8080`. Frontend akan memanggil gateway (`API_GATEWAY = http://localhost:5000`) sehingga tidak ada request langsung ke microservice.

---

## 🎥 **Video Demo & Bukti Pengujian**

- Simpan URL video demo (≤10 menit) pada `video/link.txt`. Pastikan video menampilkan arsitektur, proses run (gateway → services → frontend), demo inter-service via gateway, dokumentasi API, dan frontend.
- Letakkan screenshot bukti Swagger/Postman/health ke folder `evidence/` dengan nama file sesuai daftar pada `evidence/README.md`.

---

## 📞 **SUPPORT**

Jika ada masalah:
1. Pastikan semua dependencies terinstall
2. Cek apakah port sudah digunakan
3. Pastikan virtual environment aktif
4. Lihat logs di folder `logs/`
5. Konsultasi dengan tim lain jika perlu integrasi

---

## **FRONTEND PAGES**

Sistem frontend sudah dilengkapi dengan halaman-halaman lengkap:

- **Home Page** (`/`) - Landing page dengan restaurant list
- **Restaurant Page** (`/restaurant`) - Detail restaurant & menu
- **Cart Page** (`/cart`) - Keranjang belanja
- **Checkout Page** (`/checkout`) - Proses pembayaran
- **Order Tracking** (`/order-tracking`) - Tracking status order
- **Admin Panel** (`/admin`) - Panel administrasi

---

**Happy Coding! Semangat buat food delivery system terbaik! **
