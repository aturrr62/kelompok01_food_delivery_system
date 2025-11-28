# 🔧 USER SERVICE - STARTUP & VERIFICATION GUIDE

**Last Updated:** 28 Nov 2025 10:37 WIB  
**Status:** Service Running ✅

---

## 🚀 **QUICK START**

### **Method 1: Using Startup Script** ⭐ RECOMMENDED

```powershell
cd microservices\user-service
.\start_service.bat
```

**Expected Output:**
```
========================================
  STARTING USER SERVICE
========================================

[1/3] Checking dependencies...
[2/3] Starting User Service on port 5001...

Health Check: http://localhost:5001/health
API Endpoints: http://localhost:5001/api/users

Press Ctrl+C to stop the service
========================================

✅ User Service tables created
👤 User Service starting on port 5001
* Running on http://127.0.0.1:5001
```

---

### **Method 2: Manual Start**

```powershell
cd c:\xampp\htdocs\food_delivery_system\microservices\user-service
python app.py
```

---

## ✅ **VERIFICATION STEPS**

### **Step 1: Check Health Endpoint (Critical)**

```powershell
curl http://localhost:5001/health
```

**✅ Expected Response:**
```json
{
  "status": "healthy",
  "service": "user-service",
  "timestamp": "2025-11-28T03:37:26..."
}
```

**❌ If ECONNREFUSED:**
- Service is not running
- Run `start_service.bat`
- Check port not in use: `netstat -ano | findstr :5001`

---

### **Step 2: Create New User (Unique Data)**

**⚠️ AVOID 409 Conflict by using UNIQUE data:**

**Test User #1:**
```powershell
curl -X POST http://localhost:5001/api/users ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"alice2025\",\"email\":\"alice@foodapp.com\",\"password\":\"Alice@123\",\"full_name\":\"Alice Johnson\",\"phone\":\"08111222333\",\"user_type\":\"customer\"}"
```

**Test User #2:**
```powershell
curl -X POST http://localhost:5001/api/users ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"bob_merchant\",\"email\":\"bob@restaurant.com\",\"password\":\"Bob@456\",\"full_name\":\"Bob Smith\",\"phone\":\"08222333444\",\"user_type\":\"merchant\"}"
```

**Test User #3:**
```powershell
curl -X POST http://localhost:5001/api/users ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"charlie_admin\",\"email\":\"charlie@admin.com\",\"password\":\"Admin@789\",\"full_name\":\"Charlie Brown\",\"phone\":\"08333444555\",\"user_type\":\"admin\"}"
```

**✅ Expected Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "alice2025",
    "email": "alice@foodapp.com",
    "full_name": "Alice Johnson",
    "user_type": "customer",
    "is_active": true,
    ...
  },
  "message": "User created successfully"
}
```

**❌ If 409 Conflict:**
```json
{
  "success": false,
  "error": "Username or email already exists"
}
```
**Solution:** Use different username & email (see unique test data below)

---

### **Step 3: Test Login**

```powershell
curl -X POST http://localhost:5001/api/users ^
  -H "Content-Type: application/json" ^
  -d "{\"action\":\"login\",\"username\":\"alice2025\",\"password\":\"Alice@123\"}"
```

**✅ Expected Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "alice2025",
      ...
    },
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "Login successful"
}
```

---

### **Step 4: Get All Users**

```powershell
curl http://localhost:5001/api/users
```

**✅ Expected Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "username": "alice2025",
      ...
    }
  ],
  "count": 1
}
```

---

## 🧪 **UNIQUE TEST DATA GENERATOR**

Use these to avoid 409 conflicts:

### **Set 1: Customer Users**
```json
{
  "username": "user_2025_001",
  "email": "user001@fooddelivery.test",
  "password": "Pass@2025",
  "full_name": "Test User 001",
  "phone": "08111000001",
  "user_type": "customer"
}
```

```json
{
  "username": "customer_jane",
  "email": "jane.doe@email.test",
  "password": "Jane@Secure123",
  "full_name": "Jane Doe",
  "phone": "08122111222",
  "user_type": "customer"
}
```

### **Set 2: Merchant Users**
```json
{
  "username": "resto_owner_01",
  "email": "owner@warungpadang.test",
  "password": "Merchant@2025",
  "full_name": "Restaurant Owner",
  "phone": "08133222333",
  "user_type": "merchant"
}
```

### **Set 3: Admin Users**
```json
{
  "username": "admin_system",
  "email": "admin@foodsys.test",
  "password": "Admin@Secure456",
  "full_name": "System Administrator",
  "phone": "08144333444",
  "user_type": "admin"
}
```

---

## 🔍 **TROUBLESHOOTING**

### **Problem 1: Service Won't Start**

**Error:** `python: command not found` or `Python was not found`  
**Solution:**
```powershell
# Check Python installation
python --version

