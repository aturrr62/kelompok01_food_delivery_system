# 🍔 Food Delivery System - Microservices Architecture

> Complete food delivery platform built with Python Flask microservices architecture

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Team](#team)
- [License](#license)

---

## 🎯 About

Food Delivery System adalah platform pemesanan makanan online yang dibangun menggunakan **microservices architecture**. Sistem ini dirancang untuk memberikan pengalaman yang seamless dalam memesan makanan, tracking pengiriman, dan pembayaran online.

**Key Highlights:**
- ✅ 5 Independent Microservices
- ✅ RESTful API dengan standar 4 HTTP Methods
- ✅ JWT Authentication
- ✅ Real-time Order Tracking
- ✅ Multiple Payment Methods
- ✅ Responsive Web Interface

---

## ✨ Features

### 👤 User Management
- User registration & authentication
- Profile management
- Role-based access (Customer, Merchant, Admin)
- JWT token-based security

### 🍽️ Restaurant & Menu
- Restaurant listing & search
- Dynamic menu management
- Rating & reviews
- Menu categories

### 📦 Order Processing
- Cart management
- Order creation with multiple items
- Real-time status tracking
- Order history

### 🚚 Delivery Tracking
- Live delivery status
- Courier assignment
- GPS location tracking
- Estimated delivery time

### 💳 Payment Processing
- Multiple payment methods (Credit Card, E-Wallet, COD)
- Automatic payment processing
- Refund management
- Transaction history

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    API Gateway (5000)                    │
│                  Central Entry Point                     │
└──────────┬──────────┬──────────┬──────────┬─────────────┘
           │          │          │          │
     ┌─────▼────┐ ┌──▼────┐ ┌──▼────┐ ┌───▼────┐ ┌────▼────┐
     │  User    │ │Restaurant│Order  │ │Delivery│ │ Payment │
     │ Service  │ │ Service │Service │ │Service │ │ Service │
     │  :5001   │ │  :5002  │ :5003  │ │ :5004  │ │  :5005  │
     └──────────┘ └─────────┘└────────┘ └────────┘ └─────────┘
          │            │         │           │          │
     ┌────▼────────────▼─────────▼───────────▼──────────▼────┐
     │                SQLite Databases                        │
     └──────────────────────────────────────────────────────┘
```

### Microservices

| Service | Port | Responsibility | Endpoints |
|---------|------|----------------|-----------|
| **API Gateway** | 5000 | Request routing, authentication | `/api/*` |
| **User Service** | 5001 | User management, auth | `/api/users` |
| **Restaurant Service** | 5002 | Restaurant & menu | `/api/restaurants` |
| **Order Service** | 5003 | Order processing | `/api/orders` |
| **Delivery Service** | 5004 | Delivery tracking | `/api/deliveries` |
| **Payment Service** | 5005 | Payment processing | `/api/payments` |

---

## 🛠️ Tech Stack

### Backend
- **Language:** Python 3.8+
- **Framework:** Flask 2.0+
- **Database:** SQLite (Development) / PostgreSQL (Production-ready)
- **Authentication:** JWT (Flask-JWT-Extended)
- **ORM:** SQLAlchemy

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling
- **JavaScript** - Interactivity
- **Fetch API** - HTTP requests

### Tools & Testing
- **Postman** - API testing
- **Git** - Version control
- **GitHub** - Repository hosting

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aturrr62/kelompok01_food_delivery_system.git
   cd kelompok01_food_delivery_system
   ```

2. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy flask-jwt-extended flask-cors
   ```

3. **Start services manually** (6 different terminals)

   **Terminal 1 - API Gateway:**
   ```bash
   cd microservices/api-gateway
   python app.py
   ```

   **Terminal 2 - User Service:**
   ```bash
   cd microservices/user-service
   python app.py
   ```

   **Terminal 3 - Restaurant Service:**
   ```bash
   cd microservices/restaurant-service
   python app.py
   ```

   **Terminal 4 - Order Service:**
   ```bash
   cd microservices/order-service
   python app.py
   ```

   **Terminal 5 - Delivery Service:**
   ```bash
   cd microservices/delivery-service
   python app.py
   ```

   **Terminal 6 - Payment Service:**
   ```bash
   cd microservices/payment-service
   python app.py
   ```

4. **Open Frontend**
   ```bash
   cd frontend
   python -m http.server 8080
   ```

5. **Access the application**
   - Frontend: http://localhost:8080
   - API Gateway: http://localhost:5000
   - User Service: http://localhost:5001
   - Restaurant Service: http://localhost:5002
   - Order Service: http://localhost:5003
   - Delivery Service: http://localhost:5004
   - Payment Service: http://localhost:5005

---

## 📚 API Documentation

### RESTful API Design

All microservices follow a **consistent 4 HTTP methods** pattern:

| Method | Purpose | Example |
|--------|---------|---------|
| **GET** | Retrieve resources | `GET /api/users` |
| **POST** | Create new resource | `POST /api/orders` |
| **PUT** | Update resource | `PUT /api/restaurants/1` |
| **DELETE** | Delete resource | `DELETE /api/payments/1` |

### Example API Calls

#### User Login
```bash
POST http://localhost:5001/api/users
Content-Type: application/json

{
  "action": "login",
  "username": "customer@example.com",
  "password": "password123"
}
```

#### Create Order
```bash
POST http://localhost:5003/api/orders
Content-Type: application/json

{
  "user_id": 1,
  "restaurant_id": 1,
  "delivery_address": "Jl. Example No. 123",
  "items": [
    {
      "menu_item_id": 1,
      "quantity": 2,
      "unit_price": 25000
    }
  ]
}
```

#### Update Order Status
```bash
PUT http://localhost:5003/api/orders/1
Content-Type: application/json

{
  "status": "confirmed"
}
```

### Complete API Documentation

For detailed API documentation, see:
- **Postman Collection:** `docs/POSTMAN_COLLECTION_DIRECT.json`
- **Postman Environment:** `docs/POSTMAN_ENVIRONMENT.json`
- **API Testing Guide:** `docs/API_TESTING_GUIDE.md`

---

## 🧪 Testing

### Using Postman

1. **Import Collection**
   - Open Postman
   - Import `docs/POSTMAN_COLLECTION_DIRECT.json`
   - Import `docs/POSTMAN_ENVIRONMENT.json`

2. **Select Environment**
   - Choose "Food Delivery - Local" environment

3. **Run Tests**
   - Start with Health Checks folder
   - Test each service sequentially
   - Follow the order: User → Restaurant → Order → Delivery → Payment

### Health Check

Verify all services are running:

```bash
# API Gateway
curl http://localhost:5000/health

# User Service
curl http://localhost:5001/health

# Restaurant Service
curl http://localhost:5002/health

# Order Service
curl http://localhost:5003/health

# Delivery Service
curl http://localhost:5004/health

# Payment Service
curl http://localhost:5005/health
```

All should return:
```json
{
  "status": "healthy",
  "service": "service-name",
  "timestamp": "2025-11-28T..."
}
```

---

## 📁 Project Structure

```
food_delivery_system/
├── microservices/
│   ├── api-gateway/
│   │   ├── app.py
│   │   └── swagger_config.py
│   ├── user-service/
│   │   ├── app.py
│   │   └── USER_SERVICE_GUIDE.md
│   ├── restaurant-service/
│   │   └── app.py
│   ├── order-service/
│   │   └── app.py
│   ├── delivery-service/
│   │   └── app.py
│   └── payment-service/
│       └── app.py
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
├── docs/
│   ├── POSTMAN_COLLECTION_DIRECT.json
│   ├── POSTMAN_ENVIRONMENT.json
│   ├── API_TESTING_GUIDE.md
│   └── SETUP_GUIDE.md
├── scripts/
│   ├── start_all.py
│   └── setup.sh
├── .gitignore
└── README.md
```

---


---

## 📝 Documentation

- [API Testing Guide](docs/API_TESTING_GUIDE.md)
- [Setup Guide](docs/SETUP_GUIDE.md)
- [Postman Tutorial](docs/POSTMAN_TUTORIAL_LENGKAP.md)
- [Running Guide](docs/CARA_MENJALANKAN_PROGRAM.md)

---

## 🎯 Key Achievements

- ✅ **100% RESTful API Compliance** - All services follow 4 HTTP methods pattern
- ✅ **Microservices Architecture** - Independent, scalable services
- ✅ **Complete CRUD Operations** - Full Create, Read, Update, Delete functionality
- ✅ **Authentication & Authorization** - JWT-based security
- ✅ **Clean Code** - Well-documented and maintainable
- ✅ **Production Ready** - Error handling, validation, logging

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Flask Framework - https://flask.palletsprojects.com/
- SQLAlchemy ORM - https://www.sqlalchemy.org/
- JWT Authentication - https://jwt.io/
- Postman API Testing - https://www.postman.com/

---

## 📧 Contact

For questions or support, please contact:
- **Email:** your.email@example.com
- **GitHub Issues:** [Create an issue](https://github.com/aturrr62/kelompok01_food_delivery_system/issues)

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by Kelompok 01

</div>
