import requests
import json

BASE_URL = "http://localhost:5000"

def test_endpoints():
    print("="*60)
    print("DETAILED API ENDPOINT TESTING")
    print("="*60)
    
    # Test 1: Login
    print("\n1. Testing /auth/login...")
    try:
        resp = requests.post(f"{BASE_URL}/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })
        print(f"   Status: {resp.status_code}")
        print(f"   Response: {json.dumps(resp.json(), indent=2)}")
        
        if resp.status_code != 200:
            print("   Login failed!")
            return
        
        token = resp.json().get('access_token')
        if not token:
            print("   No token received!")
            return
        
        print(f"   Token: {token[:50]}...")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test 2: Verify Token
        print("\n2. Testing /auth/verify...")
        resp = requests.post(f"{BASE_URL}/auth/verify", headers=headers)
        print(f"   Status: {resp.status_code}")
        print(f"   Response: {resp.text[:200]}")
        
        # Test 3: Get All Users (via proxy)
        print("\n3. Testing /api/user-service/api/users...")
        resp = requests.get(f"{BASE_URL}/api/user-service/api/users", headers=headers)
        print(f"   Status: {resp.status_code}")
        print(f"   Response: {resp.text[:200]}")
        
        # Test 4: Direct to User Service
        print("\n4. Testing User Service directly (http://localhost:5001/api/users)...")
        try:
            resp = requests.get("http://localhost:5001/api/users", headers=headers)
            print(f"   Status: {resp.status_code}")
            print(f"   Response: {resp.text[:200]}")
        except Exception as e:
            print(f"   Error: {e}")
        
        print("\n" + "="*60)
        print("TEST COMPLETED")
        print("="*60)
        
    except Exception as e:
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_endpoints()
