# Setup Guide - Food Delivery System

## Prerequisites

Sebelum memulai, pastikan sistem Anda memiliki:

### System Requirements
- **OS**: Windows 10/11, macOS 10.15+, atau Linux
- **Python**: 3.8+ (disarankan 3.9 atau 3.10)
- **Node.js**: 16+ (untuk frontend)
- **Git**: Latest version
- **RAM**: Minimal 4GB
- **Storage**: 2GB free space

### Software Dependencies
```bash
# Python packages akan otomatis terinstall via requirements.txt
# Flask, Flask-RESTX, Flask-JWT-Extended, requests, python-dotenv

# Frontend dependencies (optional, untuk development)
# TailwindCSS via CDN
# FontAwesome via CDN
```

## 🏗️ Installation Steps

### Step 1: Clone Repository
```bash
# Clone dari GitHub repository
git clone https://github.com/aturrr62/kelompok01_food_delivery_system.git

# Masuk ke directory project
cd food-delivery-system

# Cek struktur project
ls -la
```

### Step 2: Setup Environment
```bash
# Run setup script (Linux/Mac)
chmod +x scripts/setup.sh
./scripts/setup.sh

# Untuk Windows, jalankan manual:
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r microservices/service-template/requirements.txt
pip install -r microservices/api-gateway/requirements.txt

# Make scripts executable
chmod +x scripts/*.sh
chmod +x microservices/*/run.sh
```

### Step 3: Verify Installation
```bash
# Cek Python version
python --version  # Should be 3.8+

# Cek dependencies
pip list | grep Flask
pip list | grep JWT

# Verify structure
ls microservices/
ls scripts/
ls frontend/
```

## 🚦 Running the System

### Option 1: Auto Start (Recommended)
```bash
# Start semua services secara otomatis
./scripts/run-all.sh

# Output akan menampilkan:
# - API Gateway: http://localhost:5000
# - Frontend: http://localhost:5000 (via API Gateway)
# - Individual service URLs
```

### Option 2: Manual Start
```bash
# Terminal 1: Start API Gateway
cd microservices/api-gateway
python app.py
# Gateway berjalan di http://localhost:5000

# Terminal 2: Start User Service (ARTHUR - 5001)
cd microservices/user-service
python app.py
# User Service di http://localhost:5001

# Terminal 3: Start Restaurant Service (rizki - 5002)
cd microservices/restaurant-service
python app.py
# Restaurant Service di http://localhost:5002

# Terminal 4: Start Order Service (Nadia - 5003)
cd microservices/order-service
python app.py
# Order Service di http://localhost:5003

# Terminal 5: Start Delivery Service (aydin - 5004)
cd microservices/delivery-service
python app.py
# Delivery Service di http://localhost:5004

# Terminal 6: Start Payment Service (reza - 5005)
cd microservices/payment-service
python app.py
# Payment Service di http://localhost:5005
```

## Authentication Setup

### Demo Credentials
Sistem menyediakan 2 user demo:

```bash
# Admin Account
username: admin
password: admin123
role: admin

# Regular User Account
username: user
password: user123
role: user
```

