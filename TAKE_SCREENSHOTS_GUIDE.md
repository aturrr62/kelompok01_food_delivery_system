# Panduan Lengkap Mengambil Screenshot Bukti Pengujian

## Target: 14 Screenshot yang Diperlukan

### **Kategori A: Health Endpoints (6 files)**
- `health-gateway.png`
- `health-user.png`
- `health-restaurant.png`
- `health-order.png`
- `health-delivery.png`
- `health-payment.png`

### **Kategori B: Swagger UI (6 files)**
- `swagger-api-gateway.png`
- `swagger-user-service.png`
- `swagger-restaurant-service.png`
- `swagger-order-service.png`
- `swagger-delivery-service.png`
- `swagger-payment-service.png`

### **Kategori C: Postman (2 files)**
- `postman-collection-run.png`
- `postman-tests-passed.png`

---

## **STEP-BY-STEP GUIDE**

### **TAHAP 1: Persiapan (15 menit)**

#### 1.1 Jalankan API Gateway
```powershell
# Terminal 1
cd c:\xampp\htdocs\food_delivery_system\microservices\api-gateway
python app.py
```
Tunggu sampai muncul: `Running on http://127.0.0.1:5000`

#### 1.2 Jalankan Semua Microservices (5 Terminal Berbeda)

**Terminal 2 - User Service:**
```powershell
cd c:\xampp\htdocs\food_delivery_system\microservices\user-service
python app.py
```

**Terminal 3 - Restaurant Service:**
```powershell
cd c:\xampp\htdocs\food_delivery_system\microservices\restaurant-service
python app.py
```

**Terminal 4 - Order Service:**
```powershell
cd c:\xampp\htdocs\food_delivery_system\microservices\order-service
python app.py
```

**Terminal 5 - Delivery Service:**
```powershell
cd c:\xampp\htdocs\food_delivery_system\microservices\delivery-service
python app.py
```

**Terminal 6 - Payment Service:**
```powershell
cd c:\xampp\htdocs\food_delivery_system\microservices\payment-service
python app.py
```

**Verifikasi:** Semua service harus running di port masing-masing (5000-5005)

---

### **TAHAP 2: Screenshot Health Endpoints (20 menit)**

#### 2.1 Buka Browser (Chrome/Edge/Firefox)

#### 2.2 Kunjungi URL Berikut dan Screenshot:

**1. API Gateway Health**
- URL: `http://localhost:5000/health`
- Tekan `Windows + Shift + S` untuk screenshot
- Save sebagai: `c:\xampp\htdocs\food_delivery_system\evidence\health-gateway.png`

**2. User Service Health**
- URL: `http://localhost:5001/health`
- Screenshot
- Save sebagai: `evidence\health-user.png`

**3. Restaurant Service Health**
- URL: `http://localhost:5002/health`
- Screenshot
- Save sebagai: `evidence\health-restaurant.png`

**4. Order Service Health**
- URL: `http://localhost:5003/health`
- Screenshot
- Save sebagai: `evidence\health-order.png`

**5. Delivery Service Health**
- URL: `http://localhost:5004/health`
- Screenshot
- Save sebagai: `evidence\health-delivery.png`

**6. Payment Service Health**
- URL: `http://localhost:5005/health`
- Screenshot
- Save sebagai: `evidence\health-payment.png`

#### 2.3 Verifikasi
Pastikan semua screenshot menunjukkan response JSON:
```json
{
  "status": "healthy",
  "service": "xxx-service",
  "timestamp": "..."
}
```

---

### **TAHAP 3: Screenshot Swagger UI (30 menit)**

#### 3.1 API Gateway Swagger

**1. Buka Swagger UI:**
- URL: `http://localhost:5000/api-docs/`
- Tunggu sampai halaman Swagger UI muncul

**2. Screenshot:**
- Pastikan terlihat:
  - Title: "Food Delivery System API Gateway"
  - List endpoints (GET /health, GET /services, POST /auth/login, dll)
  - Schema definitions (jika ada)
- Save sebagai: `evidence\swagger-api-gateway.png`

