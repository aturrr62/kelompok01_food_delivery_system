import requests
import json

BASE = "http://localhost:5000"

# Step 1: Login
print("=" * 60)
print("DETAILED ERROR DEBUGGING")
print("=" * 60)

resp = requests.post(f"{BASE}/auth/login", json={"username": "admin", "password": "admin123"})
print(f"\n1. Login: {resp.status_code}")
token = resp.json()['access_token']

# Step 2: Try all methods on /auth/verify
print(f"\n2. Testing /auth/verify with different methods:")
headers = {"Authorization": f"Bearer {token}"}

print(f"   GET: ", end="")
try:
    r = requests.get(f"{BASE}/auth/verify", headers=headers)
    print(f"{r.status_code} - {r.text[:100]}")
except Exception as e:
    print(f"ERROR: {e}")

print(f"   POST: ", end="")
try:
    r = requests.post(f"{BASE}/auth/verify", headers=headers)
    print(f"{r.status_code} - {r.text[:100]}")
except Exception as e:
    print(f"ERROR: {e}")

# Step 3: Test proxy endpoint
print(f"\n3. Testing /api/user-service/api/users:")
try:
    r = requests.get(f"{BASE}/api/user-service/api/users", headers=headers)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.text[:200]}")
except Exception as e:
    print(f"   ERROR: {e}")

print("\n" + "=" * 60)
