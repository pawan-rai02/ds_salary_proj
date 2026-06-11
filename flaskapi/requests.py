"""
Example requests to test the Salary Prediction API

Run this file to test the Flask API:
    python requests.py
    
Make sure the Flask app is running:
    python app.py
"""

import requests
import json

BASE_URL = 'http://localhost:5000'

def test_health():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("Testing /health endpoint")
    print("="*60)
    try:
        response = requests.get(f'{BASE_URL}/health')
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_home():
    """Test home/documentation endpoint"""
    print("\n" + "="*60)
    print("Testing / endpoint (API documentation)")
    print("="*60)
    try:
        response = requests.get(f'{BASE_URL}/')
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_predict_valid():
    """Test valid prediction request"""
    print("\n" + "="*60)
    print("Testing /predict endpoint (VALID REQUEST)")
    print("="*60)
    
    # Example: 19 features (should be normalized/scaled appropriately)
    # These are sample values - adjust based on your model's expected ranges
    payload = {
        "input": [
            4.5,      # Rating
            1,        # Size_M
            0,        # Size_S
            0,        # Size_XL
            0,        # Type_Private
            1,        # Type_Public
            0,        # Industry_Aerospace
            0,        # Industry_Agriculture
            0,        # Sector_Accounting
            1,        # Revenue_1-2B
            3,        # num_comp
            0,        # hourly
            1,        # employer_provided
            1,        # job_state_CA
            0,        # job_state_NY
            1,        # same_state
            15,       # age (years)
            1,        # python_yn
            1,        # spark
            1         # aws (19 features total)
        ]
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/predict',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Request Payload: {json.dumps(payload, indent=2)}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_predict_invalid_features():
    """Test invalid prediction request - wrong number of features"""
    print("\n" + "="*60)
    print("Testing /predict endpoint (INVALID - wrong # features)")
    print("="*60)
    
    payload = {
        "input": [1, 2, 3]  # Only 3 features instead of 19
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/predict',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_predict_no_input():
    """Test invalid prediction request - missing input"""
    print("\n" + "="*60)
    print("Testing /predict endpoint (INVALID - missing input)")
    print("="*60)
    
    payload = {}
    
    try:
        response = requests.post(
            f'{BASE_URL}/predict',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("SALARY PREDICTION API - TEST SUITE")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print("Make sure Flask app is running before executing tests!")
    
    # Run tests
    test_home()
    test_health()
    test_predict_valid()
    test_predict_invalid_features()
    test_predict_no_input()
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETED")
    print("="*60)
