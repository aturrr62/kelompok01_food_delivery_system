# PANDUAN LENGKAP TEST API DENGAN POSTMAN

**Dibuat:** 27 November 2025  
**Project:** Food Delivery System  
**Status:** All services running 

---

## **PERSIAPAN**

### **Pastikan Semua Service Running:**

Cek di terminal/PowerShell, harus ada 7 services:
- API Gateway (Port 5000)
- User Service (Port 5001)
- Restaurant Service (Port 5002)
- Order Service (Port 5003)
- Delivery Service (Port 5004)
- Payment Service (Port 5005)
- Frontend (Port 8080) - optional

---

## **STEP 1: INSTALL & BUKA POSTMAN**

### **A. Install Postman (jika belum ada)**

**Download:** https://www.postman.com/downloads/

**Atau bisa pakai Postman Web:**
- Buka: https://web.postman.co/
- Login dengan akun Google/email

---

## 📥 **STEP 2: IMPORT COLLECTION & ENVIRONMENT**

### **A. Import Collection**

1. **Buka Postman**
2. **Klik "Import"** (tombol di pojok kiri atas)
3. **Pilih "Upload Files"**
4. **Browse ke:**
   ```
   c:\xampp\htdocs\food_delivery_system\docs\POSTMAN_COLLECTION.json
   ```
5. **Klik "Import"**

**Expected Result:**
- Folder "Food Delivery System API - UPDATED" muncul di sidebar kiri
- Total 34 requests

---

### **B. Import Environment**

1. **Klik "Import"** lagi
2. **Browse ke:**
   ```
   c:\xampp\htdocs\food_delivery_system\docs\POSTMAN_ENVIRONMENT.json
   ```
3. **Klik "Import"**

**Expected Result:**
- Environment "Food Delivery - Local" muncul di dropdown (pojok kanan atas)

---

### **C. Pilih Environment**

1. **Klik dropdown di pojok kanan atas** (sebelah icon mata)
2. **Pilih:** "Food Delivery - Local"

**Expected Result:**
- Environment aktif (terlihat di dropdown)
- Variable `base_url`, `gateway_url`, dll tersedia

---

## **STEP 3: TEST HEALTH CHECKS (WARMUP)**

**Tujuan:** Memastikan semua service berjalan dengan baik

### **Test 1: API Gateway Health**

1. **Expand folder:** "Health Checks"
2. **Klik:** "API Gateway Health"
3. **Klik tombol:** "Send" (biru)

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "api-gateway",
  "timestamp": "2025-11-27T..."
}
```

**Status Code:** `200 OK` (hijau)

---

### **Test 2-6: Service Health Checks**

**Ulangi untuk semua:**
- User Service Health → `200 OK`
- Restaurant Service Health → `200 OK`
- Order Service Health → `200 OK`
- Delivery Service Health → `200 OK`
- Payment Service Health → `200 OK`

**Jika semua `200 OK` → LANJUT! **

---

## 👤 **STEP 4: TEST USER SERVICE**

### **Test 1: Get All Users (GET)**

1. **Expand folder:** "User Service"
2. **Klik:** "Get All Users"
3. **Lihat URL:** `{{base_url}}/api/users`
4. **Klik:** "Send"

**Expected Response:**
```json
{
  "success": true,
  "data": [],
  "count": 0
}
```

**Status Code:** `200 OK`

**Note:** Data kosong karena belum ada user

---

### **Test 2: Create User (POST)**

1. **Klik:** "Create User (Register)"
2. **Lihat tab "Body"** → harus ada JSON:
   ```json
   {
     "username": "testuser",
     "email": "test@example.com",
     "password": "password123",
     "full_name": "Test User",
     "phone": "08123456789",
     "user_type": "customer"
   }
   ```
3. **Klik:** "Send"

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User",
    "user_type": "customer",
    ...
  },
  "message": "User created successfully"
}
```

**Status Code:** `201 Created`

**PENTING:** Save `id` dari response (contoh: `1`)

---

### **Test 3: Login User (POST)**

1. **Klik:** "Login User"
2. **Lihat Body:**
   ```json
   {
     "action": "login",
     "username": "testuser",
     "password": "password123"
   }
   ```
