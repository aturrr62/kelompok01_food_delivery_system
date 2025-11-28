## QUICK START GUIDE - MEMBENERIN & TESTING FOOD DELIVERY SYSTEM

Ini adalah panduan SUPER JELAS step-by-step untuk memastikan semua services berjalan dengan baik.

---

## PILIHAN TERCEPAT: 3 LANGKAH DOANG!

### **LANGKAH 1: Buka PowerShell di folder project**
```powershell
# Pastikan Anda di folder: c:\xampp\htdocs\food_delivery_system
cd c:\xampp\htdocs\food_delivery_system
```

### **LANGKAH 2: Jalankan script untuk start SEMUA services**
```powershell
.\START_ALL_SERVICES.ps1
```

**Apa yang akan terjadi:**
- 6 PowerShell window baru akan membuka
- Setiap window menjalankan 1 service dengan port berbeda
- Dependencies akan di-install otomatis

**Services yang akan start:**
```
Port 5000: API Gateway         (Main Entry Point)
Port 5001: User Service 👤        (ARTHUR) 
Port 5002: Restaurant Service 🍽️  (rizki)
Port 5003: Order Service       (Nadia)
Port 5004: Delivery Service 🚚    (aydin)
Port 5005: Payment Service 💳     (reza)
```

### **LANGKAH 3: Tunggu 15-20 detik, kemudian jalankan test**

Setelah semua services sudah jalan (lihat log di setiap window), buka terminal baru:

```powershell
# Di folder project: c:\xampp\htdocs\food_delivery_system
python TEST_ALL_APIS.py full
```

**Output yang akan Anda lihat:**
- Health Check - Status 200 OK
- Authentication tests
- User Service tests (5 tests)
- Restaurant Service tests (4 tests)
- Order Service tests (2 tests)
- Delivery Service tests (2 tests)
- Payment Service tests (3 tests)
- Error handling tests (3 tests)

---

## DETAILED TROUBLESHOOTING GUIDE

Jika ada masalah, ikuti ini:

### **Problem 1: "Address already in use" error**

**Penyebab:** Port sudah digunakan service lain

**Solusi:**
```powershell
# Cek process yang menggunakan port
netstat -ano | findstr :5000
netstat -ano | findstr :5001
netstat -ano | findstr :5002
netstat -ano | findstr :5003
netstat -ano | findstr :5004
netstat -ano | findstr :5005

# Jika ada, kill process dengan PID tertentu
# Contoh: taskkill /PID 1234 /F
taskkill /PID <PID_NUMBER> /F
```

### **Problem 2: "ModuleNotFoundError: No module named 'flask'"**

**Penyebab:** Dependencies belum ter-install

**Solusi:**
```powershell
# Manual install untuk setiap service
cd microservices/api-gateway
pip install -r requirements.txt

cd ../user-service
pip install -r requirements.txt

# ... dan seterusnya untuk service lain
```

### **Problem 3: "Connection refused" pada test**

**Penyebab:** Service belum sepenuhnya start

**Solusi:**
- Tunggu lebih lama (30 detik) sebelum run test
- Lihat log di setiap window untuk cek error
- Cek manual: `curl http://localhost:5000/health`

### **Problem 4: Database error (sqlite3.OperationalError)**

**Penyebab:** Database file corrupt atau permission issue

**Solusi:**
```powershell
# Hapus database files
Remove-Item microservices/*/instance/*.db -Force
Remove-Item microservices/*/*.db -Force

# Jalankan ulang services
.\START_ALL_SERVICES.ps1
```

### **Problem 5: Port 5000 conflict dengan frontend**

**Penyebab:** Script lama masih running

**Solusi:**
```powershell
# Check port usage
netstat -ano | findstr :5000

# Kill yang menggunakan port (jika perlu)
taskkill /PID <PID_NUMBER> /F
```

---

## TEST MODES YANG TERSEDIA

### **1. Quick Test (2 menit)**
```powershell
python TEST_ALL_APIS.py quick
```
- Hanya 5 basic tests
- Cepat untuk debugging
- Cocok untuk development

### **2. Full Test (5 menit)**
```powershell
python TEST_ALL_APIS.py full
```
- Semua 25 comprehensive tests
- Test semua endpoints di semua services
- RECOMMENDED untuk final verification

