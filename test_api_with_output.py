#!/usr/bin/env python3
"""Simple API Test Script with File Output"""

import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def log(msg):
    print(msg)
    with open("test_results.txt", "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def main():
    # Clear output file
    with open("test_results.txt", "w", encoding="utf-8") as f:
        f.write("")
    
    log("\n" + "="*70)
    log("  FOOD DELIVERY SYSTEM - API TEST")
    log("="*70 + "\n")
    
    # Test 1: Health Check
    log("1. Testing Health Check...")
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=5)
        log(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            log("   SUCCESS - API Gateway is running")
        else:
            log("   FAILED - Health check failed")
    except Exception as e:
        log(f"   ERROR: {e}")
        return
    
    # Test 2: Login
    log("\n2. Testing Login...")
    try:
        resp = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": "admin", "password": "admin123"},
            timeout=5
        )
        log(f"   Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            token = data.get('access_token')
            log(f"   SUCCESS - Login successful")
            log(f"   Token: {token[:50]}...")
        else:
            log(f"   FAILED - Login failed")
            log(f"   Response: {resp.text}")
            return
    except Exception as e:
        log(f"   ERROR: {e}")
        return
    
    # Test 3: Verify Token
    log("\n3. Testing Token Verification...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"{BASE_URL}/auth/verify", headers=headers, timeout=5)
        log(f"   Status: {resp.status_code}")
        
        if resp.status_code == 200:
            log(f"   SUCCESS - Token is valid")
            try:
                log(f"   Response: {json.dumps(resp.json(), indent=2)}")
            except:
                log(f"   Response: {resp.text}")
        else:
            log(f"   FAILED - Token verification failed")
            log(f"   Response: {resp.text}")
    except Exception as e:
        log(f"   ERROR: {e}")
    
    # Test 4: Get All Users
    log("\n4. Testing Get All Users...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"{BASE_URL}/api/user-service/api/users", headers=headers, timeout=5)
        log(f"   Status: {resp.status_code}")
        
        if resp.status_code == 200:
            users = resp.json()
            log(f"   SUCCESS - Retrieved users")
            if isinstance(users, list):
                log(f"   Total users: {len(users)}")
                if len(users) > 0:
                    log(f"   Sample user: {json.dumps(users[0], indent=2)}")
            else:
                log(f"   Response: {json.dumps(users, indent=2)}")
        else:
            log(f"   FAILED - Could not get users")
            log(f"   Response: {resp.text}")
    except Exception as e:
        log(f"   ERROR: {e}")
    
    # Test 5: Get All Restaurants
    log("\n5. Testing Get All Restaurants...")
    try:
        resp = requests.get(f"{BASE_URL}/api/restaurant-service/api/restaurants", timeout=5)
        log(f"   Status: {resp.status_code}")
        
        if resp.status_code == 200:
            restaurants = resp.json()
            log(f"   SUCCESS - Retrieved restaurants")
            if isinstance(restaurants, list):
                log(f"   Total restaurants: {len(restaurants)}")
            else:
                log(f"   Response type: {type(restaurants)}")
        else:
            log(f"   FAILED - Could not get restaurants")
    except Exception as e:
        log(f"   ERROR: {e}")
    
    log("\n" + "="*70)
    log("  TEST COMPLETED")
    log("="*70 + "\n")

if __name__ == "__main__":
    main()