3. **Klik:** "Send"

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "user": { ... },
    "token": "eyJ0eXAiOiJKV1QiLC..."
  },
  "message": "Login successful"
}
```

**Status Code:** `200 OK`

**PENTING:** Copy `token` untuk dipakai nanti (opsional)

---

### **Test 4: Get User by ID (GET)**

1. **Klik:** "Get User by ID"
2. **Ubah URL** dari `/api/users/1` sesuai ID yang tadi (jika beda)
3. **Klik:** "Send"

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "testuser",
    ...
  }
}
```

**Status Code:** `200 OK`

---

### **Test 5: Update User (PUT)**

1. **Klik:** "Update User"
2. **Lihat Body:**
   ```json
   {
     "full_name": "Updated Name",
     "phone": "08199999999"
   }
   ```
3. **Klik:** "Send"

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "full_name": "Updated Name",
    "phone": "08199999999",
    ...
  },
  "message": "User updated successfully"
}
```

**Status Code:** `200 OK`

---

### **Test 6: Delete User (DELETE) - SKIP DULU**

**JANGAN DELETE DULU** - Kita butuh user ini untuk test service lain!

---

## 🍽️ **STEP 5: TEST RESTAURANT SERVICE**

### **Test 1: Create Restaurant (POST)**

1. **Expand folder:** "Restaurant Service"
2. **Klik:** "Create Restaurant (with menu)"
3. **Lihat Body:**
   ```json
   {
     "name": "Warung Nasi Padang",
     "description": "Authentic Padang cuisine",
     "address": "Jl. Sudirman No. 123",
     "phone": "021-12345678",
     "email": "padang@example.com",
     "rating": 4.5,
     "menu": [
       {
         "name": "Rendang",
         "description": "Spicy beef",
         "price": 35000,
         "category": "main"
       },
       {
         "name": "Ayam Pop",
         "description": "Fried chicken",
         "price": 25000,
         "category": "main"
       }
     ]
   }
   ```
4. **Klik:** "Send"

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Warung Nasi Padang",
    "menu": [
      { "id": 1, "name": "Rendang", "price": 35000 },
      { "id": 2, "name": "Ayam Pop", "price": 25000 }
    ]
  },
  "message": "Restaurant created successfully"
}
```

**Status Code:** `201 Created`

**Save:** `restaurant_id = 1`, `menu_item_id = 1`

---

### **Test 2: Get All Restaurants (GET)**

1. **Klik:** "Get All Restaurants"
2. **Klik:** "Send"

**Expected Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Warung Nasi Padang",
      ...
    }
  ],
  "count": 1
}
```

**Status Code:** `200 OK`

---

### **Test 3: Get Restaurant by ID (GET)**

1. **Klik:** "Get Restaurant by ID (with menu)"
2. **Klik:** "Send"

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Warung Nasi Padang",
    "menu": [...]  ← Menu included!
  }
}
```

**Status Code:** `200 OK`

---

### **Test 4: Update Restaurant (PUT)**

1. **Klik:** "Update Restaurant (and menu)"
2. **Ubah Body sesuai keinginan**
3. **Klik:** "Send"

**Status Code:** `200 OK`

---

## **STEP 6: TEST ORDER SERVICE**

### **Test 1: Create Order (POST)**

1. **Expand folder:** "Order Service"
2. **Klik:** "Create Order"
3. **Lihat Body:**
   ```json
   {
     "user_id": 1,
     "restaurant_id": 1,
     "delivery_address": "Jl. Gatot Subroto No. 45",
     "notes": "Extra spicy please",
     "items": [
       {
         "menu_item_id": 1,
         "menu_item_name": "Rendang",
         "quantity": 2,
         "unit_price": 35000
       },
       {
         "menu_item_id": 2,
         "menu_item_name": "Ayam Pop",
         "quantity": 1,
         "unit_price": 25000
       }
     ]
   }
   ```
4. **Klik:** "Send"

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "order_number": "ORD-20251127...",
    "total_price": 95000,
    "items": [...]
  },
  "message": "Order created successfully"
}
```

**Status Code:** `201 Created`

**Save:** `order_id = 1`

---

### **Test 2: Get All Orders (GET)**

1. **Klik:** "Get All Orders"
2. **Klik:** "Send"

**Status Code:** `200 OK`

---

### **Test 3: Update Order Status (PUT)**

1. **Klik:** "Update Order Status"
2. **Lihat Body:**
   ```json
   {
     "status": "confirmed"
   }
   ```
3. **Klik:** "Send"

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "status": "confirmed",  ← Updated!
    ...
  }
}
```

