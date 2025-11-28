# FIXED: POSTMAN TESTING GUIDE

## **PROBLEM IDENTIFIED**

**Root Cause:** URL Mismatch between Postman Collection and API Gateway Routing

- **Postman sent:** `http://localhost:5000/api/users`
- **Gateway expected:** `http://localhost:5000/api/user-service/api/users`
- **Result:** All requests returned 404

---

## **SOLUTION: USE NEW COLLECTION**

### **FILE:** `POSTMAN_COLLECTION_DIRECT.json` 

This new collection **bypasses the API Gateway** and hits services directly on their ports.

---

## **QUICK START (5 MINUTES)**

### **STEP 1: Import New Collection**

1. **Open Postman**
2. **Click "Import"**
3. **Select file:**
   ```
   c:\xampp\htdocs\food_delivery_system\docs\POSTMAN_COLLECTION_DIRECT.json
   ```
4. **Click "Import"**

**Expected:** Folder "Food Delivery - Direct to Services (FIXED)" appears

---

### **STEP 2: Quick Test - Health Checks**

Test all 5 health endpoints to verify services are running:

```
GET http://localhost:5001/health  → User Service
GET http://localhost:5002/health  → Restaurant Service
GET http://localhost:5003/health  → Order Service
GET http://localhost:5004/health  → Delivery Service
GET http://localhost:5005/health  → Payment Service
```

**All should return `200 OK`** 

---

### **STEP 3: Test Each Service**

#### **User Service (Port 5001)**

1. **Create User:**
   ```
   POST http://localhost:5001/api/users
   Body:
   {
     "username": "testuser",
     "email": "test@example.com",
     "password": "password123",
     "full_name": "Test User"
   }
   ```
   **Expected:** `201 Created` with user data

2. **Get All Users:**
   ```
   GET http://localhost:5001/api/users
   ```
   **Expected:** `200 OK` with array containing 1 user

3. **Login:**
   ```
   POST http://localhost:5001/api/users
   Body:
   {
     "action": "login",
     "username": "testuser",
     "password": "password123"
   }
   ```
   **Expected:** `200 OK` with token

---

#### **Restaurant Service (Port 5002)**

1. **Create Restaurant:**
   ```
   POST http://localhost:5002/api/restaurants
   Body:
   {
     "name": "Warung Padang",
     "address": "Jl. Sudirman No. 123",
     "rating": 4.5,
     "menu": [
       {"name": "Rendang", "price": 35000}
     ]
   }
   ```
   **Expected:** `201 Created`

2. **Get All Restaurants:**
   ```
   GET http://localhost:5002/api/restaurants
   ```
   **Expected:** `200 OK` with restaurants

---

#### **Order Service (Port 5003)**

1. **Create Order:**
   ```
   POST http://localhost:5003/api/orders
   Body:
   {
     "user_id": 1,
     "restaurant_id": 1,
     "delivery_address": "Jl. Gatot Subroto 45",
     "items": [
       {"menu_item_id": 1, "quantity": 2, "unit_price": 35000}
     ]
   }
   ```
   **Expected:** `201 Created`

2. **Update Order Status:**
   ```
   PUT http://localhost:5003/api/orders/1
   Body:
   {
     "status": "confirmed"
   }
   ```
   **Expected:** `200 OK`

---

#### **Delivery Service (Port 5004)**

1. **Create Delivery:**
   ```
   POST http://localhost:5004/api/deliveries
   Body:
   {
     "order_id": 1,
     "delivery_address": "Jl. Gatot Subroto 45"
   }
   ```
   **Expected:** `201 Created`

2. **Update Delivery:**
   ```
   PUT http://localhost:5004/api/deliveries/1
   Body:
   {
     "courier_id": 1,
     "status": "in_transit"
   }
   ```
   **Expected:** `200 OK`

---

#### **Payment Service (Port 5005)**

1. **Create Payment:**
   ```
   POST http://localhost:5005/api/payments
   Body:
   {
     "order_id": 1,
     "user_id": 1,
     "amount": 70000,
     "payment_method": "credit_card",
     "auto_process": true
   }
   ```
   **Expected:** `201 Created` with `status: "success"`

2. **Refund Payment:**
   ```
   PUT http://localhost:5005/api/payments/1
   Body:
   {
     "action": "refund",
     "refund_amount": 70000
   }
   ```
   **Expected:** `200 OK`

---

## **MINIMAL TEST PLAN**

### **Phase 1: Verify Services Running (2 minutes)**
- [ ] Test all 5 health endpoints
- [ ] All return `200 OK`

### **Phase 2: Test CRUD Operations (10 minutes)**
- [ ] User Service: Create → Read → Update → Delete
- [ ] Restaurant Service: Create → Read → Update
- [ ] Order Service: Create → Update Status
- [ ] Delivery Service: Create → Update
- [ ] Payment Service: Create → Refund

### **Phase 3: Verify HTTP Methods (5 minutes)**
- [ ] GET - All services
- [ ] POST - All services
- [ ] PUT - All services
- [ ] DELETE - All services (optional)

---

## **WHY THIS WORKS**

### **Direct URLs:**
```
http://localhost:5001/api/users
http://localhost:5002/api/restaurants
http://localhost:5003/api/orders
http://localhost:5004/api/deliveries
http://localhost:5005/api/payments
```

### **Services Confirmed Running:**
```
API Gateway    → Port 5000 (running 1+ hour)
User Service   → Port 5001 (running 1+ hour)
Restaurant     → Port 5002 (running 1+ hour)
Order          → Port 5003 (running 1+ hour)
Delivery       → Port 5004 (running 1+ hour)
Payment        → Port 5005 (running 1+ hour)
```

---

## **IF YOU WANT TO USE API GATEWAY**

If you prefer to use the Gateway on port 5000, URLs must be:

```
http://localhost:5000/api/user-service/api/users
http://localhost:5000/api/restaurant-service/api/restaurants
http://localhost:5000/api/order-service/api/orders
http://localhost:5000/api/delivery-service/api/deliveries
http://localhost:5000/api/payment-service/api/payments
```

---

## **SUCCESS CRITERIA**

After testing with the new collection:

- [ ] All health checks return `200 OK`
- [ ] Can create users (POST)
- [ ] Can create restaurants with menu (POST)
- [ ] Can create orders (POST)
- [ ] Can update order status (PUT)
- [ ] Can create and process payments (POST)
- [ ] Can refund payments (PUT)
- [ ] Total successful requests: ~25+ (vs 0 before)

---

## **TAKE SCREENSHOTS**

After successful tests:
1. Postman collection structure (left sidebar)
2. Successful health checks (all green 200 OK)
3. Create User - 201 Created
4. Create Restaurant - 201 Created
5. Create Order - 201 Created
6. Create Payment - 201 OK with status: success

---

## **EXPECTED OUTCOME**

**Before:** 0/34 requests successful (100% failure)  
**After:** 25+/25 requests successful (100% success) 

---

**Total Testing Time:** ~15-20 minutes  
**File:** `POSTMAN_COLLECTION_DIRECT.json`  
**Status:** READY TO TEST! 
