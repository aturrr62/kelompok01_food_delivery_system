# API Testing Guide - Food Delivery System

## Overview

Dokumentasi ini memberikan panduan lengkap untuk melakukan testing API Food Delivery System menggunakan berbagai tools dan metode.

## Testing Objectives

- **Functional Testing**: Memastikan semua endpoint berfungsi dengan benar
- **Authentication Testing**: Memverifikasi sistem JWT authentication
- **Integration Testing**: Menguji komunikasi antar microservices
- **Error Handling**: Memastikan error handling yang proper
- **Performance Testing**: Memeriksa response time dan throughput

## Testing Tools

### 1. Postman Collection (Recommended)
**File**: `docs/POSTMAN_COLLECTION.json`

```bash
# Import ke Postman:
# 1. Buka Postman
# 2. Import Collection → Select docs/POSTMAN_COLLECTION.json
# 3. Set Environment Variables (optional)
```

### 2. cURL Commands
Manual testing dengan command line.

### 3. Browser Testing
Testing frontend dan API gateway endpoint.

## Authentication Setup

### Demo Credentials
```json
Admin Account:
{
  "username": "admin",
  "password": "admin123",
  "role": "admin"
}

User Account:
{
  "username": "user", 
  "password": "user123",
  "role": "user"
}
```

### Getting JWT Token
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Response**:
```json
{
  "success": true,
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@fooddelivery.com",
    "role": "admin"
  },
  "message": "Login successful"
}
```

### Using Token in Requests
```bash
# Set environment variable
export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Use in authenticated requests
curl -X GET http://localhost:5000/api/user-service/api/users \
  -H "Authorization: Bearer $TOKEN"
```

## Postman Testing Workflow

### Step 1: Import Collection
1. Buka **Postman Desktop** atau web version
2. Klik **Import** button
3. Pilih file `docs/POSTMAN_COLLECTION.json`
4. Collection akan muncul di sidebar left

### Step 2: Setup Environment (Optional)
```json
Environment: Development
Variables:
{
  "base_url": "http://localhost:5000",
  "admin_token": "",  // Auto-set by collection
  "user_token": "",   // Auto-set by collection
  "user_id": "",      // Auto-set by tests
  "restaurant_id": "",
  "order_id": "",
  "delivery_id": "",
  "payment_id": ""
}
```

### Step 3: Run Test Collection
1. **Select Collection**: "Food Delivery System - UTS IAE"
2. **Click Run**: Collection Runner atau Individual folder
3. **Review Results**: Check passed/failed tests
4. **Debug Failures**: Check console logs dan response data

### Step 4: Test Results Analysis
```bash
# Successful Test Indicators:
Status code is 200
Response has success field
Response has access_token
User created successfully

# Failed Test Indicators:
Status code is 4xx/5xx
Missing required fields
Authentication failed
Service unavailable
```

## Individual Endpoint Testing

### 1. API Gateway Health Check

#### Test Endpoint
```bash
GET http://localhost:5000/health
```

#### Expected Response (200)
```json
{
  "status": "healthy",
  "service": "api-gateway",
  "timestamp": "2024-11-12T16:00:00Z",
  "services": [
    "user-service",
    "restaurant-service", 
    "order-service",
    "delivery-service",
    "payment-service"
  ],
  "version": "1.0.0"
}
```

#### Test Cases
- [ ] Health check returns 200
- [ ] Status field is "healthy"
- [ ] Services array is present
- [ ] Version field is present

### 2. Authentication Endpoints

#### Test Login (Valid Credentials)
```bash
POST http://localhost:5000/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

#### Expected Response (200)
```json
{
  "success": true,
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@fooddelivery.com",
    "role": "admin"
  },
  "message": "Login successful"
}
```

#### Test Cases
- [ ] Login admin credentials returns 200
- [ ] Login user credentials returns 200
- [ ] Response contains access_token
- [ ] Token has proper structure (3 parts separated by dots)

#### Test Login (Invalid Credentials)
```bash
POST http://localhost:5000/auth/login
Content-Type: application/json