# Should show: Python 3.7+ 
# If not, install Python from python.org
```

---

### **Problem 2: Port Already in Use**

**Error:** `OSError: [Errno 48] Address already in use`  
**Solution:**
```powershell
# Find process using port 5001
netstat -ano | findstr :5001

# Kill the process (replace PID)
taskkill /PID <PID_NUMBER> /F

# Restart service
python app.py
```

---

### **Problem 3: Module Not Found**

**Error:** `ModuleNotFoundError: No module named 'flask'`  
**Solution:**
```powershell
pip install flask flask-sqlalchemy flask-jwt-extended
```

---

### **Problem 4: Database Locked**

**Error:** `sqlite3.OperationalError: database is locked`  
**Solution:**
```powershell
# Stop all services
# Delete database file
del instance\user_service.db

# Restart service (will recreate fresh database)
python app.py
```

---

### **Problem 5: 409 Conflict**

**Error:** `"Username or email already exists"`  
**Solution:**
- Use unique username & email
- Or delete existing user first:
```powershell
curl -X DELETE http://localhost:5001/api/users/1
```

---

## 📊 **VERIFICATION CHECKLIST**

After startup, verify:

- [ ] ✅ Health check returns 200 OK
- [ ] ✅ Can create new user (201 Created)
- [ ] ✅ Can login with created user (200 OK with token)
- [ ] ✅ Can get all users (200 OK with array)
- [ ] ✅ No errors in terminal/console log
- [ ] ✅ Database file created (`instance/user_service.db`)

---

## 🚦 **STATUS INDICATORS**

### **✅ Service is Healthy:**
```
- Health check returns 200
- Can create/read users
- Login returns JWT token
- No errors in logs
```

### **⚠️ Service has Issues:**
```
- ECONNREFUSED on health check
- 500 errors on requests
- Syntax errors in console
- Database locked errors
```

### **❌ Service is Down:**
```
- No response on port 5001
- Process not in task manager
- Terminal shows exit/crash
```

---

## 📝 **LOG MONITORING**

**Watch for these in terminal:**

**✅ Good Signs:**
```
✅ User Service tables created
👤 User Service starting on port 5001
* Running on http://127.0.0.1:5001
127.0.0.1 - - [28/Nov/2025] "GET /health HTTP/1.1" 200 -
127.0.0.1 - - [28/Nov/2025] "POST /api/users HTTP/1.1" 201 -
```

**❌ Bad Signs:**
```
Traceback (most recent call last):
  File "app.py", line ...
ModuleNotFoundError: No module named 'flask'

OSError: [Errno 48] Address already in use

sqlite3.OperationalError: database is locked
```

---

## 🎯 **QUICK HEALTH CHECK COMMAND**

```powershell
# Single command to test everything
curl http://localhost:5001/health && echo. && echo SERVICE IS HEALTHY ✅ || echo SERVICE IS DOWN ❌
```

---

##  **FILES CREATED**

1. `start_service.bat` - Automated startup script
2. `USER_SERVICE_GUIDE.md` - This guide
3. `instance/user_service.db` - SQLite database (auto-created)

---

## 🔗 **QUICK LINKS**

- **Health Check:** http://localhost:5001/health
- **API Base:** http://localhost:5001/api/users
- **Documentation:** `ENDPOINT_TESTING_GUIDE.md`
- **Postman Collection:** `docs/POSTMAN_COLLECTION_DIRECT.json`

---

**Status:** ✅ **SERVICE OPERATIONAL**  
**Port:** 5001  
**Database:** SQLite (instance/user_service.db)  
**Dependencies:** Flask, SQLAlchemy, JWT-Extended

---

**Created:** 28 Nov 2025  
**Last Tested:** Working ✅
