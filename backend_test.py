#!/usr/bin/env python3
"""
Backend Test Suite for Defensive Driving Training Management System
Tests the test management endpoints: POST /api/tests, GET /api/tests/program/{program_id}, DELETE /api/tests/{test_id}
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "https://training-hub-94.preview.emergentagent.com/api"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"

class TestRunner:
    def __init__(self):
        self.admin_token = None
        self.participant_token = None
        self.test_program_id = None
        self.created_test_ids = []
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def login_admin(self):
        """Login as admin and get authentication token"""
        self.log("Attempting admin login...")
        
        login_data = {
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data['access_token']
                self.log(f"✅ Admin login successful. User: {data['user']['full_name']} ({data['user']['role']})")
                return True
            else:
                self.log(f"❌ Admin login failed: {response.status_code} - {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Admin login error: {str(e)}", "ERROR")
            return False
    
    def create_test_program(self):
        """Create a test program for testing purposes"""
        self.log("Creating test program...")
        
        if not self.admin_token:
            self.log("❌ No admin token available", "ERROR")
            return False
            
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        
        program_data = {
            "name": "Test Management Program",
            "description": "Program created for testing test management endpoints",
            "pass_percentage": 75.0
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/programs", json=program_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.test_program_id = data['id']
                self.log(f"✅ Test program created successfully. ID: {self.test_program_id}")
                return True
            else:
                self.log(f"❌ Program creation failed: {response.status_code} - {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Program creation error: {str(e)}", "ERROR")
            return False
    
    def test_create_pre_test(self):
        """Test POST /api/tests - Create pre-test"""
        self.log("Testing POST /api/tests - Creating pre-test...")
        
        if not self.admin_token or not self.test_program_id:
            self.log("❌ Missing admin token or program ID", "ERROR")
            return False
            
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        
        test_data = {
            "program_id": self.test_program_id,
            "test_type": "pre",
            "questions": [
                {
                    "question": "What is the recommended following distance in good weather conditions?",
                    "options": ["1 second", "2 seconds", "3 seconds", "4 seconds"],
                    "correct_answer": 2
                },
                {
                    "question": "When should you check your mirrors while driving?",
                    "options": ["Only when changing lanes", "Every 5-8 seconds", "Only when parking", "Once per trip"],
                    "correct_answer": 1
                },
                {
                    "question": "What does defensive driving primarily focus on?",
                    "options": ["Speed", "Anticipating hazards", "Fuel efficiency", "Vehicle maintenance"],
                    "correct_answer": 1
                }
            ]
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/tests", json=test_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                test_id = data['id']
                self.created_test_ids.append(test_id)
                self.log(f"✅ Pre-test created successfully. ID: {test_id}")
                self.log(f"   Program ID: {data['program_id']}")
                self.log(f"   Test Type: {data['test_type']}")
                self.log(f"   Questions: {len(data['questions'])}")
                return True
            else:
                self.log(f"❌ Pre-test creation failed: {response.status_code} - {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Pre-test creation error: {str(e)}", "ERROR")
            return False
    
    def test_create_post_test(self):
        """Test POST /api/tests - Create post-test"""
        self.log("Testing POST /api/tests - Creating post-test...")
        
        if not self.admin_token or not self.test_program_id:
            self.log("❌ Missing admin token or program ID", "ERROR")
            return False
            
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        
        test_data = {
            "program_id": self.test_program_id,
            "test_type": "post",
            "questions": [
                {
                    "question": "What is the recommended following distance in good weather conditions?",
                    "options": ["1 second", "2 seconds", "3 seconds", "4 seconds"],
                    "correct_answer": 2
                },
                {
                    "question": "When should you check your mirrors while driving?",
                    "options": ["Only when changing lanes", "Every 5-8 seconds", "Only when parking", "Once per trip"],
                    "correct_answer": 1
                },
                {
                    "question": "What does defensive driving primarily focus on?",
                    "options": ["Speed", "Anticipating hazards", "Fuel efficiency", "Vehicle maintenance"],
                    "correct_answer": 1
                }
            ]
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/tests", json=test_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                test_id = data['id']
                self.created_test_ids.append(test_id)
                self.log(f"✅ Post-test created successfully. ID: {test_id}")
                self.log(f"   Program ID: {data['program_id']}")
                self.log(f"   Test Type: {data['test_type']}")
                self.log(f"   Questions: {len(data['questions'])}")
                return True
            else:
                self.log(f"❌ Post-test creation failed: {response.status_code} - {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Post-test creation error: {str(e)}", "ERROR")
            return False
    
    def test_get_tests_by_program(self):
        """Test GET /api/tests/program/{program_id}"""
        self.log("Testing GET /api/tests/program/{program_id}...")
        
        if not self.admin_token or not self.test_program_id:
            self.log("❌ Missing admin token or program ID", "ERROR")
            return False
            
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        
        try:
            response = self.session.get(f"{BASE_URL}/tests/program/{self.test_program_id}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"✅ Retrieved tests for program successfully. Count: {len(data)}")
                
                # Verify we have both pre and post tests
                test_types = [test['test_type'] for test in data]
                if 'pre' in test_types and 'post' in test_types:
                    self.log("✅ Both pre-test and post-test found in results")
                else:
                    self.log(f"⚠️  Expected both pre and post tests, found: {test_types}", "WARNING")
                
                # Log details of each test
                for test in data:
                    self.log(f"   Test ID: {test['id']}, Type: {test['test_type']}, Questions: {len(test['questions'])}")
                
                return True
            else:
                self.log(f"❌ Get tests by program failed: {response.status_code} - {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Get tests by program error: {str(e)}", "ERROR")
            return False
    
    def test_delete_test_as_admin(self):
        """Test DELETE /api/tests/{test_id} as admin"""
        self.log("Testing DELETE /api/tests/{test_id} as admin...")
        
        if not self.admin_token or not self.created_test_ids:
            self.log("❌ Missing admin token or test IDs", "ERROR")
            return False
            
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        test_id_to_delete = self.created_test_ids[0]  # Delete the first test
        
        try:
            response = self.session.delete(f"{BASE_URL}/tests/{test_id_to_delete}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"✅ Test deleted successfully. Message: {data.get('message', 'No message')}")
                self.created_test_ids.remove(test_id_to_delete)  # Remove from our tracking
                return True
            else:
                self.log(f"❌ Test deletion failed: {response.status_code} - {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Test deletion error: {str(e)}", "ERROR")
            return False
    
    def test_verify_test_deleted(self):
        """Verify the test was actually deleted by getting tests again"""
        self.log("Verifying test was deleted by retrieving tests again...")
        
        if not self.admin_token or not self.test_program_id:
            self.log("❌ Missing admin token or program ID", "ERROR")
            return False
            
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        
        try:
            response = self.session.get(f"{BASE_URL}/tests/program/{self.test_program_id}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                current_count = len(data)
                self.log(f"✅ Retrieved tests after deletion. Current count: {current_count}")
                
                # Should have one less test now
                if current_count == 1:
                    self.log("✅ Test count reduced by 1, deletion confirmed")
                    return True
                else:
                    self.log(f"⚠️  Expected 1 test remaining, found {current_count}", "WARNING")
                    return False
                    
            else:
                self.log(f"❌ Get tests verification failed: {response.status_code} - {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Get tests verification error: {str(e)}", "ERROR")
            return False
    
    def test_delete_nonexistent_test(self):
        """Test DELETE /api/tests/{test_id} with non-existent test ID"""
        self.log("Testing DELETE /api/tests/{test_id} with non-existent test...")
        
        if not self.admin_token:
            self.log("❌ Missing admin token", "ERROR")
            return False
            
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        fake_test_id = "non-existent-test-id-12345"
        
        try:
            response = self.session.delete(f"{BASE_URL}/tests/{fake_test_id}", headers=headers)
            
            if response.status_code == 404:
                self.log("✅ Non-existent test deletion correctly returned 404")
                return True
            else:
                self.log(f"❌ Expected 404 for non-existent test, got: {response.status_code} - {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Non-existent test deletion error: {str(e)}", "ERROR")
            return False
    
    def test_create_participant_user(self):
        """Create a participant user for testing non-admin access"""
        self.log("Creating participant user for non-admin testing...")
        
        if not self.admin_token:
            self.log("❌ No admin token available", "ERROR")
            return False
            
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        
        participant_data = {
            "email": "testparticipant@example.com",
            "password": "participant123",
            "full_name": "Test Participant",
            "id_number": "PART001",
            "role": "participant",
            "location": "Test Location"
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/auth/register", json=participant_data, headers=headers)
            
            if response.status_code == 200:
                self.log("✅ Participant user created successfully")
                return True
            else:
                self.log(f"❌ Participant creation failed: {response.status_code} - {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Participant creation error: {str(e)}", "ERROR")
            return False
    
    def login_participant(self):
        """Login as participant to test non-admin access"""
        self.log("Logging in as participant...")
        
        login_data = {
            "email": "testparticipant@example.com",
            "password": "participant123"
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                self.participant_token = data['access_token']
                self.log(f"✅ Participant login successful. User: {data['user']['full_name']} ({data['user']['role']})")
                return True
            else:
                self.log(f"❌ Participant login failed: {response.status_code} - {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Participant login error: {str(e)}", "ERROR")
            return False
    
    def test_delete_test_as_participant(self):
        """Test DELETE /api/tests/{test_id} as participant (should fail with 403)"""
        self.log("Testing DELETE /api/tests/{test_id} as participant (should fail)...")
        
        if not self.participant_token or not self.created_test_ids:
            self.log("❌ Missing participant token or test IDs", "ERROR")
            return False
            
        headers = {'Authorization': f'Bearer {self.participant_token}'}
        test_id_to_delete = self.created_test_ids[0] if self.created_test_ids else "dummy-id"
        
        try:
            response = self.session.delete(f"{BASE_URL}/tests/{test_id_to_delete}", headers=headers)
            
            if response.status_code == 403:
                self.log("✅ Participant test deletion correctly returned 403 Forbidden")
                return True
            else:
                self.log(f"❌ Expected 403 for participant deletion, got: {response.status_code} - {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Participant test deletion error: {str(e)}", "ERROR")
            return False
    
    def test_create_test_without_auth(self):
        """Test POST /api/tests without authentication (should fail)"""
        self.log("Testing POST /api/tests without authentication (should fail)...")
        
        test_data = {
            "program_id": "dummy-program-id",
            "test_type": "pre",
            "questions": [
                {
                    "question": "Test question?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": 0
                }
            ]
        }
        
        try:
            # No Authorization header
            response = self.session.post(f"{BASE_URL}/tests", json=test_data)
            
            if response.status_code == 403:
                self.log("✅ Unauthenticated test creation correctly returned 403")
                return True
            else:
                self.log(f"❌ Expected 403 for unauthenticated request, got: {response.status_code} - {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Unauthenticated test creation error: {str(e)}", "ERROR")
            return False
    
    def cleanup(self):
        """Clean up created test data"""
        self.log("Cleaning up test data...")
        
        if self.admin_token:
            headers = {'Authorization': f'Bearer {self.admin_token}'}
            
            # Delete remaining tests
            for test_id in self.created_test_ids:
                try:
                    response = self.session.delete(f"{BASE_URL}/tests/{test_id}", headers=headers)
                    if response.status_code == 200:
                        self.log(f"✅ Cleaned up test: {test_id}")
                    else:
                        self.log(f"⚠️  Failed to cleanup test {test_id}: {response.status_code}", "WARNING")
                except Exception as e:
                    self.log(f"⚠️  Error cleaning up test {test_id}: {str(e)}", "WARNING")
            
            # Delete test program
            if self.test_program_id:
                try:
                    response = self.session.delete(f"{BASE_URL}/programs/{self.test_program_id}", headers=headers)
                    if response.status_code == 200:
                        self.log(f"✅ Cleaned up program: {self.test_program_id}")
                    else:
                        self.log(f"⚠️  Failed to cleanup program: {response.status_code}", "WARNING")
                except Exception as e:
                    self.log(f"⚠️  Error cleaning up program: {str(e)}", "WARNING")
    
    def run_all_tests(self):
        """Run all test management endpoint tests"""
        self.log("=" * 80)
        self.log("STARTING TEST MANAGEMENT ENDPOINTS TEST SUITE")
        self.log("=" * 80)
        
        test_results = []
        
        # Test sequence as specified in the review request
        tests = [
            ("Admin Login", self.login_admin),
            ("Create Test Program", self.create_test_program),
            ("Create Pre-Test", self.test_create_pre_test),
            ("Create Post-Test", self.test_create_post_test),
            ("Get Tests by Program", self.test_get_tests_by_program),
            ("Delete Test as Admin", self.test_delete_test_as_admin),
            ("Verify Test Deleted", self.test_verify_test_deleted),
            ("Delete Non-existent Test", self.test_delete_nonexistent_test),
            ("Create Participant User", self.test_create_participant_user),
            ("Participant Login", self.login_participant),
            ("Delete Test as Participant (403)", self.test_delete_test_as_participant),
            ("Create Test without Auth (403)", self.test_create_test_without_auth),
        ]
        
        for test_name, test_func in tests:
            self.log(f"\n--- Running: {test_name} ---")
            try:
                result = test_func()
                test_results.append((test_name, result))
                if not result:
                    self.log(f"❌ {test_name} FAILED", "ERROR")
                else:
                    self.log(f"✅ {test_name} PASSED")
            except Exception as e:
                self.log(f"❌ {test_name} ERROR: {str(e)}", "ERROR")
                test_results.append((test_name, False))
        
        # Cleanup
        self.log(f"\n--- Cleanup ---")
        self.cleanup()
        
        # Summary
        self.log("\n" + "=" * 80)
        self.log("TEST RESULTS SUMMARY")
        self.log("=" * 80)
        
        passed = sum(1 for _, result in test_results if result)
        total = len(test_results)
        
        for test_name, result in test_results:
            status = "✅ PASS" if result else "❌ FAIL"
            self.log(f"{status} - {test_name}")
        
        self.log(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            self.log("🎉 ALL TESTS PASSED! Test management endpoints are working correctly.")
            return True
        else:
            self.log(f"⚠️  {total - passed} tests failed. Please review the failures above.")
            return False

def main():
    """Main function to run the test suite"""
    runner = TestRunner()
    success = runner.run_all_tests()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()