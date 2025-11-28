#!/usr/bin/env python3
"""Simple API Test Script"""

import requests
import json

BASE_URL = "http://localhost:5000"

def main():
    print("\n" + "="*70)
    print("  FOOD DELIVERY SYSTEM - API TEST")
    print("="*70 + "\n")
    
    # Test 1: Health Check
    print("1. Testing Health Check...")
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            print("   API Gateway is running")
        else:
            print("   Health check failed")
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Test 2: Login
    print("\n2. Testing Login...")
    try:
        resp = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": "admin", "password": "admin123"},
            timeout=5
        )
        print(f"   Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            token = data.get('access_token')
            print(f"   Login successful")
            print(f"   Token: {token[:50]}...")
        else:
            print(f"   Login failed")
            print(f"   Response: {resp.text}")
            return
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Test 3: Verify Token
    print("\n3. Testing Token Verification...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"{BASE_URL}/auth/verify", headers=headers, timeout=5)
        print(f"   Status: {resp.status_code}")
        
        if resp.status_code == 200:
            print(f"   Token is valid")
        else:
            print(f"   Token verification failed")
            print(f"   Response: {resp.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Get All Users
    print("\n4. Testing Get All Users...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"{BASE_URL}/api/user-service/api/users", headers=headers, timeout=5)
        print(f"   Status: {resp.status_code}")
        
        if resp.status_code == 200:
            users = resp.json()
            print(f"   Successfully retrieved users")
            print(f"   Total users: {len(users) if isinstance(users, list) else 'N/A'}")
        else:
            print(f"   Failed to get users")
            print(f"   Response: {resp.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Get All Restaurants
    print("\n5. Testing Get All Restaurants...")
    try:
        resp = requests.get(f"{BASE_URL}/api/restaurant-service/api/restaurants", timeout=5)
        print(f"   Status: {resp.status_code}")
        
        if resp.status_code == 200:
            restaurants = resp.json()
            print(f"   Successfully retrieved restaurants")
            print(f"   Total restaurants: {len(restaurants) if isinstance(restaurants, list) else 'N/A'}")
        else:
            print(f"   Failed to get restaurants")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "="*70)
    print("  TEST COMPLETED")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
