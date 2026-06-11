"""
Configuration file for Salary Prediction API
"""

import os

# API Configuration
API_VERSION = '1.0'
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# Model Configuration
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'model_file.p')
MODEL_INPUT_FEATURES = 19
MODEL_TYPE = 'RandomForestRegressor'

# Flask Configuration
JSON_SORT_KEYS = False