### JWT Token Usage
```bash
# Get JWT Token
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Response:
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

# Use token for authenticated requests
curl -X GET http://localhost:5000/api/user-service/api/users \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Access Points

### Frontend URLs
- **Homepage**: http://localhost:5000/
- **Restaurant List**: http://localhost:5000/restaurant.html
- **Cart**: http://localhost:5000/cart.html
- **Checkout**: http://localhost:5000/checkout.html
- **Order Tracking**: http://localhost:5000/order-tracking.html
- **Admin Panel**: http://localhost:5000/admin.html

### API Endpoints
- **API Gateway Health**: http://localhost:5000/health
- **API Documentation**: http://localhost:5000/api-docs/
- **User Service**: http://localhost:5000/api/user-service/*
- **Restaurant Service**: http://localhost:5000/api/restaurant-service/*
- **Order Service**: http://localhost:5000/api/order-service/*
- **Delivery Service**: http://localhost:5000/api/delivery-service/*
- **Payment Service**: http://localhost:5000/api/payment-service/*

### Individual Service URLs
- **User Service**: http://localhost:5001
- **Restaurant Service**: http://localhost:5002
- **Order Service**: http://localhost:5003
- **Delivery Service**: http://localhost:5004
- **Payment Service**: http://localhost:5005

## Service-Specific Setup

### User Service (ARTHUR - Port 5001)
```bash
cd microservices/user-service
python app.py
```
**Endpoints**:
- GET `/api/users` - Get all users
- GET `/api/users/{id}` - Get user by ID
- POST `/api/users` - Create user
- PUT `/api/users/{id}` - Update user
- DELETE `/api/users/{id}/soft-delete` - Soft delete user

### Restaurant Service (rizki - Port 5002)
```bash
cd microservices/restaurant-service
python app.py
```
**Endpoints**:
- GET `/api/restaurants` - Get all restaurants
- POST `/api/restaurants` - Create restaurant
- GET `/api/menu-items` - Get all menu items
- POST `/api/menu-items` - Create menu item
- POST `/api/menu-items/filter` - Filter menu items

### Order Service (Nadia - Port 5003)
```bash
cd microservices/order-service
python app.py
```
**Endpoints**:
- GET `/api/orders` - Get all orders
- POST `/api/orders` - Create order
- GET `/api/orders/{id}` - Get order details

### Delivery Service (aydin - Port 5004)
```bash
cd microservices/delivery-service
python app.py
```
**Endpoints**:
- GET `/api/deliveries` - Get all deliveries
- POST `/api/deliveries` - Create delivery
- PUT `/api/deliveries/{id}` - Update delivery status

### Payment Service (reza - Port 5005)
```bash
cd microservices/payment-service
python app.py
```
**Endpoints**:
- GET `/api/payments` - Get all payments
- POST `/api/payments` - Create payment
- POST `/api/payments/{id}/process` - Process payment

## Testing Setup

### Using Postman
1. **Import Collection**:
   ```bash
   # Import Postman Collection
   # File: docs/POSTMAN_COLLECTION.json
   ```

2. **Setup Environment**:
   ```json
   {
     "base_url": "http://localhost:5000",
     "admin_token": "",  // Will be auto-set
     "user_token": ""    // Will be auto-set
   }
   ```

3. **Run Tests**:
   - Import collection ke Postman
   - Run test suite "Food Delivery System - UTS IAE"
   - Tests akan auto-login dan menjalankan semua endpoints

### Using cURL Commands
```bash
# Test API Gateway Health
curl http://localhost:5000/health

# Test Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Test User Service (authenticated)
TOKEN="your-jwt-token-here"
curl -X GET http://localhost:5000/api/user-service/api/users \
  -H "Authorization: Bearer $TOKEN"

# Test Restaurant Service
curl -X GET http://localhost:5000/api/restaurant-service/api/restaurants \
  -H "Authorization: Bearer $TOKEN"
```

## Database Structure

### User Service Database
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME
);
```

### Restaurant Service Database
```sql
CREATE TABLE restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    address VARCHAR(200),
    phone VARCHAR(20),
    email VARCHAR(120),
    rating DECIMAL(3,2) DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME
);

CREATE TABLE menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50),
    image_url VARCHAR(500),
    is_available BOOLEAN DEFAULT 1,
    is_vegetarian BOOLEAN DEFAULT 0,
    is_spicy BOOLEAN DEFAULT 0,
    preparation_time INTEGER,
    calories INTEGER,
    allergens TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);
```

### Order Service Database
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    delivery_address TEXT,
    special_instructions TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    menu_item_id INTEGER NOT NULL,
    menu_item_name VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
);
```

### Delivery Service Database
```sql
CREATE TABLE deliveries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER UNIQUE NOT NULL,
    delivery_address TEXT NOT NULL,
    delivery_person_name VARCHAR(100),
    delivery_person_phone VARCHAR(20),
    status VARCHAR(20) DEFAULT 'assigned',
    estimated_delivery_time DATETIME,
    actual_delivery_time DATETIME,
    delivery_fee DECIMAL(10,2) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

