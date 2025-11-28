# Cara Menjalankan Program Food Delivery System

## Prerequisites (Yang Harus Ada di Komputer Anda)

### 1. Install Python
```bash
# Download & install Python 3.8+ dari https://python.org
# Pastikan saat installcentang "Add Python to PATH"

# Verify installation
python --version
# Output seharusnya: Python 3.8.x atau lebih tinggi
```

### 2. Install Git (untuk download project)
```bash
# Download & install Git dari https://git-scm.com
# Verify installation
git --version
```

### 3. Download Project
```bash
# Clone project dari GitHub (jika belum ada)
git clone https://github.com/aturrr62/kelompok01_food_delivery_system.git
cd food-delivery-system
```

---

## 🏗️ **METODE 1: AUTOMATIC SETUP (RECOMMENDED)**

### Step 1: Setup Environment
```bash
# Di terminal/command prompt, masuk ke folder project:
cd food-delivery-system

# Run setup script (Linux/Mac):
chmod +x scripts/setup.sh
./scripts/setup.sh

# Untuk Windows:
# python scripts/setup.sh
```

### Step 2: Jalankan Semua Service
```bash
# Start semua services otomatis:
chmod +x scripts/run-all.sh
./scripts/run-all.sh

# Untuk Windows:
# python scripts/run-all.sh
```

### Step 3: Access Aplikasi
```bash
# Buka browser dan akses:
# Frontend: http://localhost:5000/
# API Docs: http://localhost:5000/api-docs/
# Health Check: http://localhost:5000/health
```

---

## **METODE 2: MANUAL SETUP (DETAILED)**

### Step 1: Setup Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
# Install untuk semua services
pip install -r microservices/service-template/requirements.txt
pip install -r microservices/api-gateway/requirements.txt

# Install JWT dependencies (untuk API Gateway)
pip install Flask-JWT-Extended==4.5.3
```

### Step 3: Jalankan API Gateway (Terminal 1)
```bash
# Buka Terminal baru (Terminal 1):
cd microservices/api-gateway
python app.py

# Expected output:
# API Gateway starting on port 5000
# Swagger Documentation: http://localhost:5000/api-docs/
# Authentication: JWT Bearer Token
```

### Step 4: Jalankan User Service (Terminal 2)
```bash
# Buka Terminal baru (Terminal 2):
cd microservices/user-service
python app.py

# Expected output:
# 👤 User Service starting on port 5001
```

### Step 5: Jalankan Restaurant Service (Terminal 3)
```bash
# Buka Terminal baru (Terminal 3):
cd microservices/restaurant-service
python app.py

# Expected output:
# 🍽️ Restaurant Service starting on port 5002
```

### Step 6: Jalankan Order Service (Terminal 4)
```bash
# Buka Terminal baru (Terminal 4):
cd microservices/order-service
python app.py

# Expected output:
# Order Service starting on port 5003
```

### Step 7: Jalankan Delivery Service (Terminal 5)
```bash
# Buka Terminal baru (Terminal 5):
cd microservices/delivery-service
python app.py

# Expected output:
# 🚚 Delivery Service starting on port 5004
```

### Step 8: Jalankan Payment Service (Terminal 6)
```bash
# Buka Terminal baru (Terminal 6):
cd microservices/payment-service
python app.py

# Expected output:
# 💳 Payment Service starting on port 5005
```

---

## **CARA MENGGUNAKAN APLIKASI**

### Frontend Web Interface
```
1. Buka Browser (Chrome, Firefox, Safari)
2. Ketik: http://localhost:5000/
3. Anda akan melihat halaman utama Food Delivery System

Navigasi:
- Home (index.html) - List restaurant
- Restaurant Detail - Klik restaurant untuk lihat menu
- Add to Cart - Klik menu yang diinginkan
- Cart (cart.html) - Review keranjang belanja
- Checkout (checkout.html) - Isi data dan bayar
- Order Tracking - Lacak pesanan
```

### API Testing
```
1. Download & install Postman dari https://postman.com
2. Import collection: docs/POSTMAN_COLLECTION.json
3. Login dengan demo credentials:
   - Admin: username="admin", password="admin123"
   - User: username="user", password="user123"
4. Test semua endpoints
```

---

## **TROUBLESHOOTING**

### Problem: "Python tidak ditemukan"
```bash
# Solution:
# 1. Reinstall Python dengan centang "Add to PATH"
# 2. Restart terminal/command prompt
# 3. Check: python --version
```

### Problem: "Port 5000 sudah digunakan"
```bash
# Solution Windows:
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Solution Linux/Mac:
lsof -ti:5000 | xargs kill -9
```

### Problem: "Module tidak ditemukan"
```bash
# Solution:
# 1. Activate virtual environment
# 2. Reinstall dependencies:
pip install -r requirements.txt
```

### Problem: "Database error"
```bash
# Solution:
# 1. Hapus database lama:
rm -f microservices/*/database.db

# 2. Restart services (database akan dibuat ulang otomatis)
```

---

## **CEK STATUS SERVICE**

### Health Check URLs:
```
API Gateway:  http://localhost:5000/health
User Service:     http://localhost:5001/health
Restaurant:       http://localhost:5002/health
Order Service:    http://localhost:5003/health
Delivery Service: http://localhost:5004/health
Payment Service:  http://localhost:5005/health
```

### Expected Response:
```json
{
  "status": "healthy",
  "service": "service-name",
  "timestamp": "2024-11-12T16:22:41Z"
}
```

---

## **QUICK START CHECKLIST**

**Sebelum menjalankan, pastikan:**
- [ ] Python 3.8+ terinstall
- [ ] Virtual environment ter-setup
- [ ] Dependencies ter-install tanpa error
- [ ] Ports 5000-5005 tersedia

**After running:**
- [ ] API Gateway running di http://localhost:5000
- [ ] Frontend accessible di http://localhost:5000/
- [ ] Health check returns "healthy"
- [ ] All 5 services respond pada ports masing-masing

---

## **DEMO WORKFLOW**

### Test via Browser:
```
1. Buka http://localhost:5000/
2. Klik restaurant "Warung Bakso Malang"
3. Add "Bakso Solo" to cart
4. Go to cart
5. Proceed to checkout
6. Fill form dan click "Bayar"
7. Redirect to order tracking
```

### Test via API:
```
1. Login: POST /auth/login
2. Get users: GET /api/user-service/api/users
3. Create restaurant: POST /api/restaurant-service/api/restaurants
4. Create order: POST /api/order-service/api/orders
5. Create payment: POST /api/payment-service/api/payments
```

---

## 📞 **SUPPORT**

Jika masih ada masalah:

1. **Check logs** di terminal untuk error messages
2. **Verify prerequisites** (Python, dependencies, ports)
3. **Restart services** one by one
4. **Check network/firewall** tidak blokir ports
5. **Try different method** (automatic vs manual)

---

## **SUCCESS INDICATORS**

**Program berhasil dijalankan jika:**
- **6 terminal windows** running (1 gateway + 5 services)
- **http://localhost:5000/** loads halaman utama
- **http://localhost:5000/health** returns healthy
- **http://localhost:5000/api-docs/** shows Swagger docs
- **Can navigate** through all frontend pages
- **Postman tests** pass 90%+

**Selamat! Program Food Delivery System Anda siap digunakan! **