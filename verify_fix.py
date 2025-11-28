import requests
import json

BASE_URL = "http://localhost:5000"

def test_api():
    print("1. Logging in...")
    try:
        resp = requests.post(f"{BASE_URL}/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })
        print(f"Login Status: {resp.status_code}")
        if resp.status_code != 200:
            print(resp.text)
            return

        data = resp.json()
        token = data.get('access_token')
        print("Token obtained.")

        headers = {"Authorization": f"Bearer {token}"}

        print("\n2. Verifying Token...")
        resp = requests.post(f"{BASE_URL}/auth/verify", headers=headers)
        print(f"Verify Status: {resp.status_code}")
        print(resp.text)

        print("\n3. Getting All Users...")
        resp = requests.get(f"{BASE_URL}/api/user-service/api/users", headers=headers)
        print(f"Get Users Status: {resp.status_code}")
        print(resp.text)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
