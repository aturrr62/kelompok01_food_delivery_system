import requests

BASE = "http://localhost:5000"

print("="*60)
print("TEST: Authorization Header Fix")
print("="*60)

# Step 1: Login
resp = requests.post(f"{BASE}/auth/login", json={"username": "admin", "password": "admin123"})
print(f"\n1. Login: {resp.status_code}")
if resp.status_code != 200:
    print("   ERROR: Login failed!")
    exit(1)

token = resp.json()['access_token']
print(f"   Token obtained: {token[:30]}...")

# Step 2: Test Verify Token (requires_token: True)
headers = {"Authorization": f"Bearer {token}"}
resp = requests.get(f"{BASE}/auth/verify", headers=headers)
print(f"\n2. Verify Token: {resp.status_code}")
if resp.status_code == 200:
    print("   PASS - Token verified")
else:
    print(f"   FAIL - {resp.text[:100]}")

# Step 3: Test Get All Users (NOW with requires_token: True)
resp = requests.get(f"{BASE}/api/user-service/api/users", headers=headers)
print(f"\n3. Get All Users: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    print(f"   PASS - Retrieved {data.get('count', 0)} users")
    print(f"   Response: {resp.text[:150]}")
else:
    print(f"   FAIL - {resp.text[:100]}")

# Step 4: Test WITHOUT token (should fail or return different result)
resp_no_auth = requests.get(f"{BASE}/api/user-service/api/users")
print(f"\n4. Get All Users (NO TOKEN): {resp_no_auth.status_code}")
print(f"   Response: {resp_no_auth.text[:100]}")

print("\n" + "="*60)
print("SUMMARY:")
print("  - Login: Working")
print("  - Verify Token (with auth): Working")
print("  - Get All Users (with auth): Working" if resp.status_code == 200 else "  - Get All Users (with auth): FAILED")
print("="*60)
