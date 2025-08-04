#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Fitness App
Tests all authentication, user, workout, and progress endpoints
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "https://f49a971d-2d55-4fa3-94c9-646b2e802986.preview.emergentagent.com/api"
TEST_USER = {
    "name": "Carlos Silva",
    "email": "carlos@test.com", 
    "password": "senha123"
}

class FitnessAppTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.user_id = None
        self.workout_id = None
        self.exercise_id = None
        self.test_results = []
        
    def log_test(self, test_name, success, details=""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
        
    def make_request(self, method, endpoint, data=None, headers=None):
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        default_headers = {"Content-Type": "application/json"}
        
        if headers:
            default_headers.update(headers)
            
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=default_headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=default_headers, timeout=30)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=default_headers, timeout=30)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=default_headers, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            return None
            
    def test_health_check(self):
        """Test API health check endpoint"""
        print("\n=== Testing Health Check ===")
        response = self.make_request("GET", "/")
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                self.log_test("Health Check", True, "API is running and healthy")
                return True
            else:
                self.log_test("Health Check", False, f"Unexpected response: {data}")
        else:
            status_code = response.status_code if response else "No response"
            self.log_test("Health Check", False, f"Status code: {status_code}")
        return False
        
    def test_user_registration(self):
        """Test user registration endpoint"""
        print("\n=== Testing User Registration ===")
        response = self.make_request("POST", "/auth/register", TEST_USER)
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("token") and data.get("user"):
                self.token = data["token"]
                self.user_id = data["user"]["id"]
                user = data["user"]
                
                # Validate user data
                if (user["name"] == TEST_USER["name"] and 
                    user["email"] == TEST_USER["email"] and
                    "avatar" in user):
                    self.log_test("User Registration", True, f"User created with ID: {self.user_id}")
                    return True
                else:
                    self.log_test("User Registration", False, "Invalid user data returned")
            else:
                self.log_test("User Registration", False, f"Missing required fields: {data}")
        else:
            status_code = response.status_code if response else "No response"
            error_msg = response.json().get("detail", "Unknown error") if response else "No response"
            self.log_test("User Registration", False, f"Status: {status_code}, Error: {error_msg}")
        return False
        
    def test_user_login(self):
        """Test user login endpoint"""
        print("\n=== Testing User Login ===")
        login_data = {
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        }
        response = self.make_request("POST", "/auth/login", login_data)
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("token") and data.get("user"):
                # Update token (should be same as registration)
                self.token = data["token"]
                user = data["user"]
                
                if (user["email"] == TEST_USER["email"] and 
                    user["name"] == TEST_USER["name"]):
                    self.log_test("User Login", True, "Login successful with valid token")
                    return True
                else:
                    self.log_test("User Login", False, "User data mismatch")
            else:
                self.log_test("User Login", False, f"Missing required fields: {data}")
        else:
            status_code = response.status_code if response else "No response"
            error_msg = response.json().get("detail", "Unknown error") if response else "No response"
            self.log_test("User Login", False, f"Status: {status_code}, Error: {error_msg}")
        return False
        
    def test_jwt_token_validation(self):
        """Test JWT token validation"""
        print("\n=== Testing JWT Token Validation ===")
        if not self.token:
            self.log_test("JWT Token Validation", False, "No token available")
            return False
            
        # Test with valid token
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.make_request("GET", "/user/profile", headers=headers)
        
        if response and response.status_code == 200:
            self.log_test("JWT Token Validation - Valid Token", True, "Token accepted")
        else:
            self.log_test("JWT Token Validation - Valid Token", False, "Valid token rejected")
            return False
            
        # Test with invalid token
        headers = {"Authorization": "Bearer invalid_token_here"}
        response = self.make_request("GET", "/user/profile", headers=headers)
        
        if response and response.status_code == 401:
            self.log_test("JWT Token Validation - Invalid Token", True, "Invalid token properly rejected")
            return True
        else:
            self.log_test("JWT Token Validation - Invalid Token", False, "Invalid token not rejected")
        return False
        
    def test_user_profile(self):
        """Test user profile endpoint"""
        print("\n=== Testing User Profile ===")
        if not self.token:
            self.log_test("User Profile", False, "No authentication token")
            return False
            
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.make_request("GET", "/user/profile", headers=headers)
        
        if response and response.status_code == 200:
            data = response.json()
            if (data.get("id") and data.get("name") == TEST_USER["name"] and 
                data.get("email") == TEST_USER["email"]):
                self.log_test("User Profile", True, f"Profile retrieved for user: {data['name']}")
                return True
            else:
                self.log_test("User Profile", False, f"Invalid profile data: {data}")
        else:
            status_code = response.status_code if response else "No response"
            self.log_test("User Profile", False, f"Status code: {status_code}")
        return False
        
    def test_get_workouts(self):
        """Test get all workouts endpoint"""
        print("\n=== Testing Get Workouts ===")
        if not self.token:
            self.log_test("Get Workouts", False, "No authentication token")
            return False
            
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.make_request("GET", "/workouts/", headers=headers)
        
        if response and response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                # Should have sample workouts created automatically
                workout = data[0]
                if ("id" in workout and "name" in workout and "exercises" in workout):
                    self.workout_id = workout["id"]
                    if workout["exercises"]:
                        self.exercise_id = workout["exercises"][0]["id"]
                    self.log_test("Get Workouts", True, f"Retrieved {len(data)} workouts")
                    return True
                else:
                    self.log_test("Get Workouts", False, "Invalid workout structure")
            else:
                self.log_test("Get Workouts", False, "No workouts returned")
        else:
            status_code = response.status_code if response else "No response"
            self.log_test("Get Workouts", False, f"Status code: {status_code}")
        return False
        
    def test_get_today_workout(self):
        """Test get today's workout endpoint"""
        print("\n=== Testing Get Today's Workout ===")
        if not self.token:
            self.log_test("Get Today's Workout", False, "No authentication token")
            return False
            
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.make_request("GET", "/workouts/today", headers=headers)
        
        if response and response.status_code == 200:
            data = response.json()
            if ("id" in data and "name" in data and "status" in data and 
                "exercises" in data):
                # Should be active workout
                if data["status"] in ["active", "pending"]:
                    self.log_test("Get Today's Workout", True, f"Today's workout: {data['name']} ({data['status']})")
                    return True
                else:
                    self.log_test("Get Today's Workout", False, f"Unexpected status: {data['status']}")
            else:
                self.log_test("Get Today's Workout", False, "Invalid workout structure")
        else:
            status_code = response.status_code if response else "No response"
            self.log_test("Get Today's Workout", False, f"Status code: {status_code}")
        return False
        
    def test_complete_set(self):
        """Test complete set endpoint"""
        print("\n=== Testing Complete Set ===")
        if not self.token or not self.workout_id or not self.exercise_id:
            self.log_test("Complete Set", False, "Missing token, workout_id, or exercise_id")
            return False
            
        headers = {"Authorization": f"Bearer {self.token}"}
        set_data = {
            "setNumber": 1,
            "weight": 80.0,
            "reps": 10
        }
        
        endpoint = f"/workouts/{self.workout_id}/exercises/{self.exercise_id}/complete-set"
        response = self.make_request("POST", endpoint, set_data, headers)
        
        if response and response.status_code == 200:
            data = response.json()
            if (data.get("success") and "exercise" in data):
                exercise = data["exercise"]
                if ("completedSets" in exercise and "totalSets" in exercise):
                    self.log_test("Complete Set", True, f"Set completed: {exercise['completedSets']}/{exercise['totalSets']}")
                    return True
                else:
                    self.log_test("Complete Set", False, "Invalid exercise data in response")
            else:
                self.log_test("Complete Set", False, f"Invalid response structure: {data}")
        else:
            status_code = response.status_code if response else "No response"
            error_msg = response.json().get("detail", "Unknown error") if response else "No response"
            self.log_test("Complete Set", False, f"Status: {status_code}, Error: {error_msg}")
        return False
        
    def test_weekly_progress(self):
        """Test weekly progress endpoint"""
        print("\n=== Testing Weekly Progress ===")
        if not self.token:
            self.log_test("Weekly Progress", False, "No authentication token")
            return False
            
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.make_request("GET", "/progress/weekly", headers=headers)
        
        if response and response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                # Should return weekly progress data
                week_data = data[0]
                if ("week" in week_data and "volume" in week_data and 
                    "weight" in week_data and "workouts" in week_data):
                    self.log_test("Weekly Progress", True, f"Retrieved {len(data)} weeks of progress data")
                    return True
                else:
                    self.log_test("Weekly Progress", False, "Invalid weekly progress structure")
            else:
                self.log_test("Weekly Progress", False, "No weekly progress data returned")
        else:
            status_code = response.status_code if response else "No response"
            self.log_test("Weekly Progress", False, f"Status code: {status_code}")
        return False
        
    def test_progress_stats(self):
        """Test progress stats endpoint"""
        print("\n=== Testing Progress Stats ===")
        if not self.token:
            self.log_test("Progress Stats", False, "No authentication token")
            return False
            
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.make_request("GET", "/progress/stats", headers=headers)
        
        if response and response.status_code == 200:
            data = response.json()
            if ("totalVolume" in data and "avgWeight" in data and 
                "completedWorkouts" in data and "currentStreak" in data):
                self.log_test("Progress Stats", True, f"Stats: {data['completedWorkouts']} workouts, streak: {data['currentStreak']}")
                return True
            else:
                self.log_test("Progress Stats", False, f"Invalid stats structure: {data}")
        else:
            status_code = response.status_code if response else "No response"
            self.log_test("Progress Stats", False, f"Status code: {status_code}")
        return False
        
    def test_authentication_protection(self):
        """Test that protected routes require authentication"""
        print("\n=== Testing Authentication Protection ===")
        protected_endpoints = [
            "/user/profile",
            "/workouts/",
            "/workouts/today",
            "/progress/weekly",
            "/progress/stats"
        ]
        
        all_protected = True
        for endpoint in protected_endpoints:
            response = self.make_request("GET", endpoint)
            if response and response.status_code == 401:
                print(f"   ✅ {endpoint} properly protected")
            else:
                print(f"   ❌ {endpoint} not properly protected")
                all_protected = False
                
        self.log_test("Authentication Protection", all_protected, 
                     "All protected endpoints require authentication" if all_protected 
                     else "Some endpoints not properly protected")
        return all_protected
        
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting Fitness App Backend API Tests")
        print(f"Base URL: {self.base_url}")
        print(f"Test User: {TEST_USER['name']} ({TEST_USER['email']})")
        
        # Test sequence
        tests = [
            self.test_health_check,
            self.test_user_registration,
            self.test_user_login,
            self.test_jwt_token_validation,
            self.test_user_profile,
            self.test_get_workouts,
            self.test_get_today_workout,
            self.test_complete_set,
            self.test_weekly_progress,
            self.test_progress_stats,
            self.test_authentication_protection
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                print(f"❌ Test {test.__name__} failed with exception: {str(e)}")
                
        # Summary
        print(f"\n{'='*60}")
        print(f"🏁 TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED!")
            return True
        else:
            print("⚠️  SOME TESTS FAILED")
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   ❌ {result['test']}: {result['details']}")
            return False

def main():
    """Main test execution"""
    tester = FitnessAppTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()