{
  "username": "invalid",
  "password": "wrong"
}
```

#### Expected Response (401)
```json
{
  "success": false,
  "message": "Invalid credentials"
}
```

#### Test Cases
- [ ] Invalid login returns 401
- [ ] Error message is clear
- [ ] No token is returned

### 3. User Service Testing

#### Setup
```bash
export TOKEN="your-jwt-token"
```

#### Test GET All Users
```bash
GET http://localhost:5000/api/user-service/api/users
Authorization: Bearer $TOKEN
```

#### Expected Response (200)
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Admin User",
      "email": "admin@fooddelivery.com",
      "phone": "",
      "address": "",
      "is_active": true,
      "created_at": "2024-11-12T16:00:00Z",
      "updated_at": "2024-11-12T16:00:00Z"
    }
  ],
  "count": 1,
  "message": "Users retrieved successfully"
}
```

#### Test POST Create User
```bash
POST http://localhost:5000/api/user-service/api/users
Content-Type: application/json
Authorization: Bearer $TOKEN

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "phone": "081234567890",
  "address": "Jl. Example No. 123"
}
```

#### Expected Response (201)
```json
{
  "success": true,
  "data": {
    "id": 2,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "081234567890",
    "address": "Jl. Example No. 123",
    "is_active": true,
    "created_at": "2024-11-12T16:01:00Z",
    "updated_at": "2024-11-12T16:01:00Z"
  },
  "message": "User created successfully"
}
```

#### Test GET User by ID
```bash
GET http://localhost:5000/api/user-service/api/users/1
Authorization: Bearer $TOKEN
```

#### Test Cases
- [ ] GET users returns 200
- [ ] Data is an array
- [ ] User objects have required fields
- [ ] POST create user returns 201
- [ ] New user has unique ID
- [ ] GET user by ID returns 200
- [ ] User data matches input

### 4. Restaurant Service Testing

#### Test GET All Restaurants
```bash
GET http://localhost:5000/api/restaurant-service/api/restaurants
Authorization: Bearer $TOKEN
```

#### Test POST Create Restaurant
```bash
POST http://localhost:5000/api/restaurant-service/api/restaurants
Content-Type: application/json
Authorization: Bearer $TOKEN

{
  "name": "Warung Bakso Malang",
  "description": "Bakso Malang autentik dengan kuah yang gurih",
  "address": "Jl. Malioboro No. 123, Yogyakarta",
  "phone": "0274-123456",
  "email": "info@warungbakso.com"
}
```

#### Test Menu Items Management
```bash
# Get all menu items
GET http://localhost:5000/api/restaurant-service/api/menu-items
Authorization: Bearer $TOKEN

# Create menu item
POST http://localhost:5000/api/restaurant-service/api/menu-items
Content-Type: application/json
Authorization: Bearer $TOKEN

{
  "restaurant_id": 1,
  "name": "Bakso Solo",
  "description": "Bakso daging sapi dengan kuah kaldu",
  "price": 25000,
  "category": "main",
  "is_vegetarian": false,
  "preparation_time": 15,
  "calories": 350
}
```

### 5. Order Service Testing

#### Test Create Order
```bash
POST http://localhost:5000/api/order-service/api/orders
Content-Type: application/json
Authorization: Bearer $TOKEN

{
  "user_id": 1,
  "restaurant_id": 1,
  "items": [
    {
      "menu_item_id": 1,
      "menu_item_name": "Bakso Solo",
      "quantity": 2,
      "price": 25000
    }
  ]
}
```

#### Expected Response (201)
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": 1,
    "restaurant_id": 1,
    "total_amount": 50000,
    "status": "pending",
    "delivery_address": "",
    "created_at": "2024-11-12T16:02:00Z"
  },
  "message": "Order created successfully"
}
```

### 6. Delivery Service Testing

#### Test Create Delivery
```bash
POST http://localhost:5000/api/delivery-service/api/deliveries
Content-Type: application/json
Authorization: Bearer $TOKEN

{
  "order_id": 1,
  "delivery_address": "Jl. Malioboro No. 123, Yogyakarta",
  "delivery_fee": 10000
}
```

### 7. Payment Service Testing

#### Test Create Payment
```bash
POST http://localhost:5000/api/payment-service/api/payments
Content-Type: application/json
Authorization: Bearer $TOKEN

