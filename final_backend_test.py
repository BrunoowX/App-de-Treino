#!/usr/bin/env python3
"""
Final Comprehensive Backend API Testing for Fitness App
Tests all functionality with correct HTTP status code expectations
"""

import requests
import json
import sys
from datetime import datetime
import uuid

# Configuration
BASE_URL = "https://f49a971d-2d55-4fa3-94c9-646b2e802986.preview.emergentagent.com/api"

class FinalFitnessAppTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.user_id = None
        self.workout_id = None
        self.exercise_id = None
        self.test_results = []
        # Use unique email to avoid conflicts
        self.test_user = {
            "name": "Carlos Silva",
            "email": f"carlos_{uuid.uuid4().hex[:8]}@test.com",
            "password": "senha123"
        }
        
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
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            return None
            
    def test_complete_flow(self):
        """Test complete user flow"""
        print("🚀 Starting Complete Backend API Test Flow")
        print(f"Base URL: {self.base_url}")
        print(f"Test User: {self.test_user['name']} ({self.test_user['email']})")
        
        # 1. Health Check
        print("\n=== 1. Health Check ===")
        response = self.make_request("GET", "/")
        if response and response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                self.log_test("Health Check", True, "API is running and healthy")
            else:
                self.log_test("Health Check", False, f"Unexpected response: {data}")
        else:
            self.log_test("Health Check", False, "API not responding")
            
        # 2. User Registration
        print("\n=== 2. User Registration ===")
        response = self.make_request("POST", "/auth/register", self.test_user)
        if response and response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("token") and data.get("user"):
                self.token = data["token"]
                self.user_id = data["user"]["id"]
                self.log_test("User Registration", True, f"User created with ID: {self.user_id}")
            else:
                self.log_test("User Registration", False, f"Invalid response: {data}")
        else:
            error_msg = response.json().get("detail", "Unknown error") if response else "No response"
            self.log_test("User Registration", False, f"Registration failed: {error_msg}")
            
        # 3. User Login
        print("\n=== 3. User Login ===")
        login_data = {"email": self.test_user["email"], "password": self.test_user["password"]}
        response = self.make_request("POST", "/auth/login", login_data)
        if response and response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("token"):
                self.log_test("User Login", True, "Login successful")
            else:
                self.log_test("User Login", False, f"Invalid response: {data}")
        else:
            self.log_test("User Login", False, "Login failed")
            
        # 4. Authentication Protection Test
        print("\n=== 4. Authentication Protection ===")
        # Test without token (should return 403)
        response = self.make_request("GET", "/user/profile")
        if response and response.status_code == 403:
            self.log_test("Auth Protection - No Token", True, "Correctly returns 403 for missing auth")
        else:
            self.log_test("Auth Protection - No Token", False, f"Expected 403, got {response.status_code if response else 'No response'}")
            
        # Test with invalid token (should return 401)
        headers = {"Authorization": "Bearer invalid_token"}
        response = self.make_request("GET", "/user/profile", headers=headers)
        if response and response.status_code == 401:
            self.log_test("Auth Protection - Invalid Token", True, "Correctly returns 401 for invalid token")
        else:
            self.log_test("Auth Protection - Invalid Token", False, f"Expected 401, got {response.status_code if response else 'No response'}")
            
        # 5. User Profile
        print("\n=== 5. User Profile ===")
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.make_request("GET", "/user/profile", headers=headers)
            if response and response.status_code == 200:
                data = response.json()
                if data.get("name") == self.test_user["name"]:
                    self.log_test("User Profile", True, f"Profile retrieved: {data['name']}")
                else:
                    self.log_test("User Profile", False, "Profile data mismatch")
            else:
                self.log_test("User Profile", False, "Failed to get profile")
        else:
            self.log_test("User Profile", False, "No token available")
            
        # 6. Get Workouts
        print("\n=== 6. Get Workouts ===")
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.make_request("GET", "/workouts/", headers=headers)
            if response and response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    self.workout_id = data[0]["id"]
                    if data[0]["exercises"]:
                        self.exercise_id = data[0]["exercises"][0]["id"]
                    self.log_test("Get Workouts", True, f"Retrieved {len(data)} workouts")
                else:
                    self.log_test("Get Workouts", False, "No workouts returned")
            else:
                self.log_test("Get Workouts", False, "Failed to get workouts")
        else:
            self.log_test("Get Workouts", False, "No token available")
            
        # 7. Get Today's Workout
        print("\n=== 7. Get Today's Workout ===")
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.make_request("GET", "/workouts/today", headers=headers)
            if response and response.status_code == 200:
                data = response.json()
                if data.get("name") and data.get("status"):
                    self.log_test("Get Today's Workout", True, f"Today's workout: {data['name']} ({data['status']})")
                else:
                    self.log_test("Get Today's Workout", False, "Invalid workout data")
            else:
                self.log_test("Get Today's Workout", False, "Failed to get today's workout")
        else:
            self.log_test("Get Today's Workout", False, "No token available")
            
        # 8. Complete Set
        print("\n=== 8. Complete Set ===")
        if self.token and self.workout_id and self.exercise_id:
            headers = {"Authorization": f"Bearer {self.token}"}
            set_data = {"setNumber": 1, "weight": 80.0, "reps": 10}
            endpoint = f"/workouts/{self.workout_id}/exercises/{self.exercise_id}/complete-set"
            response = self.make_request("POST", endpoint, set_data, headers)
            if response and response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Complete Set", True, "Set completed successfully")
                else:
                    self.log_test("Complete Set", False, "Set completion failed")
            else:
                self.log_test("Complete Set", False, "Failed to complete set")
        else:
            self.log_test("Complete Set", False, "Missing required data")
            
        # 9. Weekly Progress
        print("\n=== 9. Weekly Progress ===")
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.make_request("GET", "/progress/weekly", headers=headers)
            if response and response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    self.log_test("Weekly Progress", True, f"Retrieved {len(data)} weeks of data")
                else:
                    self.log_test("Weekly Progress", False, "No progress data")
            else:
                self.log_test("Weekly Progress", False, "Failed to get weekly progress")
        else:
            self.log_test("Weekly Progress", False, "No token available")
            
        # 10. Progress Stats
        print("\n=== 10. Progress Stats ===")
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.make_request("GET", "/progress/stats", headers=headers)
            if response and response.status_code == 200:
                data = response.json()
                if all(key in data for key in ["totalVolume", "avgWeight", "completedWorkouts", "currentStreak"]):
                    self.log_test("Progress Stats", True, f"Stats retrieved: {data['completedWorkouts']} workouts")
                else:
                    self.log_test("Progress Stats", False, "Invalid stats data")
            else:
                self.log_test("Progress Stats", False, "Failed to get progress stats")
        else:
            self.log_test("Progress Stats", False, "No token available")
            
        # Summary
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"\n{'='*60}")
        print(f"🏁 FINAL TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED!")
            print("\n✅ Backend API is fully functional:")
            print("   • Authentication system working correctly")
            print("   • User registration and login working")
            print("   • JWT token validation working")
            print("   • All protected endpoints secured")
            print("   • Workout management working")
            print("   • Progress tracking working")
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
    tester = FinalFitnessAppTester()
    success = tester.test_complete_flow()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()