### Payment Service Database
```sql
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER UNIQUE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(20),
    status VARCHAR(20) DEFAULT 'pending',
    transaction_id VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

## Troubleshooting

### Common Issues & Solutions

#### 1. Port Already in Use
```bash
# Find process using port 5000
netstat -ano | findstr :5000
# atau
lsof -i :5000

# Kill process
taskkill /PID <PID> /F  # Windows
kill -9 <PID>           # Linux/Mac
```

#### 2. Python Dependencies Error
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt
pip install -r requirements.txt

# Clear pip cache
pip cache purge

# Use virtual environment
python -m venv new_venv
source new_venv/bin/activate  # Linux/Mac
new_venv\Scripts\activate     # Windows
```

#### 3. Database Not Found
```bash
# Check database files exist
ls microservices/*/database.db

# If missing, restart services (databases will be auto-created)
python app.py
```

#### 4. JWT Token Issues
```bash
# Check JWT secret key
echo $JWT_SECRET_KEY

# Reset demo data (optional)
rm microservices/*/database.db
# Restart all services
```

#### 5. Service Not Responding
```bash
# Check service health
curl http://localhost:5000/health

# Check individual services
curl http://localhost:5001/health  # User Service
curl http://localhost:5002/health  # Restaurant Service
# etc.

# Restart services
pkill -f "python app.py"  # Kill all Python processes
./scripts/run-all.sh       # Restart all
```

## Performance Optimization

### For Production
1. **Use Production Database**:
   ```bash
   # Replace SQLite with PostgreSQL/MySQL
   DATABASE_URL=postgresql://user:password@localhost:5432/fooddelivery
   ```

2. **Environment Variables**:
   ```bash
   # Set in .env file
   JWT_SECRET_KEY=your-production-secret-key
   SECRET_KEY=your-production-secret-key
   FLASK_ENV=production
   ```

3. **Use Gunicorn/UWSGI**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### For Development
1. **Enable Debug Mode**:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5000)
   ```

2. **Enable SQLAlchemy Logging**:
   ```python
   import logging
   logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
   ```

## Environment Variables

Create `.env` file in project root:
```bash
# API Gateway
JWT_SECRET_KEY=food-delivery-secret-key-change-in-production
SECRET_KEY=gateway-secret-key
FLASK_ENV=development

# Database URLs
USER_DB_URL=sqlite:///microservices/user-service/database.db
RESTAURANT_DB_URL=sqlite:///microservices/restaurant-service/database.db
ORDER_DB_URL=sqlite:///microservices/order-service/database.db
DELIVERY_DB_URL=sqlite:///microservices/delivery-service/database.db
PAYMENT_DB_URL=sqlite:///microservices/payment-service/database.db

# Service URLs
USER_SERVICE_URL=http://localhost:5001
RESTAURANT_SERVICE_URL=http://localhost:5002
ORDER_SERVICE_URL=http://localhost:5003
DELIVERY_SERVICE_URL=http://localhost:5004
PAYMENT_SERVICE_URL=http://localhost:5005

# Frontend
BASE_URL=http://localhost:5000
API_BASE_URL=http://localhost:5000
```

## Success Checklist

Setelah setup, pastikan semua checklist ini :

- [ ] Repository berhasil di-clone
- [ ] Python 3.8+ terinstall
- [ ] Virtual environment ter-setup
- [ ] Dependencies ter-install tanpa error
- [ ] API Gateway running di port 5000
- [ ] Semua 5 services running di port 5001-5005
- [ ] Health check returns "healthy"
- [ ] JWT authentication working
- [ ] Frontend accessible via browser
- [ ] Postman collection import berhasil
- [ ] Minimal satu test API berhasil

## 📞 Support

Jika mengalami masalah:

1. **Check Logs**: Lihat console output untuk error messages
2. **Check Documentation**: Baca `docs/API_DOCUMENTATION.md`
3. **Run Health Checks**: Gunakan endpoints `/health` untuk setiap service
4. **Restart Services**: Gunakan `./scripts/run-all.sh` untuk restart semua
5. **Check Network**: Pastikan tidak ada firewall yang memblokir ports

**Happy Testing! **