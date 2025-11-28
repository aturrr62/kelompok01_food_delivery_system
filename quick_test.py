import requests

BASE = "http://localhost:5000"

# Login
resp = requests.post(f"{BASE}/auth/login", json={"username": "admin", "password": "admin123"})
print(f"Login: {resp.status_code}")

token = resp.json()['access_token']
headers = {"Authorization": f"Bearer {token}"}

# Test each endpoint
tests = [
    ("Health", "GET", f"{BASE}/health", {}),
    ("Verify Token", "GET", f"{BASE}/auth/verify", headers),
    ("Get All Users", "GET", f"{BASE}/api/user-service/api/users", headers),
]

print("\n" + "="*60)
for name, method, url, hdrs in tests:
    try:
        resp = requests.request(method, url, headers=hdrs)
        status = "" if resp.status_code == 200 else ""
        print(f"{status} {name:20s} {resp.status_code}")
        if resp.status_code != 200:
            print(f"   {resp.text[:100]}")
    except Exception as e:
        print(f"{name:20s} ERROR: {e}")
print("="*60)
