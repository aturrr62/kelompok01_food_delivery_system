# DATABASE FIX SCRIPT - Food Delivery System

## **PROBLEM:** Database Schema Outdated

Services baru punya kolom yang tidak ada di database lama:
- Order Service: `total_price` missing
- Payment Service: `card_last_4` missing

## **SOLUTION: Recreate Databases**

### **METHOD 1: Quick Fix - Delete & Recreate (RECOMMENDED)** 

**Step 1: Stop All Services**
```powershell
# Tekan Ctrl+C di semua terminal yang running services
```

**Step 2: Delete Old Database Files**
```powershell
# Order Service
Remove-Item "microservices\order-service\order_service.db" -ErrorAction SilentlyContinue

# Payment Service  
Remove-Item "microservices\payment-service\payment_service.db" -ErrorAction SilentlyContinue

# Optional: Delete semua database untuk fresh start
Remove-Item "microservices\user-service\user_service.db" -ErrorAction SilentlyContinue
Remove-Item "microservices\restaurant-service\restaurant.db" -ErrorAction SilentlyContinue
Remove-Item "microservices\delivery-service\delivery_service.db" -ErrorAction SilentlyContinue
```

**Step 3: Restart All Services**
```powershell
# Terminal 1 - API Gateway
cd microservices\api-gateway
python app.py

# Terminal 2 - User Service
cd microservices\user-service
python app.py

# Terminal 3 - Restaurant Service
cd microservices\restaurant-service
python app.py

# Terminal 4 - Order Service
cd microservices\order-service
python app.py

# Terminal 5 - Delivery Service
cd microservices\delivery-service
python app.py

# Terminal 6 - Payment Service
cd microservices\payment-service
python app.py
```

**Expected Output (each service):**
```
[Service Name] tables created
```

Database akan otomatis dibuat dengan schema yang benar!

---

### **METHOD 2: Manual SQL Migration (Advanced)**

Jika Anda ingin keep data lama:

**Order Service:**
```sql
-- Connect to order_service.db
sqlite3 microservices/order-service/order_service.db

-- Check if column exists
PRAGMA table_info(order);

-- Add column if not exists (SQLite way)
ALTER TABLE "order" ADD COLUMN total_price REAL DEFAULT 0.0;

-- Exit
.exit
```

**Payment Service:**
```sql
-- Connect to payment_service.db
sqlite3 microservices/payment-service/payment_service.db

-- Check columns
PRAGMA table_info(payment);

-- Add column if not exists
ALTER TABLE payment ADD COLUMN card_last_4 VARCHAR(4);

-- Exit
.exit
```

---

### **METHOD 3: Python Migration Script (Automated)**

Run this script:

```powershell
python database_migration.py
```

(See database_migration.py file)

---

## **VERIFICATION**

After recreating databases, test:

**Order Service:**
```powershell
# Create order
curl -X POST http://localhost:5003/api/orders ^
  -H "Content-Type: application/json" ^
  -d "{\"user_id\":1,\"restaurant_id\":1,\"delivery_address\":\"Test\",\"items\":[{\"menu_item_id\":1,\"quantity\":1,\"unit_price\":10000}]}"
```

**Expected:** `201 Created` with `total_price: 10000` 

**Payment Service:**
```powershell
# Create payment
curl -X POST http://localhost:5005/api/payments ^
  -H "Content-Type: application/json" ^
  -d "{\"order_id\":1,\"user_id\":1,\"amount\":10000,\"payment_method\":\"credit_card\",\"card_last_4\":\"1234\"}"
```

**Expected:** `201 Created` with `card_last_4: "1234"` 

---

## **TROUBLESHOOTING**

### **Problem: Column still missing after restart**

**Solution:**
1. Make sure service completely stopped (Ctrl+C)
2. Actually delete the database file
3. Restart service
4. Check output for "tables created"

### **Problem: Data lost after recreation**

**Solution:**
- Use Method 2 (Manual SQL) to keep data
- Or use Method 3 (Python script) for safer migration

### **Problem: Permission denied when deleting**

**Solution:**
```powershell
# Force delete
Remove-Item -Path "path\to\database.db" -Force
```

---

## **SUMMARY**

**Fastest Fix:** Delete databases → Restart services → Fresh tables 

**Time:** 2-3 minutes

**Risk:** Lose existing data (OK for dev/testing)

**Status:** READY TO TEST! 
