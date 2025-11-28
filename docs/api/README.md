# 📖 Dokumentasi API

Semua dokumentasi resmi API ditempatkan di folder `docs/api/` untuk memenuhi requirement tugas.

## 1. Swagger / OpenAPI

- **File spesifikasi:** `docs/openapi-spec-api-gateway.yaml`
- **Swagger UI (saat runtime):** `http://localhost:5000/api-docs/`
- **Endpoint utama yang dicakup:** `/health`, `/services`, `/auth/*`, serta proxy ke seluruh microservice (`/api/user-service/*`, `/api/restaurant-service/*`, dst).

> Jalankan API Gateway terlebih dahulu (`python microservices/api-gateway/app.py`) untuk mengakses Swagger UI.

## 2. Postman Collection

- **Collection:** `docs/POSTMAN_COLLECTION.json`
- **Environment:** `docs/POSTMAN_ENVIRONMENT.json`

Langkah penggunaan:
1. Import `POSTMAN_COLLECTION.json`.
2. Import `POSTMAN_ENVIRONMENT.json`.
3. Pilih environment **Food Delivery - Local**.
4. Jalankan folder sesuai service atau gunakan Collection Runner.

## 3. Ringkasan Endpoint

| Service | Prefix di Gateway | Contoh Endpoint | Dokumentasi |
|---------|------------------|-----------------|-------------|
| User | `/api/user-service` | `GET /api/user-service/api/users` | Swagger & Postman |
| Restaurant | `/api/restaurant-service` | `GET /api/restaurant-service/api/restaurants` | Swagger & Postman |
| Order | `/api/order-service` | `POST /api/order-service/api/orders` | Swagger & Postman |
| Delivery | `/api/delivery-service` | `GET /api/delivery-service/api/deliveries` | Swagger & Postman |
| Payment | `/api/payment-service` | `POST /api/payment-service/api/payments` | Swagger & Postman |

## 4. Cara Menambah Dokumentasi

1. Update file OpenAPI (`openapi-spec-api-gateway.yaml`) bila ada endpoint baru di gateway.
2. Tambahkan contoh request/response baru ke Postman collection & environment.
3. Sertakan catatan perubahan di README utama agar anggota tim lain mengetahui update terbaru.

Selamat menggunakan! 

