import requests
import json

BASE = "http://localhost:5000"

print("=== QUICK DIAGNOSIS ===\n")

# Login
resp = requests.post(f"{BASE}/auth/login", json={"username": "admin", "password": "admin123"})
print(f"1. Login: {resp.status_code}")
if resp.status_code != 200:
    print(f"   ERROR: {resp.text}")
    exit(1)

token = resp.json()['access_token']
headers = {"Authorization": f"Bearer {token}"}

# Test Verify Token with GET
resp = requests.get(f"{BASE}/auth/verify", headers=headers)
print(f"2. Verify Token (GET): {resp.status_code}")
if resp.status_code != 200:
    print(f"   Response: {resp.text[:200]}")

# Test Get All Users
resp = requests.get(f"{BASE}/api/user-service/api/users", headers=headers)
print(f"3. Get All Users: {resp.status_code}")
if resp.status_code != 200:
    print(f"   Response: {resp.text[:200]}")
else:
    data = resp.json()
    print(f"   Success! Count: {data.get('count', 0)}")

# Test direct to User Service
resp = requests.get("http://localhost:5001/api/users", headers=headers)
print(f"4. Direct User Service: {resp.status_code}")
if resp.status_code != 200:
    print(f"   Response: {resp.text[:200]}")

print("\n=== DIAGNOSIS COMPLETE ===")