**3. BONUS Screenshot (Optional tapi bagus):**
- Click salah satu endpoint (misalnya GET /health)
- Click "Try it out"
- Click "Execute"
- Screenshot response
- Save sebagai: `evidence\swagger-api-gateway-tryout.png`

#### 3.2 Microservices Swagger (JIKA ADA)

**Cek apakah setiap microservice punya Swagger UI:**

**User Service:**
- URL: `http://localhost:5001/api-docs/` atau `http://localhost:5001/docs/`
- Jika ada → Screenshot → `evidence\swagger-user-service.png`
- Jika tidak ada → **Buat dokumentasi alternatif** (lihat section dibawah)

**Restaurant Service:**
- URL: `http://localhost:5002/api-docs/`
- Screenshot → `evidence\swagger-restaurant-service.png`

**Order Service:**
- URL: `http://localhost:5003/api-docs/`
- Screenshot → `evidence\swagger-order-service.png`

**Delivery Service:**
- URL: `http://localhost:5004/api-docs/`
- Screenshot → `evidence\swagger-delivery-service.png`

**Payment Service:**
- URL: `http://localhost:5005/api-docs/`
- Screenshot → `evidence\swagger-payment-service.png`

#### 3.3 ALTERNATIF: Jika Microservices Tidak Punya Swagger UI

Jika microservices tidak punya Swagger UI sendiri, **TIDAK MASALAH** karena:
1. API Gateway sudah punya Swagger UI lengkap
2. Semua endpoint microservices accessible via Gateway
3. Postman Collection sudah mendokumentasikan semua endpoint

**Screenshot yang bisa diambil sebagai alternatif:**
- Screenshot endpoint list dari code `app.py` di text editor
- Screenshot response di browser (akses endpoint langsung)
- Screenshot Postman request untuk service tersebut

---

### **TAHAP 4: Screenshot Postman (20 menit)**

#### 4.1 Setup Postman

**1. Import Collection:**
- Buka Postman
- Click "Import"
- Select file: `c:\xampp\htdocs\food_delivery_system\docs\POSTMAN_COLLECTION_COMPLETE.json`
- Click "Import"

**2. Import Environment:**
- Click "Import" lagi
- Select file: `c:\xampp\htdocs\food_delivery_system\docs\POSTMAN_ENVIRONMENT.json`
- Click "Import"

**3. Pilih Environment:**
- Di top-right corner, pilih dropdown environment
- Select: "Food Delivery - Local"

#### 4.2 Screenshot #1: Collection View

**Yang harus terlihat:**
- List lengkap folders/requests di collection
- Nama collection: "Food Delivery System API"
- Folders: Auth, User Service, Restaurant Service, Order Service, dll

**Cara screenshot:**
1. Expand semua folders di collection
2. Screenshot seluruh sidebar kiri
3. Save sebagai: `evidence\postman-collection-run.png`

#### 4.3 Screenshot #2: Test Results

**Option A: Run Collection dengan Collection Runner (RECOMMENDED)**

1. Click collection "Food Delivery System API"
2. Click "Run" (atau icon ️ Run)
3. Pilih requests yang mau di-run (atau pilih semua)
4. Click "Run Food Delivery System API"
5. Tunggu sampai semua request selesai
6. Screenshot hasil dengan **test results showing PASSED**
7. Save sebagai: `evidence\postman-tests-passed.png`

**Option B: Manual Request (jika Collection Runner error)**

1. Click salah satu request (misalnya "Login")
2. Click "Send"
3. Screenshot response yang sukses (status 200/201)
4. Pastikan terlihat:
   - Request method & URL
   - Response status code
   - Response body
5. Save sebagai: `evidence\postman-tests-passed.png`

---

## **TIPS SCREENSHOT BERKUALITAS**

### **Do's **
- Gunakan full screen browser/Postman
- Pastikan URL terlihat jelas
- Pastikan response body terlihat
- Gunakan resolusi tinggi (tidak blur)
- Crop agar fokus ke konten penting
- Format PNG (lebih baik dari JPG untuk screenshot code)

