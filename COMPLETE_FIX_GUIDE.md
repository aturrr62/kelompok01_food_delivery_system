# SOLUSI LENGKAP - DATABASE & ENDPOINT ISSUES

## **PROBLEMS IDENTIFIED**

### **1. Database Schema Issues:**
- Order Service: Column `total_price` tidak ada di database lama
- Payment Service: Column `card_last_4` tidak ada di database lama

### **2. "Missing" Endpoints (Sebenarnya SUDAH ADA!):**
- `POST /api/users/auth` → Ini `POST /api/users` dengan `{"action": "login"}`
- `PUT /api/orders/{id}/status` → Ini `PUT /api/orders/{id}` dengan `{"status": "..."}`
- `PUT /api/payments/{id}/status` → Ini `PUT /api/payments/{id}` dengan `{"status": "..."}`
- `POST /api/payments/{id}/refund` → Ini `PUT /api/payments/{id}` dengan `{"action": "refund"}`

---

## **SOLUTIONS**

### **FIX DATABASE - PILIH SALAH SATU:**

#### **OPTION 1: Quick Fix (RECOMMENDED)** **2 MINUTES**

1. **Run script:**
   ```powershell
   .\QUICK_DATABASE_FIX.ps1
   ```

2. **Stop semua services** (Ctrl+C di semua terminal)

3. **Restart services** (ikuti instruksi di script)

**Done!** Database baru akan ter-create dengan schema yang benar!

---

#### **OPTION 2: Python Migration Script** 🐍 **3 MINUTES**

1. **Run migration:**
   ```powershell
   python database_migration.py
   ```

2. **Restart Order & Payment services:**
   ```powershell
   # Stop the services (Ctrl+C)
   
   # Restart Order Service
   cd microservices\order-service
   python app.py
   
   # Restart Payment Service  
   cd microservices\payment-service
   python app.py
   ```

**Keeps existing data!**

---

#### **OPTION 3: Manual SQL** **5 MINUTES**

**Order Service:**
```powershell
sqlite3 microservices\order-service\order_service.db
```
```sql
ALTER TABLE "order" ADD COLUMN total_price REAL DEFAULT 0.0;
.exit
```

**Payment Service:**
```powershell
sqlite3 microservices\payment-service\payment_service.db
```
```sql
ALTER TABLE payment ADD COLUMN card_last_4 VARCHAR(4);
.exit
```

Then restart services.

---

### **ENDPOINT USAGE GUIDE**

Endpoint yang "missing" sebenarnya **SUDAH ADA**, hanya cara pakainya berbeda:

#### **1. User Login (User Service)**

**SALAH (lama):**
```
POST http://localhost:5001/api/users/auth
```

**BENAR (baru):**
```
POST http://localhost:5001/api/users
Body:
{
  "action": "login",
  "username": "testuser",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {...},
    "token": "eyJ0eXAi..."
  }
}
```

---

#### **2. Update Order Status (Order Service)**

**SALAH (lama):**
```
PUT http://localhost:5003/api/orders/1/status
```

**BENAR (baru):**
```
PUT http://localhost:5003/api/orders/1
Body:
{
  "status": "confirmed"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "status": "confirmed",
    ...
  }
}
```

**Status options:**
- `pending`
- `confirmed`
- `preparing`
- `ready`
- `delivered`
- `cancelled`

---

#### **3. Update Payment Status (Payment Service)**

**SALAH (lama):**
```
PUT http://localhost:5005/api/payments/1/status
```

**BENAR (baru):**
```
PUT http://localhost:5005/api/payments/1
Body:
{
  "status": "success"
}
```

**Status options:**
- `pending`
- `processing`
- `success`
- `failed`
- `refunded`

---

#### **4. Refund Payment (Payment Service)**

**SALAH (lama):**
```
POST http://localhost:5005/api/payments/1/refund
```

**BENAR (baru):**
```
PUT http://localhost:5005/api/payments/1
Body:
{
  "action": "refund",
  "refund_amount": 50000,
  "refund_reason": "Customer requested"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "status": "refunded",
    "refund_amount": 50000,
    "refund_reason": "Customer requested",
    ...
  }
}
```

---

## **TESTING GUIDE**

### **Step 1: Fix Database**

Run Quick Fix script:
```powershell
.\QUICK_DATABASE_FIX.ps1
```

### **Step 2: Restart Services**

Follow script instructions to restart Order & Payment services.

### **Step 3: Test with Postman**

Use `POSTMAN_COLLECTION_DIRECT.json`:

**Test Order Service:**
```
POST http://localhost:5003/api/orders
Body:
{
  "user_id": 1,
  "restaurant_id": 1,
  "delivery_address": "Test Address",
  "items": [
    {
      "menu_item_id": 1,
      "menu_item_name": "Test Item",
      "quantity": 2,
      "unit_price": 25000
    }
  ]
}
```

**Expected:** `201 Created` with `total_price: 50000`

**Test Payment Service:**
```
POST http://localhost:5005/api/payments
Body:
{
  "order_id": 1,
  "user_id": 1,
  "amount": 50000,
  "payment_method": "credit_card",
  "card_last_4": "1234",
  "auto_process": true
}
```

**Expected:** `201 Created` with `card_last_4: "1234"`

**Test Order Status Update:**
```
PUT http://localhost:5003/api/orders/1
Body:
{
  "status": "confirmed"
}
```

**Expected:** `200 OK` with updated status

**Test Payment Refund:**
```
PUT http://localhost:5005/api/payments/1
Body:
{
  "action": "refund",
  "refund_amount": 50000,
  "refund_reason": "Test refund"
}
```

**Expected:** `200 OK` with status `refunded`

---

## **VERIFICATION CHECKLIST**

After fix:

- [ ] Order Service creates orders with `total_price` 
- [ ] Payment Service creates payments with `card_last_4` 
- [ ] User login via `POST /api/users` with action parameter 
- [ ] Order status update via `PUT /api/orders/{id}` 
- [ ] Payment refund via `PUT /api/payments/{id}` with action 
- [ ] All services return `200/201` instead of `500` 

---

## **SUMMARY**

### **Root Causes:**
1. **Database outdated** - created before model updates
2. **Endpoint naming confusion** - endpoints exist but with different URLs

### **Solutions:**
1. **Database:** Recreate or migrate to add missing columns
2. **Endpoints:** Use correct URLs with parameters

### **Time to Fix:** 2-5 minutes

### **Files Created:**
- `DATABASE_FIX_GUIDE.md` - Detailed guide
- `database_migration.py` - Automated Python script
- `QUICK_DATABASE_FIX.ps1` - PowerShell quick fix
- `COMPLETE_FIX_GUIDE.md` - This file

---

## **NEXT STEPS**

1. **Run:** `.\QUICK_DATABASE_FIX.ps1`
2. **Restart:** Order & Payment services
3. **Test:** With Postman (use POSTMAN_COLLECTION_DIRECT.json)
4. **Verify:** All requests return success
5. **Submit:** Project ready! 

---

**STATUS:** **ALL ISSUES HAVE SOLUTIONS - READY TO FIX!**
