#!/usr/bin/env python
"""
Quick start script to test and deploy the Salary Prediction API

Usage:
    python quick_start.py
"""

import sys
import subprocess
import os
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def check_dependencies():
    """Verify all required packages are installed"""
    print_header("CHECKING DEPENDENCIES")
    
    required = ['flask', 'numpy', 'pandas', 'sklearn', 'werkzeug']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n  Missing packages: {', '.join(missing)}")
        print(f"  Run: pip install -r requirements.txt")
        return False
    
    print("\n  ✓ All dependencies installed")
    return True

def check_model():
    """Verify model file exists"""
    print_header("CHECKING MODEL FILE")
    
    model_path = Path(__file__).parent / 'models' / 'model_file.p'
    
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"  ✓ Model found: {model_path}")
        print(f"  ✓ Model size: {size_mb:.2f} MB")
        return True
    else:
        print(f"  ✗ Model NOT found: {model_path}")
        print(f"  Copy model_file.p to models/ directory")
        return False

def load_app():
    """Test loading the Flask app and model"""
    print_header("TESTING APP INITIALIZATION")
    
    try:
        from app import app, load_model
        print(f"  ✓ Flask app created")
        
        model = load_model()
        print(f"  ✓ Model loaded successfully")
        print(f"  ✓ Model type: {type(model).__name__}")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print_header("TESTING API ENDPOINTS")
    
    try:
        from app import app
        
        client = app.test_client()
        
        # Test home endpoint
        response = client.get('/')
        if response.status_code == 200:
            print(f"  ✓ GET / (Status: {response.status_code})")
        else:
            print(f"  ✗ GET / (Status: {response.status_code})")
        
        # Test health endpoint
        response = client.get('/health')
        if response.status_code == 200:
            print(f"  ✓ GET /health (Status: {response.status_code})")
        else:
            print(f"  ✗ GET /health (Status: {response.status_code})")
        
        # Test prediction endpoint with valid input
        payload = {
            'input': [4.5, 1, 0, 0, 0, 1, 0, 0, 0, 1, 3, 0, 1, 1, 0, 1, 15, 1, 1, 1]
        }
        response = client.post(
            '/predict',
            json=payload,
            content_type='application/json'
        )
        if response.status_code == 200:
            data = response.get_json()
            prediction = data.get('prediction')
            print(f"  ✓ POST /predict (Status: {response.status_code})")
            print(f"    Prediction: ${prediction:,.0f}")
        else:
            print(f"  ✗ POST /predict (Status: {response.status_code})")
        
        return True
    except Exception as e:
        print(f"  ✗ Error testing endpoints: {e}")
        return False

def display_startup_instructions():
    """Display instructions for starting the API"""
    print_header("DEPLOYMENT OPTIONS")
    
    instructions = """
    1. DEVELOPMENT SERVER (Simple)
       ────────────────────────────
       Command:
           python app.py
       
       Then access API at:
           http://localhost:5000
       
       Best for: Testing and development
       
       
    2. BATCH FILE (Windows)
       ────────────────────────────
       Run:
           run_api.bat
       
       This starts the Flask development server
       
       
    3. PRODUCTION DEPLOYMENT (Gunicorn)
       ────────────────────────────
       Command:
           gunicorn -w 4 -b 0.0.0.0:5000 app:app
       
       Best for: Production deployment
       
       
    4. DOCKER DEPLOYMENT
       ────────────────────────────
       Create Dockerfile in this directory, then:
           docker build -t salary-api .
           docker run -p 5000:5000 salary-api
    """
    print(instructions)

def display_api_usage():
    """Display API usage examples"""
    print_header("API USAGE EXAMPLES")
    
    usage = """
    TEST ENDPOINTS:
    ───────────────
    
    1. Health Check:
       curl http://localhost:5000/health
    
    
    2. API Documentation:
       curl http://localhost:5000/
    
    
    3. Make Prediction:
       curl -X POST http://localhost:5000/predict \\
         -H "Content-Type: application/json" \\
         -d '{"input": [4.5, 1, 0, 0, 0, 1, 0, 0, 0, 1, 3, 0, 1, 1, 0, 1, 15, 1, 1, 1]}'
    
    
    PYTHON EXAMPLE:
    ───────────────
    
    import requests
    
    url = 'http://localhost:5000/predict'
    features = [4.5, 1, 0, 0, 0, 1, 0, 0, 0, 1, 3, 0, 1, 1, 0, 1, 15, 1, 1, 1]
    payload = {'input': features}
    
    response = requests.post(url, json=payload)
    prediction = response.json()['prediction']
    
    print(f"Predicted Salary: ${prediction:,.0f}")
    """
    print(usage)

def main():
    """Run all checks and display startup info"""
    print_header("SALARY PREDICTION API - QUICK START")
    
    # Run checks
    checks_passed = [
        check_dependencies(),
        check_model(),
        load_app(),
        test_api_endpoints()
    ]
    
    # Display results
    print_header("VERIFICATION SUMMARY")
    if all(checks_passed):
        print("  ✓ ALL CHECKS PASSED")
        print("  ✓ API is ready for deployment")
        status = "✅ READY"
    else:
        print("  ✗ Some checks failed")
        print("  ✗ See errors above")
        status = "❌ NOT READY"
    
    print(f"\n  Status: {status}\n")
    
    # Display instructions
    if all(checks_passed):
        display_startup_instructions()
        display_api_usage()
        
        print_header("NEXT STEPS")
        print("""
  1. Start the API:
     python app.py
  
  2. In another terminal, test the API:
     python requests.py
  
  3. Or make manual requests using curl or Python requests
  
  4. For production, use gunicorn or Docker
        """)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nQuick start interrupted by user.")
    except Exception as e:
        print(f"\n\nError: {e}")
        sys.exit(1)
