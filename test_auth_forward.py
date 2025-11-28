import requests
import json

BASE = "http://localhost:5000"
USER_SERVICE = "http://localhost:5001"

print("=== AUTHORIZATION HEADER FORWARDING TEST ===\n")

# Step 1: Login to get token
resp = requests.post(f"{BASE}/auth/login", json={"username": "admin", "password": "admin123"})
print(f"1. Login: {resp.status_code}")
token = resp.json()['access_token']
print(f"   Token: {token[:50]}...")

headers = {"Authorization": f"Bearer {token}"}

# Step 2: Test direct User Service call
print(f"\n2. Direct call to User Service (/api/users):")
try:
    resp = requests.get(f"{USER_SERVICE}/api/users", headers=headers)
    print(f"   Status: {resp.status_code}")
    print(f"   Response: {resp.text[:300]}")
except Exception as e:
    print(f"   ERROR: {e}")

# Step 3: Test through API Gateway proxy
print(f"\n3. Through API Gateway (/api/user-service/api/users):")
try:
    resp = requests.get(f"{BASE}/api/user-service/api/users", headers=headers)
    print(f"   Status: {resp.status_code}")
    print(f"   Response: {resp.text[:300]}")
except Exception as e:
    print(f"   ERROR: {e}")

# Step 4: Test without Authorization header
print(f"\n4. Without Authorization header:")
try:
    resp = requests.get(f"{USER_SERVICE}/api/users")
    print(f"   Status: {resp.status_code}")
    print(f"   Response: {resp.text[:300]}")
except Exception as e:
    print(f"   ERROR: {e}")

print("\n" + "="*50)
