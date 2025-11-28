ocs/PANDUAN_LENGKAP_RUNNING.md</path>
<content">
# PANDUAN LENGKAP: MENJALANKAN FOOD DELIVERY SYSTEM

## **MASALAH YANG AKITITIS DIPERBAIKI:**

1. **Frontend belum lengkap** - index.html ada tapi belum menampilkan konten sempurna
2. **Server belum running** - API gateway dan services belum dijalankan
3. **Port salah** - Buka port 5501 (VS Code live server) padahal seharusnya gateway di port 5000

---

## **SOLUSI LENGKAP:**

### **STEP 1: PERSIAPAN ENVIRONMENT**

```bash
# 1. Pastikan sudah ada file .env di root folder
# 2. Install dependencies
pip install -r microservices/api-gateway/requirements.txt
pip install -r microservices/service-template/requirements.txt

# 3. Setup virtual environment (jika belum)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### **STEP 2: JALANKAN API GATEWAY (PORT 5000) - WAJIB**

```bash
# Terminal 1 - BUKA CMD/TERMINAL BARU
cd microservices/api-gateway
python app.py

# Expected Output:
# API Gateway starting on port 5000
# JWT Authentication enabled
# Swagger Documentation: http://localhost:5000/api-docs/
```

### **STEP 3: JALANKAN SEMUA SERVICES**

```bash
# Terminal 2 - User Service (ARTHUR - 5001)
cd microservices/user-service
python app.py

# Terminal 3 - Restaurant Service (rizki - 5002)  
cd microservices/restaurant-service
python app.py

# Terminal 4 - Order Service (Nadia - 5003)
cd microservices/order-service
python app.py

# Terminal 5 - Delivery Service (aydin - 5004)
cd microservices/delivery-service
python app.py

# Terminal 6 - Payment Service (reza - 5005)
cd microservices/payment-service
python app.py
```

### **STEP 4: AKSES APLIKASI**

```bash
# BUKA BROWSER DAN KETIK:
http://localhost:5000/  # ← INILAH URL YANG BENAR!

# BUKAN:
http://localhost:5501/  # ← INI SALAH! (VS Code live server)
```

---

## **FRONTEND FIXES**

### **A. PYTHON HTTP SERVER (RECOMMENDED)**

```bash
# Di folder project root, jalankan:
python -m http.server 5000

# Akan serve static files dari folder saat ini
# Frontend akan accessible di: http://localhost:5000/
```

### **B. MODIFIED API GATEWAY SERVE FRONTEND**

Edit `microservices/api-gateway/app.py`, tambahkan route untuk serve frontend:

```python
from flask import send_from_directory, send_file
import os

# Serve frontend static files
@app.route('/')
def serve_frontend():
    try:
        return send_file('../../frontend/index.html')
    except:
        return jsonify({"error": "Frontend files not found"}), 404

@app.route('/<path:filename>')
def serve_static_files(filename):
    try:
        return send_from_directory('../../frontend', filename)
    except:
        return jsonify({"error": "File not found"}), 404
```

### **C. MANUAL STARTUP (EASIEST)**

```bash
# Di folder project root, jalankan satu script untuk semua:

# Buat start-all.py
python -c "
import subprocess
import time
import threading
import webbrowser

def start_server():
    # Start API Gateway
    subprocess.Popen(['python', 'microservices/api-gateway/app.py'])
    time.sleep(5)
    
    # Start frontend server
    subprocess.Popen(['python', '-m', 'http.server', '5000'])
    time.sleep(2)
    
    # Open browser
    webbrowser.open('http://localhost:5000/')

# Run
start_server()
"
```

---

## **TESTING APAKAH BERHASIL**

### **1. Health Check**
```bash
# Buka browser dan cek:
http://localhost:5000/health

# Expected Response:
{
  "status": "healthy",
  "service": "api-gateway", 
  "timestamp": "2024-11-12T16:56:23Z"
}
```

### **2. API Documentation**
```
# Test Swagger UI:
http://localhost:5000/api-docs/

# Test individual services:
http://localhost:5001/health  # User Service
http://localhost:5002/health  # Restaurant Service  
http://localhost:5003/health  # Order Service
http://localhost:5004/health  # Delivery Service
http://localhost:5005/health  # Payment Service
```

### **3. Frontend Test**
```
# Test homepage:
http://localhost:5000/