**Status Code:** `200 OK`

---

## 🚚 **STEP 7: TEST DELIVERY SERVICE**

### **Test 1: Create Delivery (POST)**

1. **Expand folder:** "Delivery Service"
2. **Klik:** "Create Delivery"
3. **Lihat Body:**
   ```json
   {
     "order_id": 1,
     "delivery_address": "Jl. Gatot Subroto No. 45",
     "pickup_address": "Jl. Sudirman No. 123",
     "notes": "Ring the bell"
   }
   ```
4. **Klik:** "Send"

**Status Code:** `201 Created`

**Save:** `delivery_id = 1`

---

### **Test 2: Update Delivery (Assign Courier) (PUT)**

1. **Klik:** "Update Delivery (Assign Courier)"
2. **Lihat Body:**
   ```json
   {
     "courier_id": 1,
     "courier_name": "John Doe",
     "courier_phone": "08123456789",
     "status": "assigned"
   }
   ```
3. **Klik:** "Send"

**Status Code:** `200 OK`

---

### **Test 3: Update Delivery Location (PUT)**

1. **Klik:** "Update Delivery Location"
2. **Lihat Body:**
   ```json
   {
     "current_latitude": -6.2088,
     "current_longitude": 106.8456,
     "status": "in_transit"
   }
   ```
3. **Klik:** "Send"

**Status Code:** `200 OK`

---

## 💳 **STEP 8: TEST PAYMENT SERVICE**

### **Test 1: Create Payment (POST)**

1. **Expand folder:** "Payment Service"
2. **Klik:** "Create Payment (Auto Process)"
3. **Lihat Body:**
   ```json
   {
     "order_id": 1,
     "user_id": 1,
     "amount": 95000,
     "payment_method": "credit_card",
     "card_last_4": "1234",
     "auto_process": true
   }
   ```
4. **Klik:** "Send"

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "status": "success",  ← Auto processed!
    "amount": 95000,
    ...
  }
}
```

**Status Code:** `201 Created`

---

### **Test 2: Refund Payment (PUT)**

1. **Klik:** "Refund Payment"
2. **Lihat Body:**
   ```json
   {
     "action": "refund",
     "refund_amount": 95000,
     "refund_reason": "Customer requested refund"
   }
   ```
3. **Klik:** "Send"

**Status Code:** `200 OK`

---

## **STEP 9: VERIFIKASI HASIL**

### **Checklist Test Results:**

- [ ] User Service - 4 methods tested (GET, POST, PUT, DELETE)
- [ ] Restaurant Service - 4 methods tested
- [ ] Order Service - 4 methods tested
- [ ] Delivery Service - 4 methods tested
- [ ] Payment Service - 4 methods tested
- [ ] All health checks return 200 OK

---

## **STEP 10: AMBIL SCREENSHOTS (UNTUK SUBMISSION)**

**Screenshot yang perlu:**

1. **Postman Collection Structure** (sidebar kiri showing all folders)
2. **Successful Test Results:**
   - User Service - Create User (201 Created)
   - Restaurant Service - Get All (200 OK)
   - Order Service - Create Order (201 Created)
   - Delivery Service - Update Delivery (200 OK)
   - Payment Service - Create Payment (201 Created)
   - Health Checks - All Green (200 OK)

**Cara screenshot:**
- Windows: `Win + Shift + S`
- Simpan di: `c:\xampp\htdocs\food_delivery_system\evidence\`

---

## **SUMMARY - TESTING COMPLETE!**

**Total Requests Tested:** ~20-25 requests

**HTTP Methods Verified:**
- GET - Read operations
- POST - Create operations
- PUT - Update operations
- DELETE - Delete operations (optional)

**Services Verified:**
- User Service (Port 5001)
- Restaurant Service (Port 5002)
- Order Service (Port 5003)
- Delivery Service (Port 5004)
- Payment Service (Port 5005)

---

## **NEXT STEPS:**

1. Save screenshots untuk submission
2. Buat video demo (lihat `VIDEO_DEMO_GUIDE.md`)
3. Update `video/link.txt` dengan URL video
4. Submit project!

---

**SELAMAT! API TESTING COMPLETE!**

**Troubleshooting:** Jika ada error, pastikan:
- Semua services running
- Port tidak bentrok
- JSON body benar formatnya
- ID yang dipakai sudah ada di database
