from flask import Flask, jsonify, request
import json
import numpy as np
import pickle
import os

# Initialize Flask app
app = Flask(__name__)

# Model cache - load once
_model = None

def load_model():
    """Load the trained model from pickle file"""
    global _model
    if _model is None:
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'model_file.p')
        try:
            with open(model_path, 'rb') as pickled:
                data = pickle.load(pickled)
                _model = data['model']
            print(f"✓ Model loaded successfully from {model_path}")
        except FileNotFoundError:
            print(f"✗ Model file not found at {model_path}")
            raise
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            raise
    return _model

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict salary based on input features
    
    Expected JSON format:
    {
        "input": [feature1, feature2, ..., feature19]
    }
    
    Returns:
    {
        "prediction": predicted_salary,
        "status": "success"
    }
    """
    try:
        request_json = request.get_json()
        
        if not request_json or 'input' not in request_json:
            return jsonify({
                'error': 'Invalid request. Required format: {"input": [feature_array]}',
                'status': 'error'
            }), 400
        
        x = request_json['input']
        
        # Validate input length (should be 19 features for Random Forest)
        if len(x) != 19:
            return jsonify({
                'error': f'Expected 19 features, got {len(x)}',
                'status': 'error'
            }), 400
        
        # Convert to numpy array and reshape for model
        x_in = np.array(x).reshape(1, -1)
        
        # Load model and make prediction
        model = load_model()
        prediction = model.predict(x_in)[0]
        
        response = {
            'prediction': float(prediction),
            'status': 'success'
        }
        return jsonify(response), 200
        
    except ValueError as e:
        return jsonify({
            'error': f'Invalid input values: {str(e)}',
            'status': 'error'
        }), 400
    except Exception as e:
        return jsonify({
            'error': f'Prediction error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Salary Prediction API',
        'model_loaded': _model is not None
    }), 200

@app.route('/', methods=['GET'])
def home():
    """API documentation endpoint"""
    return jsonify({
        'service': 'Salary Prediction API',
        'version': '1.0',
        'endpoints': {
            '/': 'This help message',
            '/health': 'Health check',
            '/predict (POST)': 'Make prediction with 19 features'
        },
        'usage': {
            'method': 'POST',
            'url': '/predict',
            'format': '{"input": [f1, f2, ..., f19]}',
            'returns': '{"prediction": salary, "status": "success"}'
        }
    }), 200

if __name__ == '__main__':
    # Load model on startup
    try:
        load_model()
        print("Starting Salary Prediction API...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Failed to start API: {e}")