# Should display:
- Food Delivery System header
- Restaurant list dengan gambar
- Navigation menu
- Footer dengan informasi
```

---

## **TROUBLESHOOTING**

### **Problem: "Port 5000 sudah digunakan"**
```bash
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Linux/Mac:
lsof -ti:5000 | xargs kill -9
```

### **Problem: "Frontend tidak muncul"**
```bash
# Solution 1: Check file structure
ls frontend/
# Should show: index.html, restaurant.html, cart.html, etc.

# Solution 2: Run manual HTTP server
cd frontend
python -m http.server 8000
# Then access: http://localhost:8000/
```

### **Problem: "API Gateway error"**
```bash
# Check imports di api-gateway/app.py
# Pastikan sudah ada:
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

# Check .env file exists di root folder
ls .env
```

### **Problem: "Services tidak respond"**
```bash
# Check logs di terminal masing-masing service
# Pastikan tidak ada error message seperti:
# - Module not found
# - Database connection error
# - Port already in use
```

---

## **SUCCESS CHECKLIST**

**Before claiming success, check:**

- [ ] **API Gateway** running di terminal dengan output: "API Gateway starting on port 5000"
- [ ] **6 services** running di 6 terminal berbeda (ports 5000-5005)
- [ ] **http://localhost:5000/** menampilkan homepage Food Delivery System
- [ ] **http://localhost:5000/health** returns JSON dengan "healthy"
- [ ] **http://localhost:5000/api-docs/** menampilkan Swagger UI
- [ ] **Navigation** antar halaman frontend berfungsi
- [ ] **Cart functionality** working (add to cart, proceed to checkout)

---

## 📁 **FILE STRUCTURE YANG DIHARAPKAN**

```
food-delivery-system/
├── .env                           ← Environment variables
├── frontend/                      ← Static files
│   ├── index.html               ← Homepage
│   ├── restaurant.html          ← Restaurant detail
│   ├── cart.html               ← Shopping cart
│   ├── checkout.html           ← Checkout page
│   ├── order-tracking.html     ← Order tracking
│   └── admin.html              ← Admin panel
├── microservices/
│   ├── api-gateway/             ← API Gateway (PORT 5000)
│   ├── user-service/            ← User Service (PORT 5001)
│   ├── restaurant-service/      ← Restaurant Service (PORT 5002)
│   ├── order-service/           ← Order Service (PORT 5003)
│   ├── delivery-service/        ← Delivery Service (PORT 5004)
│   └── payment-service/         ← Payment Service (PORT 5005)
└── docs/                        ← Documentation
```

---

## **QUICK START COMMANDS**

### **Method 1: Manual (Step by step)**
```bash
# Terminal 1: API Gateway
cd microservices/api-gateway && python app.py

# Terminal 2: Frontend Server
cd frontend && python -m http.server 5000

# Terminal 3: User Service  
cd microservices/user-service && python app.py

# Terminal 4: Restaurant Service
cd microservices/restaurant-service && python app.py

# Terminal 5: Order Service
cd microservices/order-service && python app.py

# Terminal 6: Delivery Service
cd microservices/delivery-service && python app.py

# Terminal 7: Payment Service
cd microservices/payment-service && python app.py
```

### **Method 2: Auto Script**
```bash
# Jalankan script yang sudah disediakan
./scripts/run-all.sh
```

---

## **FINAL ACCESS POINTS**

**Setelah semua running:**

```
Frontend Homepage:     http://localhost:5000/
API Documentation:     http://localhost:5000/api-docs/
Health Check:          http://localhost:5000/health

Login Demo:
- Admin: username=admin, password=admin123
- User:  username=user, password=user123

Postman Collection:    docs/POSTMAN_COLLECTION.json
📖 Documentation:         docs/SETUP_GUIDE.md
```

---

## 🚨 **JANGAN LUPA:**

1. **Gunakan PORT 5000** untuk API Gateway (bukan 5501)
2. **Jalankan SEMUA 6 services** (1 gateway + 5 microservices)
3. **Pastikan .env file** ada di root folder
4. **Frontend harus di-serve** via Python HTTP server atau API Gateway
5. **Test health endpoints** sebelum akses frontend

**Setelah steps ini, Food Delivery System akan berjalan sempurna!**