{
  "order_id": 1,
  "amount": 60000,
  "payment_method": "credit_card"
}
```

#### Test Process Payment
```bash
POST http://localhost:5000/api/payment-service/api/payments/1/process
Authorization: Bearer $TOKEN
```

## Integration Testing

### End-to-End Workflow Test
```bash
# 1. Login to get token
TOKEN=$(curl -s -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | jq -r '.access_token')

# 2. Create user
USER_RESPONSE=$(curl -s -X POST http://localhost:5000/api/user-service/api/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "Test User", "email": "test@example.com", "password": "test123"}')
USER_ID=$(echo $USER_RESPONSE | jq -r '.data.id')

# 3. Create restaurant
RESTAURANT_RESPONSE=$(curl -s -X POST http://localhost:5000/api/restaurant-service/api/restaurants \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "Test Restaurant", "description": "Test Description", "address": "Test Address"}')
RESTAURANT_ID=$(echo $RESTAURANT_RESPONSE | jq -r '.data.id')

# 4. Create order
ORDER_RESPONSE=$(curl -s -X POST http://localhost:5000/api/order-service/api/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"user_id\": $USER_ID, \"restaurant_id\": $RESTAURANT_ID, \"items\": []}")
ORDER_ID=$(echo $ORDER_RESPONSE | jq -r '.data.id')

# 5. Create delivery
curl -s -X POST http://localhost:5000/api/delivery-service/api/deliveries \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"order_id\": $ORDER_ID, \"delivery_address\": \"Test Address\"}"

# 6. Create payment
PAYMENT_RESPONSE=$(curl -s -X POST http://localhost:5000/api/payment-service/api/payments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"order_id\": $ORDER_ID, \"amount\": 60000, \"payment_method\": \"credit_card\"}")
PAYMENT_ID=$(echo $PAYMENT_RESPONSE | jq -r '.data.id')

# 7. Process payment
curl -s -X POST http://localhost:5000/api/payment-service/api/payments/$PAYMENT_ID/process \
  -H "Authorization: Bearer $TOKEN"

echo "End-to-end test completed!"
echo "User ID: $USER_ID"
echo "Order ID: $ORDER_ID"
echo "Payment ID: $PAYMENT_ID"
```

## Error Handling Tests

### 1. Unauthorized Access Test
```bash
# Should return 401
curl -X GET http://localhost:5000/api/user-service/api/users
```

#### Expected Response (401)
```json
{
  "success": false,
  "error": "Authorization required",
  "message": "Please provide a valid JWT token"
}
```

### 2. Invalid Token Test
```bash
# Should return 401
curl -X GET http://localhost:5000/api/user-service/api/users \
  -H "Authorization: Bearer invalid-token"
```

#### Expected Response (401)
```json
{
  "success": false,
  "error": "Invalid token",
  "message": "Please provide a valid token"
}
```

### 3. Expired Token Test
```bash
# Create token with short expiry and test after expiry
# Should return 401
```

### 4. Service Unavailable Test
```bash
# Kill one service and test its endpoints
# Should return 503
curl -X GET http://localhost:5000/api/nonexistent-service/api/test \
  -H "Authorization: Bearer $TOKEN"
```

#### Expected Response (404)
```json
{
  "success": false,
  "error": "Service not found",
  "message": "Service 'nonexistent-service' is not available"
}
```

### 5. Validation Error Test
```bash
# Test with invalid data
curl -X POST http://localhost:5000/api/user-service/api/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "", "email": "invalid-email"}'
```

## Performance Testing

### Response Time Testing
```bash
# Test single request time
time curl -X GET http://localhost:5000/health

# Test concurrent requests (basic)
for i in {1..10}; do
  curl -X GET http://localhost:5000/health &
done
wait
```

### Load Testing with AB (Apache Bench)
```bash
# Install Apache Bench (if not available)
# sudo apt-get install apache2-utils  # Ubuntu/Debian
# brew install httpd  # macOS

# Basic load test
ab -n 100 -c 10 http://localhost:5000/health

# Test authenticated endpoint
ab -n 100 -c 10 -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/user-service/api/users
```

### Expected Performance Metrics
- **Response Time**: < 500ms for most endpoints
- **Throughput**: > 100 requests/second
- **Error Rate**: < 1% for healthy services
- **Memory Usage**: < 512MB per service

## Debugging Common Issues

### 1. Authentication Issues
```bash
# Check token structure
echo $TOKEN | cut -d'.' -f1 | base64 -d | jq

# Check token expiry
echo $TOKEN | cut -d'.' -f2 | base64 -d | jq '.exp'
```

### 2. Service Communication Issues
```bash
# Check service health directly
curl http://localhost:5001/health  # User Service
curl http://localhost:5002/health  # Restaurant Service
curl http://localhost:5003/health  # Order Service
curl http://localhost:5004/health  # Delivery Service
curl http://localhost:5005/health  # Payment Service

# Check API Gateway routing
curl -v http://localhost:5000/health
```

### 3. Database Issues
```bash
# Check if databases exist
ls -la microservices/*/database.db

# Check service logs for database errors
tail -f microservices/*/app.log
```

### 4. CORS Issues
```bash
# Test CORS preflight
curl -X OPTIONS http://localhost:5000/api/user-service/api/users \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: Authorization"
```

## 📈 Test Automation

### Create Test Scripts
```bash
#!/bin/bash
# test-api.sh - Automated API testing script

BASE_URL="http://localhost:5000"

echo "Starting API Tests..."

# Get admin token
echo "1. Testing Login..."
TOKEN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | jq -r '.access_token')

if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
  echo "Login failed!"
  exit 1
fi

echo "Login successful"

# Health check
echo "2. Testing Health Check..."
curl -s $BASE_URL/health | jq '.status' | grep -q "healthy"
if [ $? -eq 0 ]; then
  echo "Health check passed"
else
  echo "Health check failed"
fi

# Test authenticated endpoint
echo "3. Testing User Service..."
curl -s -X GET $BASE_URL/api/user-service/api/users \
  -H "Authorization: Bearer $TOKEN" | jq '.success' | grep -q "true"
if [ $? -eq 0 ]; then
  echo "User service accessible"
else
  echo "User service failed"
fi

echo "API Tests Completed!"
```

### Run Automated Tests
```bash
chmod +x test-api.sh
./test-api.sh
```

## Test Reports

### Manual Test Report Template
```markdown
## Test Report - Food Delivery System API

**Date**: [Date]
**Tester**: [Name]
**Environment**: Development

### Test Summary
- **Total Tests**: 45
- **Passed**: 42
- **Failed**: 3
- **Success Rate**: 93.3%

### Critical Issues Found
1. [Issue description]
2. [Issue description]

### Recommendations
1. [Recommendation]
2. [Recommendation]

### Test Details
| Test ID | Endpoint | Expected | Actual | Status |
|---------|----------|----------|--------|--------|
| TC001 | GET /health | 200 | 200 | |
| TC002 | POST /auth/login | 200 | 200 | |
| TC003 | GET /api/users | 401 | 401 | |
```

## Success Criteria

### Must Pass Tests
- [ ] Health check returns 200
- [ ] Login with admin credentials works
- [ ] Authentication required for protected endpoints
- [ ] CRUD operations work for all services
- [ ] Error handling returns proper status codes
- [ ] Service-to-service communication works
- [ ] Frontend can communicate with API Gateway

### Should Pass Tests
- [ ] Response times < 500ms
- [ ] Multiple concurrent requests handled
- [ ] CORS headers present
- [ ] Proper JSON responses
- [ ] Database operations succeed

### Nice to Have Tests
- [ ] Load testing under 100 concurrent users
- [ ] Rate limiting works
- [ ] Pagination works for large datasets
- [ ] File upload (if implemented)

## Conclusion

Dengan mengikuti panduan testing ini, Anda akan dapat:

1. **Memastikan sistem berfungsi** dengan benar
2. **Menganalisis performance** dan scalability
3. **Mengidentifikasi issues** sebelum production
4. **Mendokumentasikan bugs** untuk debugging
5. **Memvalidasi compliance** dengan requirements UTS IAE/EAI

**Happy Testing! **

---

**Next Steps**:
1. Import Postman collection
2. Run test suite
3. Analyze results
4. Fix any failed tests
5. Document findings

**For Support**: Check `docs/SETUP_GUIDE.md` untuk troubleshooting