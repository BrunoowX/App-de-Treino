#!/usr/bin/env python3
"""
Focused Authentication Testing for Fitness App
Tests JWT token validation and authentication protection
"""

import requests
import json
import sys
from datetime import datetime
import uuid

# Configuration
BASE_URL = "https://f49a971d-2d55-4fa3-94c9-646b2e802986.preview.emergentagent.com/api"

def test_invalid_token():
    """Test invalid token handling"""
    print("=== Testing Invalid Token Handling ===")
    
    # Test with completely invalid token
    headers = {"Authorization": "Bearer invalid_token_here"}
    response = requests.get(f"{BASE_URL}/user/profile", headers=headers, timeout=30)
    
    print(f"Invalid token response: Status {response.status_code}")
    if response.status_code == 401:
        print("✅ Invalid token properly rejected")
        return True
    else:
        print(f"❌ Invalid token not rejected. Response: {response.text}")
        return False

def test_no_token():
    """Test endpoints without token"""
    print("\n=== Testing No Token Protection ===")
    
    endpoints = [
        "/user/profile",
        "/workouts/",
        "/workouts/today", 
        "/progress/weekly",
        "/progress/stats"
    ]
    
    all_protected = True
    for endpoint in endpoints:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=30)
        print(f"{endpoint}: Status {response.status_code}")
        if response.status_code != 401:
            print(f"   ❌ Not protected - Response: {response.text[:100]}")
            all_protected = False
        else:
            print(f"   ✅ Properly protected")
    
    return all_protected

def test_malformed_token():
    """Test malformed token"""
    print("\n=== Testing Malformed Token ===")
    
    # Test with malformed Authorization header
    headers = {"Authorization": "InvalidFormat"}
    response = requests.get(f"{BASE_URL}/user/profile", headers=headers, timeout=30)
    
    print(f"Malformed auth header: Status {response.status_code}")
    if response.status_code == 401:
        print("✅ Malformed auth header properly rejected")
        return True
    else:
        print(f"❌ Malformed auth header not rejected. Response: {response.text}")
        return False

def test_new_user_registration():
    """Test registration with unique user"""
    print("\n=== Testing New User Registration ===")
    
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@test.com"
    user_data = {
        "name": "Test User",
        "email": unique_email,
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data, timeout=30)
    print(f"Registration response: Status {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success") and data.get("token"):
            print("✅ New user registration successful")
            return True, data["token"]
        else:
            print(f"❌ Registration failed: {data}")
            return False, None
    else:
        print(f"❌ Registration failed: {response.text}")
        return False, None

def main():
    """Run focused authentication tests"""
    print("🔐 Focused Authentication Testing")
    print(f"Base URL: {BASE_URL}")
    
    # Test new user registration first
    reg_success, token = test_new_user_registration()
    
    # Test authentication protection
    no_token_protected = test_no_token()
    
    # Test invalid token handling
    invalid_token_handled = test_invalid_token()
    
    # Test malformed token
    malformed_handled = test_malformed_token()
    
    # Summary
    print(f"\n{'='*50}")
    print("🏁 AUTHENTICATION TEST SUMMARY")
    print(f"{'='*50}")
    print(f"New User Registration: {'✅' if reg_success else '❌'}")
    print(f"No Token Protection: {'✅' if no_token_protected else '❌'}")
    print(f"Invalid Token Handling: {'✅' if invalid_token_handled else '❌'}")
    print(f"Malformed Token Handling: {'✅' if malformed_handled else '❌'}")
    
    all_passed = all([reg_success, no_token_protected, invalid_token_handled, malformed_handled])
    
    if all_passed:
        print("🎉 ALL AUTHENTICATION TESTS PASSED!")
    else:
        print("⚠️  SOME AUTHENTICATION TESTS FAILED")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)