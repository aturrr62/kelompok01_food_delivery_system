#!/usr/bin/env python3
"""
Generate Complete Postman Collection dengan Full CRUD untuk semua 5 microservices
"""

import json

def create_complete_collection():
    """Generate complete Postman collection dengan 56 endpoints"""
    
    collection = {
        "info": {
            "_postman_id": "food-delivery-complete-v2",
            "name": "Food Delivery System - COMPLETE API Collection",
            "description": "Complete Postman Collection with Full CRUD Operations (GET, POST, PUT, DELETE) for all 5 Microservices",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }
    
    # 1. Authentication
    collection["item"].append({
        "name": "1. API Gateway - Authentication",
        "item": [
            {
                "name": "POST - Login Admin",
                "event": [{
                    "listen": "test",
                    "script": {
                        "exec": [
                            "pm.test(\"Status code is 200\", function () { pm.response.to.have.status(200); });",
                            "if (pm.response.code === 200) {",
                            "    const jsonData = pm.response.json();",
                            "    pm.environment.set('admin_token', jsonData.access_token);",
                            "}"
                        ],
                        "type": "text/javascript"
                    }
                }],
                "request": {
                    "method": "POST",
                    "header": [{"key": "Content-Type", "value": "application/json"}],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({"username": "{{admin_username}}", "password": "{{admin_password}}"}, indent=2)
                    },
                    "url": {
                        "raw": "{{base_url}}/auth/login",
                        "host": ["{{base_url}}"],
                        "path": ["auth", "login"]
                    }
                }
            },
            {
                "name": "GET - Verify Token",
                "request": {
                    "method": "GET",
                    "header": [{"key": "Authorization", "value": "Bearer {{admin_token}}"}],
                    "url": {"raw": "{{base_url}}/auth/verify", "host": ["{{base_url}}"], "path": ["auth", "verify"]}
                }
            }
        ]
    })
    
    # 2. Health Check
    collection["item"].append({
        "name": "2. 🏥 System Health",
        "item": [{
            "name": "GET - Health Check",
            "request": {
                "method": "GET",
                "header": [],
                "url": {"raw": "{{base_url}}/health", "host": ["{{base_url}}"], "path": ["health"]}
            }
        }]
    })
    
    # 3. User Service - Full CRUD
    user_service_items = [
        ("GET - Get All Users", "GET", "/api/user-service/api/users", None),
        ("GET - Get User by ID", "GET", "/api/user-service/api/users/{{user_id}}", None),
        ("POST - Create User", "POST", "/api/user-service/api/users", {
            "username": "newuser{{$randomInt}}",
            "full_name": "New User",
            "email": "user{{$randomInt}}@example.com",
            "password": "SecurePass123!",
            "phone": "08123456789",
            "address": "Jl. Test No. 123",
            "user_type": "customer"
        }),
        ("PUT - Update User", "PUT", "/api/user-service/api/users/{{user_id}}", {
            "full_name": "Updated Name",
            "phone": "08199999999"
        }),
        ("DELETE - Hard Delete User", "DELETE", "/api/user-service/api/users/{{user_id}}", None),
        ("POST - Soft Delete User", "POST", "/api/user-service/api/users/{{user_id}}/soft-delete", None),
        ("POST - Restore User", "POST", "/api/user-service/api/users/{{user_id}}/restore", None),
        ("GET - Get All Profiles", "GET", "/api/user-service/api/profiles", None),
        ("POST - Create Profile", "POST", "/api/user-service/api/profiles", {
            "user_id": "{{user_id}}",
            "bio": "I love food!",
            "date_of_birth": "1990-01-01"
        }),
    ]
    
    user_items = []
    for name, method, path, body in user_service_items:
        request = {
            "method": method,
            "header": [{"key": "Authorization", "value": "Bearer {{admin_token}}"}],
            "url": {"raw": f"{{{{base_url}}}}{path}", "host": ["{{base_url}}"], "path": path.split('/')[1:]}
        }
        if body:
            request["header"].append({"key": "Content-Type", "value": "application/json"})
            request["body"] = {"mode": "raw", "raw": json.dumps(body, indent=2)}
        user_items.append({"name": name, "request": request})
    
    collection["item"].append({
        "name": "3. 👤 User Service - Full CRUD",
        "description": "Full CRUD Operations: GET, POST, PUT, DELETE",
        "item": user_items
    })
    
    # 4. Restaurant Service - Full CRUD
    restaurant_items = []
    
    # Restaurants
    rest_endpoints = [
        ("GET - Get All Restaurants", "GET", "/api/restaurant-service/api/restaurants", None),
        ("GET - Get Restaurant by ID", "GET", "/api/restaurant-service/api/restaurants/{{restaurant_id}}", None),
        ("POST - Create Restaurant", "POST", "/api/restaurant-service/api/restaurants", {
            "name": "Test Restaurant",
            "description": "Great food",
            "address": "Jl. Restaurant No. 1",
            "phone": "0812-3456789",
            "email": "restaurant@example.com"
        }),
        ("PUT - Update Restaurant", "PUT", "/api/restaurant-service/api/restaurants/{{restaurant_id}}", {
            "name": "Updated Restaurant Name",
            "description": "Even better food"
        }),
        ("POST - Soft Delete Restaurant", "POST", "/api/restaurant-service/api/restaurants/{{restaurant_id}}/soft-delete", None),
    ]
    
    # Menu Items
    menu_endpoints = [
        ("GET - Get All Menu Items", "GET", "/api/restaurant-service/api/menu-items", None),
        ("GET - Get Menu Item by ID", "GET", "/api/restaurant-service/api/menu-items/1", None),
        ("GET - Get Restaurant Menu", "GET", "/api/restaurant-service/api/restaurants/{{restaurant_id}}/menu", None),
        ("POST - Create Menu Item", "POST", "/api/restaurant-service/api/menu-items", {
            "restaurant_id": "{{restaurant_id}}",
            "name": "Nasi Goreng",
            "description": "Delicious fried rice",
            "price": 25000,
            "category": "main",
            "is_vegetarian": False,
            "is_available": True
        }),
        ("PUT - Update Menu Item", "PUT", "/api/restaurant-service/api/menu-items/1", {
            "name": "Nasi Goreng Special",
            "price": 30000
        }),
        ("PATCH - Partial Update Menu Item", "PATCH", "/api/restaurant-service/api/menu-items/1", {
            "price": 28000
        }),
        ("POST - Soft Delete Menu Item", "POST", "/api/restaurant-service/api/menu-items/1/soft-delete", None),
        ("DELETE - Hard Delete Menu Item", "DELETE", "/api/restaurant-service/api/menu-items/1", None),
        ("POST - Restore Menu Item", "POST", "/api/restaurant-service/api/menu-items/1/restore", None),
        ("POST - Filter Menu Items", "POST", "/api/restaurant-service/api/menu-items/filter", {
            "category": "main",
            "is_vegetarian": False
        }),
    ]
    
    for name, method, path, body in rest_endpoints + menu_endpoints:
        request = {
            "method": method,
            "header": [],
            "url": {"raw": f"{{{{base_url}}}}{path}", "host": ["{{base_url}}"], "path": path.split('/')[1:]}
        }
        if body:
            request["header"].append({"key": "Content-Type", "value": "application/json"})
            request["body"] = {"mode": "raw", "raw": json.dumps(body, indent=2)}
        restaurant_items.append({"name": name, "request": request})
    
    collection["item"].append({
        "name": "4. 🍽️ Restaurant Service - Full CRUD",
        "description": "Full CRUD for Restaurants and Menu Items",
        "item": restaurant_items
    })
    
    # 5. Order Service - Full CRUD
    order_items = []
    order_endpoints = [
        ("GET - Get All Orders", "GET", "/api/order-service/api/orders", None),
        ("GET - Get Order by ID", "GET", "/api/order-service/api/orders/{{order_id}}", None),
        ("POST - Create Order", "POST", "/api/order-service/api/orders", {
            "user_id": "{{user_id}}",
            "restaurant_id": "{{restaurant_id}}",
            "delivery_address": "Jl. Test No. 123",
            "total_amount": 150000,
            "delivery_fee": 10000,
            "items": [
                {"menu_item_id": 1, "quantity": 2, "price": 50000, "notes": "Extra spicy"}
            ]
        }),
        ("PUT - Update Order Status", "PUT", "/api/order-service/api/orders/{{order_id}}/status", {
            "status": "confirmed",
            "notes": "Order confirmed by restaurant"
        }),
        ("POST - Soft Delete Order", "POST", "/api/order-service/api/orders/{{order_id}}/soft-delete", None),
        ("DELETE - Hard Delete Order", "DELETE", "/api/order-service/api/orders/{{order_id}}", None),
        ("POST - Restore Order", "POST", "/api/order-service/api/orders/{{order_id}}/restore", None),
    ]
    
    for name, method, path, body in order_endpoints:
        request = {
            "method": method,
            "header": [],
            "url": {"raw": f"{{{{base_url}}}}{path}", "host": ["{{base_url}}"], "path": path.split('/')[1:]}
        }
        if body:
            request["header"].append({"key": "Content-Type", "value": "application/json"})
            request["body"] = {"mode": "raw", "raw": json.dumps(body, indent=2)}
        order_items.append({"name": name, "request": request})
    
    collection["item"].append({
        "name": "5. Order Service - Full CRUD",
        "description": "Full CRUD for Orders",
        "item": order_items
    })
    
    # 6. Delivery Service - Full CRUD
    delivery_items = []
    delivery_endpoints = [
        ("GET - Get All Deliveries", "GET", "/api/delivery-service/api/deliveries", None),
        ("GET - Get Delivery by ID", "GET", "/api/delivery-service/api/deliveries/{{delivery_id}}", None),
        ("POST - Create Delivery", "POST", "/api/delivery-service/api/deliveries", {
            "order_id": "{{order_id}}",
            "pickup_address": "Restaurant Address",
            "delivery_address": "Customer Address",
            "pickup_lat": -6.2088,
            "pickup_lng": 106.8456,
            "delivery_lat": -6.2000,
            "delivery_lng": 106.8300
        }),
        ("POST - Assign Courier", "POST", "/api/delivery-service/api/deliveries/{{delivery_id}}/assign-courier", {
            "courier_id": 1
        }),
        ("PUT - Update Location", "PUT", "/api/delivery-service/api/deliveries/{{delivery_id}}/location", {
            "latitude": -6.2044,
            "longitude": 106.8378,
            "status": "in_transit",
            "notes": "On the way to customer"
        }),
        ("GET - Track Delivery", "GET", "/api/delivery-service/api/deliveries/track/{{order_id}}", None),
        ("POST - Soft Delete Delivery", "POST", "/api/delivery-service/api/deliveries/{{delivery_id}}/soft-delete", None),
        ("POST - Restore Delivery", "POST", "/api/delivery-service/api/deliveries/{{delivery_id}}/restore", None),
        ("GET - Get All Couriers", "GET", "/api/delivery-service/api/couriers", None),
        ("POST - Create Courier", "POST", "/api/delivery-service/api/couriers", {
            "name": "Test Courier",
            "phone": "08123456789",
            "email": "courier@example.com",
            "vehicle_type": "motorcycle"
        }),
    ]
    
    for name, method, path, body in delivery_endpoints:
        request = {
            "method": method,
            "header": [],
            "url": {"raw": f"{{{{base_url}}}}{path}", "host": ["{{base_url}}"], "path": path.split('/')[1:]}
        }
        if body:
            request["header"].append({"key": "Content-Type", "value": "application/json"})
            request["body"] = {"mode": "raw", "raw": json.dumps(body, indent=2)}
        delivery_items.append({"name": name, "request": request})
    
    collection["item"].append({
        "name": "6. 🚚 Delivery Service - Full CRUD",
        "description": "Full CRUD for Deliveries and Couriers",
        "item": delivery_items
    })
    
    # 7. Payment Service - Full CRUD
    payment_items = []
    payment_endpoints = [
        ("GET - Get All Payments", "GET", "/api/payment-service/api/payments", None),
        ("GET - Get Payment by ID", "GET", "/api/payment-service/api/payments/{{payment_id}}", None),
        ("POST - Create Payment", "POST", "/api/payment-service/api/payments", {
            "order_id": "{{order_id}}",
            "user_id": "{{user_id}}",
            "amount": 160000,
            "payment_method": "credit_card",
            "payment_provider": "xendit"
        }),
        ("POST - Process Payment", "POST", "/api/payment-service/api/payments/{{payment_id}}/process", {
            "card_number": "4111111111111111",
            "cvv": "123",
            "expiry_month": "12",
            "expiry_year": "2025"
        }),
        ("POST - Create Refund", "POST", "/api/payment-service/api/payments/{{payment_id}}/refund", {
            "amount": 160000,
            "reason": "Customer cancelled order"
        }),
        ("POST - Soft Delete Payment", "POST", "/api/payment-service/api/payments/{{payment_id}}/soft-delete", None),
        ("POST - Restore Payment", "POST", "/api/payment-service/api/payments/{{payment_id}}/restore", None),
        ("GET - Get Payment Methods", "GET", "/api/payment-service/api/payment-methods?user_id={{user_id}}", None),
        ("POST - Create Payment Method", "POST", "/api/payment-service/api/payment-methods", {
            "user_id": "{{user_id}}",
            "name": "My Credit Card",
            "type": "credit_card",
            "card_number": "4111111111111111",
            "card_holder": "John Doe",
            "expiry_month": "12",
            "expiry_year": "2025"
        }),
    ]
    
    for name, method, path, body in payment_endpoints:
        request = {
            "method": method,
            "header": [],
            "url": {"raw": f"{{{{base_url}}}}{path}", "host": ["{{base_url}}"], "path": path.split('/')[1:]}
        }
        if body:
            request["header"].append({"key": "Content-Type", "value": "application/json"})
            request["body"] = {"mode": "raw", "raw": json.dumps(body, indent=2)}
        payment_items.append({"name": name, "request": request})
    
    collection["item"].append({
        "name": "7. 💳 Payment Service - Full CRUD",
        "description": "Full CRUD for Payments and Payment Methods",
        "item": payment_items
    })
    
    return collection

if __name__ == "__main__":
    print("🔨 Generating Complete Postman Collection...")
    collection = create_complete_collection()
    
    # Save to file
    output_file = "docs/POSTMAN_COLLECTION_COMPLETE.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)
    
    # Count endpoints
    total_endpoints = sum(len(folder["item"]) for folder in collection["item"])
    print(f"Generated {total_endpoints} endpoints across {len(collection['item'])} services")
    print(f"Saved to: {output_file}")
    
    # Show summary
    print("\nSummary:")
    for folder in collection["item"]:
        print(f"   {folder['name']}: {len(folder['item'])} endpoints")