### **Don'ts **
- Jangan ada bookmark bar pribadi
- Jangan ada tabs yang tidak relevan
- Jangan blur/pecah
- Jangan ada informasi sensitif (password, token, dll)

---

## **CHECKLIST PROGRESS**

Print checklist ini dan centang saat selesai:

### Health Endpoints:
- [ ] `health-gateway.png`
- [ ] `health-user.png`
- [ ] `health-restaurant.png`
- [ ] `health-order.png`
- [ ] `health-delivery.png`
- [ ] `health-payment.png`

### Swagger UI:
- [ ] `swagger-api-gateway.png`
- [ ] `swagger-user-service.png` (atau alternatif)
- [ ] `swagger-restaurant-service.png` (atau alternatif)
- [ ] `swagger-order-service.png` (atau alternatif)
- [ ] `swagger-delivery-service.png` (atau alternatif)
- [ ] `swagger-payment-service.png` (atau alternatif)

### Postman:
- [ ] `postman-collection-run.png`
- [ ] `postman-tests-passed.png`

**Total: 14 screenshots**

---

## **TROUBLESHOOTING**

### **Problem 1: Service tidak bisa dijalankan**
```
Error: Address already in use
```
**Solution:**
```powershell
# Cari process yang menggunakan port
netstat -ano | findstr :5000

# Kill process (ganti <PID> dengan Process ID dari command diatas)
taskkill /PID <PID> /F
```

### **Problem 2: Browser tidak bisa akses localhost**
**Solution:**
- Tunggu 5-10 detik setelah service start
- Refresh browser (F5)
- Clear browser cache
- Coba browser lain (Chrome/Edge/Firefox)

### **Problem 3: Swagger UI tidak muncul**
**Solution:**
- Cek log terminal, pastikan tidak ada error
- Cek apakah service menggunakan Flask-RESTX atau Flask-Swagger
- Jika tidak ada Swagger, gunakan alternatif (screenshot code atau Postman)

### **Problem 4: Postman Collection error saat import**
**Solution:**
- Pastikan file JSON valid
- Buka file di text editor, cek format
- Gunakan collection yang lebih simple: `POSTMAN_COLLECTION.json`

---

## **ESTIMASI WAKTU**

| Tahap | Estimasi | Difficulty |
|-------|----------|------------|
| Persiapan (run services) | 15 min | Easy |
| Health screenshots | 20 min | Easy |
| Swagger screenshots | 30 min | Medium |
| Postman screenshots | 20 min | Medium |
| **TOTAL** | **~90 min** | |

---

## 🎁 **BONUS: Quick Screenshot Script**

Jika ingin otomatis, gunakan PowerShell script ini:

```powershell
# Create evidence directory if not exists
New-Item -ItemType Directory -Force -Path "c:\xampp\htdocs\food_delivery_system\evidence"

# Open all health endpoints in browser tabs (requires manual screenshot)
Start-Process "http://localhost:5000/health"
Start-Sleep -Seconds 2
Start-Process "http://localhost:5001/health"
Start-Sleep -Seconds 2
Start-Process "http://localhost:5002/health"
Start-Sleep -Seconds 2
Start-Process "http://localhost:5003/health"
Start-Sleep -Seconds 2
Start-Process "http://localhost:5004/health"
Start-Sleep -Seconds 2
Start-Process "http://localhost:5005/health"

Write-Host "Semua health endpoints dibuka di browser!"
Write-Host "Silakan screenshot satu per satu dan save di folder evidence/"
```

Save sebagai `open_health_endpoints.ps1` dan jalankan:
```powershell
.\open_health_endpoints.ps1
```

---

## **FINAL CHECK**

Sebelum melanjutkan ke video demo, pastikan:

- [ ] Folder `evidence/` berisi 14 file PNG
- [ ] Semua screenshot clear dan tidak blur
- [ ] Semua screenshot menunjukkan status success/healthy
- [ ] File naming sesuai dengan requirement di `evidence/README.md`

---

**SELAMAT MENGAMBIL SCREENSHOT! **

**Next step:** Setelah screenshot selesai → Buat video demo!
