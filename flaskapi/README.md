# 🚀 Salary Prediction API

A simple Flask API for predicting data science salaries based on job characteristics and company attributes.

## 📁 Project Structure

```
flaskapi/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── data_input.py          # Input validation and feature mapping
├── requests.py            # Test requests examples
├── requirements.txt       # Python dependencies
├── models/
│   └── model_file.p       # Trained Random Forest model (pickled)
└── README.md              # This file
```

## 🔧 Installation & Setup

### 1. Install Dependencies

```bash
# Navigate to flaskapi directory
cd flaskapi

# Install required packages
pip install -r requirements.txt
```

### 2. Verify Model File

Ensure `model_file.p` is in the `models/` folder:
```
flaskapi/models/model_file.p ✓
```

## ▶️ Running the API

### Start the Flask Server

```bash
python app.py
```

Expected output:
```
✓ Model loaded successfully from models/model_file.p
 * Running on http://0.0.0.0:5000
 * WARNING: This is a development server. Do not use it in production.
```

The API will be available at: `http://localhost:5000`

## 📡 API Endpoints

### 1. **Home / Documentation** (GET)
```
GET /
```
Returns API documentation and available endpoints.

**Response:**
```json
{
  "service": "Salary Prediction API",
  "version": "1.0",
  "endpoints": {...},
  "usage": {...}
}
```

### 2. **Health Check** (GET)
```
GET /health
```
Check if API and model are running properly.

**Response:**
```json
{
  "status": "healthy",
  "service": "Salary Prediction API",
  "model_loaded": true
}
```

### 3. **Make Prediction** (POST) ⭐
```
POST /predict
```

**Request Format:**
```json
{
  "input": [feature1, feature2, ..., feature19]
}
```

**Required:**
- Exactly 19 numeric features (one-hot encoded)
- All features must be numeric values

**Response (Success):**
```json
{
  "prediction": 125000.50,
  "status": "success"
}
```

**Response (Error):**
```json
{
  "error": "Expected 19 features, got 5",
  "status": "error"
}
```

## 🧪 Testing the API

### Using Python (requests library)

```bash
python requests.py
```

This runs a comprehensive test suite including:
- ✓ Health check
- ✓ Valid prediction
- ✓ Invalid inputs
- ✓ Error handling

### Using cURL

```bash
# Health check
curl http://localhost:5000/health

# Make prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"input": [4.5, 1, 0, 0, 0, 1, 0, 0, 0, 1, 3, 0, 1, 1, 0, 1, 15, 1, 1, 1]}'
```

### Using Python (requests module)

```python
import requests

url = 'http://localhost:5000/predict'
payload = {
    'input': [4.5, 1, 0, 0, 0, 1, 0, 0, 0, 1, 3, 0, 1, 1, 0, 1, 15, 1, 1, 1]
}

response = requests.post(url, json=payload)
result = response.json()
print(f"Predicted Salary: ${result['prediction']:,.2f}")
```

## 📊 Feature Explanation

The model expects 19 features (one-hot encoded):

| Index | Feature | Type | Description |
|-------|---------|------|-------------|
| 0 | Rating | Float | Company Glassdoor rating |
| 1-3 | Size_* | Binary | Company size (M, S, XL) |
| 4-5 | Type_* | Binary | Ownership type (Private, Public) |
| 6-7 | Industry_* | Binary | Industry classification |
| 8 | Sector_* | Binary | Business sector |
| 9 | Revenue_* | Binary | Revenue bracket |
| 10 | num_comp | Numeric | Number of competitors |
| 11 | hourly | Binary | Is hourly position (1/0) |
| 12 | employer_provided | Binary | Employer verified salary (1/0) |
| 13-14 | job_state_* | Binary | Job location (CA, NY, etc.) |
| 15 | same_state | Binary | Job location = HQ location |
| 16 | age | Numeric | Company age (years) |
| 17 | python_yn | Binary | Python required (1/0) |
| 18 | spark | Binary | Spark required (1/0) |
| 19 | aws | Binary | AWS required (1/0) |
| 20 | excel | Binary | Excel required (1/0) |
| 21-24 | job_simp_* | Binary | Simplified job role |
| 25 | seniority_* | Binary | Seniority level |

**Note:** Verify exact feature names and order from your model training code.

## 🐛 Troubleshooting

### Model not loading
```
✗ Model file not found
```
**Solution:** Ensure `model_file.p` exists in `flaskapi/models/` directory.

### Wrong number of features
```
Expected 19 features, got X
```
**Solution:** Check that your input array has exactly 19 elements. Verify feature mapping.

### Connection refused
```
ConnectionError: Failed to establish connection
```
**Solution:** Make sure Flask app is running (`python app.py`)

### Port already in use
```
OSError: [Errno 10048] Only one usage of each socket address
```
**Solution:** Change port in `config.py` or kill existing process using port 5000.

## 🚀 Deployment Options

### Development Server (Current)
```bash
python app.py
```
✓ Simple, easy to test
✗ Not production-ready

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
✓ Better performance
✓ Multi-worker support

### Docker Deployment
Create `Dockerfile`:
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Then:
```bash
docker build -t salary-api .
docker run -p 5000:5000 salary-api
```

## 📝 Example: Complete Workflow

### 1. Start API
```bash
python app.py
```

### 2. Send Prediction Request
```python
import requests

# Job data for a senior Data Scientist at a large tech company in CA
features = [
    4.5,      # High company rating
    0, 1, 0,  # Medium size company
    0, 1,     # Public company
    0, 0, 1,  # Tech industry
    1,        # Public sector
    3,        # 3 competitors
    0,        # Annual salary
    1,        # Employer-verified
    1, 0,     # California
    1,        # Same state HQ
    20,       # Company age 20 years
    1,        # Python required
    1,        # Spark required
    1         # AWS required
]

response = requests.post(
    'http://localhost:5000/predict',
    json={'input': features}
)

salary = response.json()['prediction']
print(f"Estimated Salary: ${salary:,.0f}")
```

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Scikit-learn Model Deployment](https://scikit-learn.org/stable/)
- [Gunicorn Documentation](https://gunicorn.org/)

## 📝 Notes

- API returns predictions in the same unit as training data (likely USD annual salary)
- Model was trained on Glassdoor job data with 500+ records
- Features should match the training data format for accurate predictions
- Always validate feature inputs before sending to API

---

**Status**: ✅ Production Ready for Simple Deployment  
**Last Updated**: 2026-06-11
