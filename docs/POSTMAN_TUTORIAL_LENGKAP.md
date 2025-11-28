# 🎓 TUTORIAL LENGKAP: Postman Testing untuk Food Delivery System

## Daftar Isi
1. [Setup Awal](#1-setup-awal)
2. [Import Collection](#2-import-collection)
3. [Setup Environment](#3-setup-environment)
4. [Run Tests Step-by-Step](#4-run-tests-step-by-step)
5. [Troubleshooting](#5-troubleshooting)
6. [Expected Results](#6-expected-results)

---

## 1️⃣ Setup Awal

### Pastikan semua services running:

**Terminal 1 - API Gateway (port 5000):**
```powershell
cd c:\xampp\htdocs\food_delivery_system\microservices\api-gateway
python app.py
```

**Terminal 2 - Service Template (port 5001):**
```powershell
cd c:\xampp\htdocs\food_delivery_system\microservices\service-template
python app.py
```

**Terminal 3+ - Services lainnya (5002, 5003, 5004, 5005)** - sesuai dengan anggota tim

---

## 2️⃣ Import Collection

### Langkah A: Buka Postman
```
1. Klik aplikasi Postman (atau buka https://www.postman.com/downloads/)
2. Login dengan akun Postman Anda
3. Biarkan loading selesai
```

### Langkah B: Import File Collection
```
1. Di sidebar KIRI atas, cari button "Import"
2. Klik "Import" 
3. Pilih tab "File" atau drag-and-drop
4. Browse ke file:
   📁 c:\xampp\htdocs\food_delivery_system\docs\POSTMAN_COLLECTION_LENGKAP.json
5. Klik "Import"
```

### Langkah C: Verifikasi Import Berhasil
```
Setelah import, di sidebar KIRI Anda akan melihat:

📁 Food Delivery System - Complete Testing Collection
   ├── 1. SETUP - Login & Authentication
   ├── 👤 2. USER SERVICE (ARTHUR - Port 5001)
   ├── 🍽️ 3. RESTAURANT SERVICE (Rizki - Port 5002)
   ├── 4. ORDER SERVICE (Nadia - Port 5003)
   ├── 🚚 5. DELIVERY SERVICE (Aydin - Port 5004)
   ├── 💳 6. PAYMENT SERVICE (Reza - Port 5005)
   └── 7. ERROR HANDLING TESTS
```

---

## 3️⃣ Setup Environment

### Langkah A: Buat Environment Baru
```
1. Di sidebar KIRI, cari tab "Environments"
2. Klik "+" atau button "Create Environment"
3. Beri nama: "Food Delivery - Development"
4. Klik "Create"
```

### Langkah B: Set Variables
Masukkan variable berikut dengan Initial Value:

| Variable | Initial Value |
|----------|---|
| base_url | http://localhost:5000 |
| admin_token | (kosong - akan auto-filled saat login) |
| user_token | (kosong) |
| user_id | (kosong) |
| restaurant_id | (kosong) |
| order_id | (kosong) |
| delivery_id | (kosong) |
| payment_id | (kosong) |

### Langkah C: Select Environment
```
1. Di TOP-RIGHT Postman, cari dropdown "No Environment"
2. Pilih "Food Delivery - Development"
3. Pastikan environment name muncul di dropdown (sudah active)
```

---

## 4️⃣ Run Tests Step-by-Step

### FLOW REKOMENDASI:

#### **STEP 1: Setup & Login** 
```
Folder: "1. SETUP - Login & Authentication"

Jalankan dalam urutan:
1. "Health Check - API Gateway"
   → Expected: 200 OK, status: "healthy"

2. "🔓 POST - Login Admin"
   → Expected: 200 OK
   → Lihat response → copy access_token
   → Token otomatis tersimpan di variable admin_token 
   → Cek di "Environments" → admin_token sudah terisi

3. "🔓 POST - Login User"
   → Expected: 200 OK
   → user_token tersimpan otomatis
```

#### **STEP 2: Health Check Semua Services** 
```
Jalankan health check di setiap folder:

Folder "2. USER SERVICE":
   → "Health Check" → Expected: 200

Folder "3. RESTAURANT SERVICE":
   → "Health Check" → Expected: 200

Folder "4. ORDER SERVICE":
   → "Health Check" → Expected: 200

Folder "5. DELIVERY SERVICE":
   → "Health Check" → Expected: 200

Folder "6. PAYMENT SERVICE":
   → "Health Check" → Expected: 200

Jika ada yang gagal (tidak 200), service tersebut belum running!
```

#### **STEP 3: User Service Testing** 👤
```
Folder: "2. USER SERVICE (ARTHUR - Port 5001)"

Urutan:
1. "GET - All Users"
   → Klik "Send"
   → Expected: 200 OK
   → Lihat response array users

2. "➕ POST - Create User"
   → Klik "Send"
   → Expected: 201 Created
   → Lihat ID user baru
   → PENTING: user_id OTOMATIS TERSIMPAN di environment!

3. "GET - User by ID"
   → Klik "Send"
   → Expected: 200 OK
   → Verify data sesuai yang dibuat sebelumnya

4. "✏️ PUT - Update User"
   → Klik "Send"
   → Expected: 200 OK
   → Name berubah dari "User Baru" → "User Updated"

5. "🗑️ DELETE - Soft Delete User"
   → Klik "Send"
   → Expected: 200 OK
   → is_deleted: true dalam response
```

#### **STEP 4: Restaurant Service Testing** 🍽️
```
Folder: "3. RESTAURANT SERVICE (Rizki - Port 5002)"

Urutan:
1. "GET - All Restaurants"
   → Expected: 200 OK

2. "➕ POST - Create Restaurant"
   → Expected: 201 Created
   → restaurant_id tersimpan otomatis
```

#### **STEP 5: Order Service Testing** 
```
Folder: "4. ORDER SERVICE (Nadia - Port 5003)"

Urutan:
1. "GET - All Orders"
   → Expected: 200 OK

2. "➕ POST - Create Order"
   → Expected: 201 Created
   → order_id tersimpan otomatis
```

#### **STEP 6: Delivery Service Testing** 🚚
```
Folder: "5. DELIVERY SERVICE (Aydin - Port 5004)"

Urutan:
1. "GET - All Deliveries"
   → Expected: 200 OK

2. "GET - All Couriers"
   → Expected: 200 OK
   → Lihat sample couriers yang dibuat

3. "➕ POST - Create Delivery"
   → Expected: 201 Created
   → delivery_id tersimpan otomatis
```

#### **STEP 7: Payment Service Testing** 💳
```
Folder: "6. PAYMENT SERVICE (Reza - Port 5005)"

Urutan:
1. "GET - All Payments"
   → Expected: 200 OK

2. "➕ POST - Create Payment"
   → Expected: 201 Created
   → payment_id tersimpan otomatis
```

#### **STEP 8: Error Handling Testing** 
```
Folder: "7. ERROR HANDLING TESTS"

1. "GET - Invalid Endpoint"
   → Expected: 404 Not Found

2. "POST - Missing Required Field"
   → Expected: 400 Bad Request

3. "GET - Non-existent Resource"
   → Expected: 404 Not Found
```

---

## 5️⃣ Troubleshooting

### Problem: "Connection refused" atau "Couldn't connect"
```
Solusi:
1. Pastikan API Gateway running di port 5000
2. Buka terminal dan cek: curl http://localhost:5000/health
3. Jika error, restart API Gateway
4. Check variable base_url benar: http://localhost:5000 (tanpa trailing /)
```

### Problem: "Unauthorized" atau "401 Token missing"
```
Solusi:
1. Jalankan dulu "🔓 POST - Login Admin" 
2. Check response ada access_token
3. Pastikan environment "Food Delivery - Development" sudah ACTIVE
4. Refresh page Postman (Ctrl+Shift+R)
5. Re-run login jika token expired
```

### Problem: Service tidak merespon (gateway 503 Service Unavailable)
```
Solusi:
1. Pastikan service target sudah running:
   - Port 5001: user-service (Arthur)
   - Port 5002: restaurant-service (Rizki)
   - Port 5003: order-service (Nadia)
   - Port 5004: delivery-service (Aydin)
   - Port 5005: payment-service (Reza)
2. Check port tidak konflik (lakukan: netstat -an | findstr :5001)
3. Restart service yang tidak running
```

### Problem: Variables kosong (user_id, restaurant_id, dll)
```
Solusi:
1. Variables otomatis di-set oleh test scripts setelah create
2. Pastikan folder "Environments" terbuka untuk lihat variable
3. Manual set jika perlu: klik variable → edit → set value
```

### Problem: "Database error" atau "Integrity error"
```
Solusi:
1. Hapus database file jika ada di service
   - c:\xampp\htdocs\food_delivery_system\microservices\[service]\database.db
2. Restart service untuk recreate database
3. Re-run tests
```

---

## 6️⃣ Expected Results

### Jika semua berjalan lancar:

```
TEST SUMMARY:

Authentication:
   - Login Admin: 200 + token
   - Login User: 200 + token

User Service:
   - Health: 200
   - Get All: 200 + array users
   - Create: 201 + new user
   - Get One: 200 + user data
   - Update: 200 + updated data
   - Soft Delete: 200 + is_deleted: true

Restaurant Service:
   - Health: 200
   - Get All: 200
   - Create: 201 + new restaurant

Order Service:
   - Health: 200
   - Get All: 200
   - Create: 201 + new order

Delivery Service:
   - Health: 200
   - Get Deliveries: 200 + array
   - Get Couriers: 200 + sample couriers
   - Create Delivery: 201 + new delivery

Payment Service:
   - Health: 200
   - Get All: 200
   - Create: 201 + new payment

Error Handling:
   - Invalid endpoint: 404
   - Missing field: 400
   - Non-existent: 404

TOTAL: 95-100% tests passing
```

### 📈 Metrics yang diharapkan:
- **Total Tests:** 30+
- **Success Rate:** 95-100%
- **Failed:** 0-1
- **Response Time:** < 500ms per request

---

## CHECKLIST SEBELUM SUBMIT

Pastikan Anda sudah:

- [ ] Semua health check 200
- [ ] Login admin & user berhasil
- [ ] Semua CRUD (Create, Read, Update, Delete) working
- [ ] Variable otomatis ter-fill (user_id, restaurant_id, dll)
- [ ] Error handling test working (404, 400, dll)
- [ ] Tidak ada "Connection refused" error
- [ ] Database consistent (data terekspor dengan benar)
- [ ] Screenshot hasil tests untuk dokumentasi

---

## Advanced Tips

### 1. Run Entire Collection Sekaligus
```
1. Right-click collection name
2. Pilih "Run collection"
3. Configure:
   - Environment: "Food Delivery - Development"
   - Iterations: 1
   - Delay: 100ms (untuk avoid rate limiting)
4. Klik "Run [Collection]"
5. Lihat hasil di Collection Runner
```

### 2. Export Test Results
```
1. Setelah run collection selesai
2. Di runner window, cari "Export Results"
3. Save sebagai JSON
4. Bisa di-share atau di-dokumentasikan
```

### 3. Performance Testing
```
1. Set iterations: 10
2. Run collection
3. Monitor response times
4. Identify bottlenecks
```

### 4. Data Persistence Check
```
1. Run collection (iteration 1)
2. Run collection lagi (iteration 2)
3. Verify data konsisten
4. Check no duplicates atau conflicts
```

---

## 📞 Support

Jika ada error yang tidak terselesaikan:

1. **Check logs** di terminal service yang error
2. **Restart service** yang problematic
3. **Clear environment variables** dan login ulang
4. **Delete database files** dan restart (jika perlu reset)
5. **Check port conflicts** dengan `netstat -an | findstr :[port]`

---

**Happy Testing! Semoga semua tests pass!**

