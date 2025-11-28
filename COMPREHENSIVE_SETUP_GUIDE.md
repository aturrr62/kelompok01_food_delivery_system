## COMPREHENSIVE SETUP & TESTING DOCUMENTATION
## Food Delivery System - Microservices Architecture

**Last Updated:** November 13, 2025  
**Status:** READY FOR TESTING  
**Author:** QA Team  

---

## TABLE OF CONTENTS

1. [Overview](#overview)
2. [Files Created](#files-created)
3. [Quick Start (3 Steps)](#quick-start-3-steps)
4. [Detailed Instructions](#detailed-instructions)
5. [Testing Guide](#testing-guide)
6. [Troubleshooting](#troubleshooting)
7. [Architecture](#architecture)

---

## OVERVIEW

Ini adalah **Food Delivery System** dengan microservices architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Port 8080)                     │
│              admin.html, index.html, etc.                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│          API GATEWAY (Port 5000) - Main Entry Point          │
│            • Authentication (JWT)                            │
│            • Request routing & forwarding                    │
│            • Error handling                                  │
│            • Swagger documentation                           │
└─────────────────────────────────────────────────────────────┘
    │          │           │          │          │
    ▼          ▼           ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│User    │ │Restau. │ │Order   │ │Delivery│ │Payment │
│Service │ │Service │ │Service │ │Service │ │Service │
│(5001)  │ │(5002)  │ │(5003)  │ │(5004)  │ │(5005)  │
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘
   │          │          │          │          │
   ▼          ▼          ▼          ▼          ▼
 user.db   rest.db    order.db   deliv.db   payment.db
```

**Key Features:**
- 6 independent microservices
- API Gateway with JWT authentication
- SQLite databases per service
- Flask-RESTX with Swagger documentation
- Comprehensive error handling
- CORS enabled for frontend integration

---

## 📁 FILES CREATED

### **1. START_ALL_SERVICES.ps1** 
**Purpose:** Start all 6 microservices in separate PowerShell windows

**What it does:**
```powershell
.\START_ALL_SERVICES.ps1
```

**Features:**
- Opens 6 new PowerShell windows (one per service)
- Auto-installs dependencies for each service
- Starts each service on its designated port
- Shows colored console output for easy monitoring
- Each window stays open for live log viewing

**Expected Output:**
```
Port 5000: API Gateway 
Port 5001: User Service 👤 (ARTHUR)
Port 5002: Restaurant Service 🍽️ (rizki)
Port 5003: Order Service (Nadia)
Port 5004: Delivery Service 🚚 (aydin)
Port 5005: Payment Service 💳 (reza)
```

---

### **2. TEST_ALL_APIS.py** 
**Purpose:** Comprehensive API testing with 25 test cases

**Usage:**
```powershell
python TEST_ALL_APIS.py full    # 25 comprehensive tests (5 min)
python TEST_ALL_APIS.py quick   # 5 basic tests (2 min)
python TEST_ALL_APIS.py debug   # Auth & health only (1 min)
```

**Test Coverage:**
| Category | Tests | Ports |
|----------|-------|-------|
| Health Check | 2 | 5000 |
| Authentication | 2 | 5000 |
| User Service | 5 | 5001 |
| Restaurant Service | 4 | 5002 |
| Order Service | 2 | 5003 |
| Delivery Service | 2 | 5004 |
| Payment Service | 3 | 5005 |
| Error Handling | 3 | Various |
| **TOTAL** | **25** | |

**Expected Results:**
- 25/25 tests pass (100% success rate)
- All HTTP status codes correct
- JSON responses valid
- Error handling working properly

---

### **3. HEALTH_CHECK.ps1** 🏥
**Purpose:** Diagnose system health and troubleshoot issues

**Modes:**
```powershell
.\HEALTH_CHECK.ps1 -Mode quick      # Port & process check
.\HEALTH_CHECK.ps1 -Mode detailed   # Full diagnostics
.\HEALTH_CHECK.ps1 -Mode cleanup    # Remove databases & kill processes
.\HEALTH_CHECK.ps1 -Mode monitor    # Real-time service monitoring
```

**Features:**
- Port availability check (5000-5005)
- Health endpoint verification
- Python process monitoring
- Database file validation
- Dependency verification
- Real-time monitoring mode
- Cleanup utilities

---

### **4. QUICK_START_GUIDE.md** 📖
**Purpose:** User-friendly step-by-step guide

**Contents:**
- 3-step quick start
- Detailed troubleshooting guide
- Common errors & solutions
- Manual verification steps
- Monitoring tips

---

## QUICK START (3 STEPS)

### **STEP 1: Open PowerShell**
```powershell
cd c:\xampp\htdocs\food_delivery_system
```

### **STEP 2: Start All Services**
```powershell
.\START_ALL_SERVICES.ps1
```

**What happens:**
- 6 PowerShell windows open
- Each runs one service
- Each service has its own port
- Dependencies auto-installed
- Wait 15-20 seconds for all to start

### **STEP 3: Run Tests**
```powershell
python TEST_ALL_APIS.py full
```

**Expected Output:**
```
Health Check                                  (200)
Login Admin                                  (200)
Get All Users                                (200)
Create User                                  (201)
... (25 tests total)
OVERALL RESULT: ALL TESTS PASSED! 🎊
```

---

## DETAILED INSTRUCTIONS

### **Architecture Check**

```
Project Structure:
├── microservices/
│   ├── api-gateway/          (Port 5000) - Main entry point
│   │   ├── app.py            - Flask app with routing
│   │   ├── swagger_config.py  - Swagger setup
│   │   └── requirements.txt   - Dependencies
│   │
│   ├── user-service/          (Port 5001) - User management
│   │   ├── app.py             - Flask app
│   │   └── requirements.txt    - Dependencies
│   │
│   ├── restaurant-service/    (Port 5002) - Restaurant management
│   │   ├── app.py
│   │   └── requirements.txt
│   │
│   ├── order-service/         (Port 5003) - Order management
│   │   ├── app.py
│   │   └── requirements.txt
│   │
│   ├── delivery-service/      (Port 5004) - Delivery tracking
│   │   ├── app.py
│   │   └── requirements.txt
│   │
│   └── payment-service/       (Port 5005) - Payment processing
│       ├── app.py
│       └── requirements.txt
│
├── frontend/                   - HTML/CSS/JS frontend
│   ├── index.html             - Main page
│   ├── admin.html             - Admin dashboard
│   ├── restaurant.html        - Restaurant page
│   └── js/                    - JavaScript files
│
├── docs/                       - Documentation
│   ├── openapi-spec-api-gateway.yaml
│   └── POSTMAN_COLLECTION.json
│
└── scripts/
    ├── START_ALL_SERVICES.ps1 - Start all services (NEW)
    ├── TEST_ALL_APIS.py       - Test suite (NEW)
    ├── HEALTH_CHECK.ps1       - Health diagnostics (NEW)
    └── QUICK_START_GUIDE.md   - This guide (NEW)
```

### **Port Usage**

| Port | Service | Description | Owner | Status |
|------|---------|-------------|-------|--------|
| 5000 | API Gateway | Main entry point, routing, auth | System | Required |
| 5001 | User Service | User management, authentication | ARTHUR | 👤 Required |
| 5002 | Restaurant Service | Restaurant & menu management | rizki | 🍽️ Required |
| 5003 | Order Service | Order processing | Nadia | Required |
| 5004 | Delivery Service | Delivery tracking | aydin | 🚚 Required |
| 5005 | Payment Service | Payment processing | reza | 💳 Required |

### **Testing Modes**

**1. Quick Test (2 minutes)**
```powershell
python TEST_ALL_APIS.py quick
```
- Tests: 5 basic endpoints
- Use for: Development & quick debugging
- Good for: CI/CD pipelines

**2. Full Test (5 minutes)**
```powershell
python TEST_ALL_APIS.py full
```
- Tests: All 25 endpoints
- Use for: Pre-deployment verification
- Good for: QA & client demos

**3. Debug Test (1 minute)**
```powershell
python TEST_ALL_APIS.py debug
```
- Tests: Auth & health only
- Use for: Troubleshooting connection issues
- Good for: Quick diagnostics

### **Manual API Testing**

If test script fails, verify manually:

```powershell
# 1. Health check
curl http://localhost:5000/health

# 2. Login
curl -X POST http://localhost:5000/auth/login `
  -H "Content-Type: application/json" `
  -d '{"username":"admin","password":"admin123"}'

# 3. List users
curl http://localhost:5001/api/users

# 4. List restaurants  
curl http://localhost:5002/api/restaurants

# 5. List orders
curl http://localhost:5003/api/orders
```

---

## TESTING GUIDE

### **Pre-Test Checklist**

```
Before running tests:
☐ All 6 services started (START_ALL_SERVICES.ps1)
☐ Wait 15-20 seconds for full startup
☐ No error messages in service windows
☐ All ports showing "Running on..."
☐ curl http://localhost:5000/health returns JSON
☐ Python 3.7+ installed
☐ requests module available (pip install requests)
```

### **Test Execution**

```powershell
# Option 1: Run full test suite
python TEST_ALL_APIS.py full

# Option 2: Run quick test
python TEST_ALL_APIS.py quick

# Option 3: Run debug test
python TEST_ALL_APIS.py debug

# Option 4: Monitor services while testing (in separate terminal)
.\HEALTH_CHECK.ps1 -Mode monitor
```

### **Interpreting Results**

**Good Signs:**
```
OVERALL RESULT: ALL TESTS PASSED! 🎊
PASSED: 25 (100%)
FAILED: 0 (0%)
```

**Warning Signs:**
```
 OVERALL RESULT: MOSTLY PASSING - Some issues to fix
PASSED: 20 (80%)
FAILED: 5 (20%)
```

**Problem Signs:**
```
🚨 OVERALL RESULT: SIGNIFICANT FAILURES - Major issues
PASSED: 2 (8%)
FAILED: 23 (92%)
```

### **Understanding Test Output**

Each test shows:
```
[1/25] Health Check...................................... (200)
       │    │           │                                    │
       │    │           │                                    └─ HTTP Status Code
       │    │           └─ Test name
       │    └─ Result (pass or fail)
       └─ Test number
```

---

## TROUBLESHOOTING

### **Problem 1: "Address already in use"**

**Symptoms:** `OSError: [WinError 10048] Only one usage of each socket address`

**Solution:**
```powershell
# Find process using port
netstat -ano | findstr :5000

# Kill process (replace XXXX with PID)
taskkill /PID XXXX /F

# Or use cleanup mode
.\HEALTH_CHECK.ps1 -Mode cleanup
```

### **Problem 2: "ModuleNotFoundError: No module named 'flask'"**

**Symptoms:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```powershell
# Manual pip install
cd microservices/api-gateway
pip install -r requirements.txt -q

cd ../user-service
pip install -r requirements.txt -q

# Repeat for all services...
```

### **Problem 3: "Connection refused"**

**Symptoms:** `requests.exceptions.ConnectionError`

**Solution:**
```powershell
# 1. Check services are running
.\HEALTH_CHECK.ps1 -Mode quick

# 2. Verify ports are listening
netstat -ano | findstr :5000
netstat -ano | findstr :5001

# 3. Check service logs in each window
# Look for errors

# 4. Wait longer before testing
Start-Sleep 30
python TEST_ALL_APIS.py quick
```

### **Problem 4: Database errors**

**Symptoms:** `sqlite3.OperationalError: no such table`

**Solution:**
```powershell
# Delete all database files
Remove-Item microservices/*/*.db -Force
Remove-Item microservices/*/instance/*.db -Force

# Restart services
.\START_ALL_SERVICES.ps1
```

### **Problem 5: 404 errors on all endpoints**

**Symptoms:** All tests return 404 NOT FOUND

**Likely Cause:** API Gateway not running, or routing misconfigured

**Solution:**
```powershell
# 1. Check if port 5000 is listening
Test-NetConnection -ComputerName localhost -Port 5000

# 2. Check process
Get-Process python | Where-Object {$_.CommandLine -like "*5000*"}

# 3. Restart API Gateway
.\START_ALL_SERVICES.ps1

# 4. Wait 10 seconds then test
Start-Sleep 10
python TEST_ALL_APIS.py debug
```

---

## 🏗️ ARCHITECTURE DETAILS

### **Request Flow**

```
Client Request
       │
       ▼
   HTTP Request (Port 5000)
       │
       ▼
   ┌─────────────────────────┐
   │  API Gateway            │
   │  • Auth check           │
   │  • Request validation   │
   │  • Route determination  │
   └─────────────────────────┘
       │
       ├─► /auth/*       ──► Internal auth handling
       ├─► /api/user/*   ──► Forward to localhost:5001
       ├─► /api/rest/*   ──► Forward to localhost:5002
       ├─► /api/order/*  ──► Forward to localhost:5003
       ├─► /api/deliv/*  ──► Forward to localhost:5004
       └─► /api/pay/*    ──► Forward to localhost:5005
       │
       ▼
   Microservice (Port 500X)
       │
       ▼
   SQLite Database
       │
       ▼
   Response JSON
       │
       ▼
   API Gateway Response
       │
       ▼
   Client Response
```

### **Service Communication**

**Synchronous (Direct HTTP):**
```
API Gateway
    ↓
User Service (5001)
    ↓
SQLite Database
```

**All services respond with:**
```json
{
    "success": true/false,
    "data": {...},
    "message": "..."
}
```

### **Authentication Flow**

```
1. Client POST /auth/login
   ├─ API Gateway verifies credentials
   ├─ Generates JWT token
   └─ Returns token to client

2. Client includes token in Authorization header
   Authorization: Bearer <token>

3. API Gateway verifies token
   ├─ If valid → Forward request to service
   └─ If invalid → Return 401 Unauthorized

4. Service processes request
   └─ Returns response
```

---

## SUCCESS CRITERIA

### **All Tests Passing (25/25)**

```
Health Check (2 tests)
   ├─ GET /health (200)
   └─ GET /api/nonexistent (404)

Authentication (2 tests)
   ├─ POST /auth/login (200)
   └─ GET /auth/verify (200)

User Service (5 tests)
   ├─ GET /api/user-service/api/users (200)
   ├─ POST /api/user-service/api/users (201)
   ├─ GET /api/user-service/api/users/1 (200)
   ├─ PUT /api/user-service/api/users/1 (200)
   └─ DELETE /api/user-service/api/users/2 (200)

Restaurant Service (4 tests)
   ├─ GET /api/restaurant-service/api/restaurants (200)
   ├─ POST /api/restaurant-service/api/restaurants (201)
   ├─ GET /api/restaurant-service/api/menu-items (200)
   └─ POST /api/restaurant-service/api/menu-items (201)

Order Service (2 tests)
   ├─ GET /api/order-service/api/orders (200)
   └─ POST /api/order-service/api/orders (201)

Delivery Service (2 tests)
   ├─ GET /api/delivery-service/api/deliveries (200)
   └─ POST /api/delivery-service/api/deliveries (201)

Payment Service (3 tests)
   ├─ GET /api/payment-service/api/payments (200)
   ├─ POST /api/payment-service/api/payments (201)
   └─ POST /api/payment-service/api/payments/1/process (200)

Error Handling (3 tests)
   ├─ POST /auth/login (invalid) (401)
   ├─ GET /api/user-service/api/users (unauthorized) (401/200)
   └─ GET /api/user-service/api/users/9999 (404)
```

---

## 📞 SUPPORT & NEXT STEPS

### **If tests PASS (25/25):**
- System is ready for production
- Frontend integration can proceed
- Load testing can begin
- Deployment planning can start

### **If tests FAIL partially:**
- Review TROUBLESHOOTING section
- Check service logs in each window
- Run `.\HEALTH_CHECK.ps1 -Mode detailed`
- Check database files exist
- Verify all ports are available

### **If tests FAIL completely:**
- 🚨 Run cleanup: `.\HEALTH_CHECK.ps1 -Mode cleanup`
- 🚨 Kill all Python: `Get-Process python | Stop-Process -Force`
- 🚨 Restart everything: `.\START_ALL_SERVICES.ps1`
- 🚨 Wait 30 seconds before testing again

---

## 📈 PERFORMANCE METRICS

**Expected Performance:**
- Health check response: < 10ms
- Login response: < 100ms
- Query response: < 500ms
- Create request: < 1000ms
- Database operations: < 200ms per request

**Resource Usage:**
- Per service memory: ~50-80MB
- Total Python memory: ~400-500MB
- Database size per service: ~100KB-1MB
- Total network bandwidth (test): ~2-5MB

---

## 🎓 LEARNING RESOURCES

**Key Concepts:**
1. **Microservices Architecture:** Decoupled, independently deployable services
2. **API Gateway Pattern:** Single entry point for all services
3. **JWT Authentication:** Stateless token-based security
4. **Request Forwarding:** Gateway proxies requests to services
5. **Error Handling:** Consistent error response format

**Files to Study:**
- `api-gateway/app.py` - Gateway implementation & routing
- `user-service/app.py` - Service implementation example
- `TEST_ALL_APIS.py` - Comprehensive API testing
- `swagger_config.py` - API documentation setup

---

## NOTES

- All services use SQLite (suitable for development/testing)
- For production: Use PostgreSQL/MySQL
- JWT tokens expire after 24 hours
- All responses are JSON format
- CORS enabled for frontend requests
- Error messages are descriptive for debugging

---

**Status:** READY FOR TESTING & DEPLOYMENT

**Last Updated:** November 13, 2025

**Questions?** Check QUICK_START_GUIDE.md or run `.\HEALTH_CHECK.ps1 -Mode detailed`