### **3. Debug Test (1 menit)**
```powershell
python TEST_ALL_APIS.py debug
```
- Hanya auth & health checks
- Untuk troubleshoot connection issues

---

## CHECKLIST SEBELUM TEST

- [ ] Semua 6 PowerShell window sudah buka
- [ ] Tidak ada error message di window (atau minimal error)
- [ ] Semua services show "Running on http://localhost:PORT"
- [ ] Sudah tunggu 15-20 detik
- [ ] `curl http://localhost:5000/health` returns JSON (di terminal baru)
- [ ] Test dibuat dengan Python 3.7+

---

## EXPECTED SUCCESS RESULTS

### **Target: 25/25 tests pass (100%)**

```
Health Check                                  (200)
Non-existent Service                         (404)
Login Admin                                  (200)
Verify Token                                 (200)
Get All Users                                (200)
Create User                                  (201)
Get User by ID                               (200)
Update User                                  (200)
Delete User (Soft)                           (200)
Get All Restaurants                          (200)
Create Restaurant                            (201)
Get All Menu Items                           (200)
Create Menu Item                             (201)
Get All Orders                               (200)
Create Order                                 (201)
Get All Deliveries                           (200)
Create Delivery                              (201)
Get All Payments                             (200)
Create Payment                               (201)
Process Payment                              (200)
Invalid Credentials                          (401)
Unauthorized Access                          (401)
Invalid JSON                                 (400)
Get User by ID (Non-existent)                (404)
API Documentation                            (200/404)
```

---

## MANUAL VERIFICATION (Alternative)

Jika tidak ingin run test script, bisa test manual pakai Postman/curl:

### **1. Test Health Check**
```bash
curl http://localhost:5000/health
```

### **2. Test Login**
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### **3. Test User Service**
```bash
curl http://localhost:5001/api/users
```

### **4. Test Restaurant Service**
```bash
curl http://localhost:5002/api/restaurants
```

Dan seterusnya...

---

## MONITORING TIPS

Untuk monitor services saat running:

### **Terminal 1: Monitor API Gateway**
```powershell
# Watch error logs
Get-Content -Path "microservices/api-gateway/app.py" -Wait
```

### **Terminal 2: Monitor specific service**
```powershell
# Misalnya User Service
cd microservices/user-service
python -u app.py  # -u untuk unbuffered output
```

### **Terminal 3: Test saat services running**
```powershell
# Run test sambil monitor
python TEST_ALL_APIS.py full

# Atau jika ingin repeat test setiap 10 detik
while ($true) { python TEST_ALL_APIS.py quick; Start-Sleep 10 }
```

---

## 🚨 IF ALL ELSE FAILS

Nuclear option - reset everything:

```powershell
# 1. Kill all Python processes
Get-Process python | Stop-Process -Force

# 2. Remove all database files
Remove-Item microservices/*/instance/*.db -Force -ErrorAction SilentlyContinue
Remove-Item microservices/*/*.db -Force -ErrorAction SilentlyContinue

# 3. Clean pip cache
pip cache purge

# 4. Reinstall everything
cd microservices/api-gateway; pip install -r requirements.txt
cd ../user-service; pip install -r requirements.txt
cd ../restaurant-service; pip install -r requirements.txt
cd ../order-service; pip install -r requirements.txt
cd ../delivery-service; pip install -r requirements.txt
cd ../payment-service; pip install -r requirements.txt

# 5. Start fresh
cd ..\..\
.\START_ALL_SERVICES.ps1
```

---

## 📞 SUPPORT

Jika masih error:
1. **Cek log di setiap service window** - lihat error message spesifik
2. **Run `python TEST_ALL_APIS.py debug`** - cek connection
3. **Check port dengan**: `netstat -ano | findstr :<PORT>`
4. **Google error message** - biasanya common issues

---

## CONGRATULATIONS!

Jika semua test pass (25/25), system sudah siap untuk:
- Production deployment
- Load testing
- Frontend integration
- API documentation
- Client demo

**Next steps:**
1. Integrate dengan frontend
2. Setup monitoring & logging
3. Configure database backup
4. Setup CI/CD pipeline
5. Deploy ke production

---

**Last Updated:** November 13, 2025
**Version:** 1.0
**Status:** READY FOR TESTING 
