import requests

BASE_URL = "http://localhost:5000"

print("Testing Food Delivery APIs")
print("-" * 50)

# Login
resp = requests.post(f"{BASE_URL}/auth/login", json={"username": "admin", "password": "admin123"})
print(f"1. Login: {resp.status_code}")

if resp.status_code == 200:
    token = resp.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # Verify Token
    resp = requests.post(f"{BASE_URL}/auth/verify", headers=headers)
    print(f"2. Verify Token: {resp.status_code}")
    
    # Get All Users
    resp = requests.get(f"{BASE_URL}/api/user-service/api/users", headers=headers)
    print(f"3. Get All Users: {resp.status_code}")
    
    # Health Check
    resp = requests.get(f"{BASE_URL}/health")
    print(f"4. Health Check: {resp.status_code}")
    
    # Non-existent
    resp = requests.get(f"{BASE_URL}/nonexistent")
    print(f"5. Non-existent: {resp.status_code}")
    
print("-" * 50)
print("All tests completed")
