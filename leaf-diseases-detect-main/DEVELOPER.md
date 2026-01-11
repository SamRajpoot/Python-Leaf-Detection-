# Leaf Disease Detection System - Developer Guide

## Table of Contents
1. [Project Overview](#project-overview)
2. [Development Setup](#development-setup)
3. [Architecture & Components](#architecture--components)
4. [Code Standards](#code-standards)
5. [Testing & Debugging](#testing--debugging)
6. [Deployment Guide](#deployment-guide)
7. [Troubleshooting](#troubleshooting)

---

## Project Overview

### What This Project Does
The Leaf Disease Detection System is an AI-powered application that analyzes photographs of plant leaves and identifies diseases with high accuracy. The system provides:
- Disease identification (fungal, bacterial, viral, pest, nutrient deficiency)
- Severity assessment (mild/moderate/severe)
- Confidence scoring (0-100%)
- Symptom identification
- Treatment recommendations

### Technology Stack
| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend API** | FastAPI | 0.116.1+ |
| **Frontend UI** | Streamlit | 1.28+ |
| **AI Engine** | Groq API + Llama Vision | Latest |
| **Server** | Uvicorn | 0.21.1+ |
| **Language** | Python | 3.8+ |

---

## Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/shukur-alom/leaf-diseases-detect.git
cd leaf-diseases-detect-main
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt

# Optional: Install development dependencies
pip install pytest pytest-asyncio black flake8 mypy
```

### 4. Configure Environment
```bash
# Copy example to actual .env file
cp .env.example .env

# Edit .env with your Groq API key
# Get key from: https://console.groq.com/
```

### 5. Verify Installation
```bash
python -c "import streamlit, fastapi, groq; print('✓ Ready to develop!')"
```

---

## Architecture & Components

### Project Structure
```
leaf-diseases-detect-main/
├── main.py                    # Streamlit web interface
├── app.py                     # FastAPI REST API
├── utils.py                   # Shared utilities
├── test_api.py                # API tests
├── requirements.txt           # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── README.md                  # User documentation
├── DEVELOPER.md               # This file
├── Leaf Disease/
│   ├── main.py                # AI detection engine
│   └── config.py              # Configuration
├── .streamlit/
│   └── config.toml            # Streamlit settings
└── Media/                     # Test images
    └── *.jpg                  # Sample leaf images
```

### Component Details

#### main.py (Streamlit Frontend)
**Purpose**: Interactive web interface for disease detection

**Key Functions**:
- `render_header()`: Display application header
- `render_invalid_image()`: Show error for non-leaf images
- `render_disease_result()`: Display detected disease information
- `render_healthy_leaf()`: Show healthy leaf status
- `process_image()`: Handle image upload and API communication
- `main()`: Application entry point

**Dependencies**:
```python
import streamlit as st      # Web framework
import requests             # HTTP client
from typing import Dict, Any, Optional  # Type hints
```

**How It Works**:
1. User uploads leaf image via file uploader
2. Image is sent to FastAPI backend
3. Backend processes and returns results
4. Results are rendered with custom CSS styling
5. User sees disease info or healthy status

**Styling**: Uses inline CSS with `.stApp` and custom classes for styling

#### app.py (FastAPI Backend)
**Purpose**: RESTful API service for disease detection

**Key Endpoints**:
- `GET /` - API information
- `GET /health` - Health check
- `POST /disease-detection-file` - Main detection endpoint

**Key Features**:
- File upload validation (type, size)
- CORS middleware for cross-origin requests
- Comprehensive error handling
- OpenAPI/Swagger documentation
- Structured logging

**Error Handling**:
- 400 Bad Request - Invalid file type
- 413 Payload Too Large - File exceeds limit
- 500 Internal Server Error - Processing failure

#### utils.py (Utilities)
**Purpose**: Image processing and utility functions

**Key Functions**:
```python
def test_with_base64_data(base64_image_string: str) -> Optional[Dict[str, Any]]
# - Takes base64 encoded image
# - Returns disease analysis result

def convert_image_to_base64_and_test(image_bytes: bytes) -> Optional[Dict[str, Any]]
# - Takes raw image bytes
# - Converts to base64
# - Calls detection engine
```

#### Leaf Disease/main.py (AI Engine)
**Purpose**: Core disease detection using Groq API

**Key Classes**:
```python
class LeafDiseaseDetector:
    def __init__(api_key: Optional[str] = None)
    def analyze_leaf_image_base64(base64_image: str) -> Dict[str, Any]
    # - Sends base64 image to Groq API
    # - Parses response
    # - Returns structured result

@dataclass
class DiseaseAnalysisResult:
    disease_detected: bool
    disease_name: Optional[str]
    disease_type: str
    severity: str
    confidence: float
    symptoms: List[str]
    possible_causes: List[str]
    treatment: List[str]
    analysis_timestamp: str
```

---

## Code Standards

### Python Style Guide
- Follow **PEP 8** naming conventions
- Use **type hints** for all function parameters and returns
- Write **docstrings** for all functions and classes
- Keep functions **focused and single-purpose**
- Maximum line length: **100 characters**

### Example Function:
```python
def analyze_image(image_bytes: bytes, max_retries: int = 3) -> Optional[Dict[str, Any]]:
    """
    Analyze a leaf image for diseases.
    
    Args:
        image_bytes (bytes): Raw image data
        max_retries (int): Maximum API retry attempts
    
    Returns:
        Optional[Dict[str, Any]]: Disease analysis result or None if failed
    
    Example:
        >>> with open('leaf.jpg', 'rb') as f:
        ...     result = analyze_image(f.read())
        >>> if result:
        ...     print(result['disease_name'])
    """
    if not image_bytes:
        logger.error("No image data provided")
        return None
    # ... implementation
```

### Naming Conventions
```python
# Classes: PascalCase
class LeafDiseaseDetector:
    pass

# Functions: snake_case
def detect_disease():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_IMAGE_SIZE = 10_000_000

# Private: _leading_underscore
def _internal_method():
    pass
```

### Logging Best Practices
```python
import logging

logger = logging.getLogger(__name__)

# Usage
logger.debug("Detailed diagnostic info")
logger.info("General informational message")
logger.warning("Warning about potential issues")
logger.error("Error occurred", exc_info=True)
logger.critical("Critical system failure")
```

---

## Testing & Debugging

### Manual API Testing with curl
```bash
# Test disease detection endpoint
curl -X POST "http://localhost:8000/disease-detection-file" \
  -F "file=@Media/test_image.jpg"

# Test health check
curl -X GET "http://localhost:8000/health"

# Test root endpoint
curl -X GET "http://localhost:8000/"
```

### Testing with Python
```python
import requests
from pathlib import Path

# Test with local image
image_path = "Media/test_image.jpg"
with open(image_path, 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/disease-detection-file',
        files=files
    )
    print(response.json())
```

### Running Tests
```bash
# Run all tests
pytest test_api.py -v

# Run specific test
pytest test_api.py::test_disease_detection -v

# Run with coverage
pytest test_api.py --cov=. --cov-report=html
```

### Debugging Tips

**Issue**: "ModuleNotFoundError: No module named 'groq'"
```bash
pip install -r requirements.txt
```

**Issue**: API Key not found
```bash
# Check .env file exists
ls -la .env

# Verify API key is set
echo $GROQ_API_KEY
```

**Issue**: Port already in use
```bash
# Kill process using port 8000
# Windows: netstat -ano | findstr :8000
# Linux: lsof -i :8000

# Or use different port
uvicorn app:app --port 8001
```

**Enable Debug Logging**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Deployment Guide

### Local Development
```bash
# Terminal 1: Start FastAPI
uvicorn app:app --reload --port 8000

# Terminal 2: Start Streamlit
streamlit run main.py --server.port 8501
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t leaf-disease-detector .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key leaf-disease-detector
```

### Vercel Deployment
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# For Python API, use serverless function
# See vercel.json configuration
```

### Environment Variables for Production
```bash
export GROQ_API_KEY="your-production-key"
export ENVIRONMENT="production"
export LOG_LEVEL="WARNING"
uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## Troubleshooting

### Common Issues

#### 1. API Key Issues
```
Error: "GROQ_API_KEY not found in environment"
```
**Solution**:
- Get key from https://console.groq.com/
- Add to .env file: `GROQ_API_KEY=your_key_here`
- Reload environment: `source venv/bin/activate`

#### 2. Image Processing Errors
```
Error: "Failed to process image file"
```
**Solution**:
- Check image format (JPG, PNG, WebP supported)
- Verify file size < 10MB
- Ensure image is valid leaf photo

#### 3. API Connection Timeout
```
Error: "Request timeout. Please try again."
```
**Solution**:
- Check internet connection
- Verify Groq API is accessible
- Increase timeout in code: `timeout=60`

#### 4. Port Already in Use
```
Error: "Address already in use"
```
**Solution**:
- Find process: `lsof -i :8000`
- Kill process: `kill -9 <PID>`
- Or use different port: `--port 8001`

---

## Contributing

### Before Submitting Code
1. **Format**: Run `black . && isort .`
2. **Lint**: Run `flake8 .`
3. **Type Check**: Run `mypy .`
4. **Test**: Run `pytest .`
5. **Document**: Update relevant docstrings and README

### Pull Request Process
1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes and test thoroughly
3. Commit with clear messages: `git commit -m "Add feature: description"`
4. Push to branch: `git push origin feature/my-feature`
5. Create Pull Request with description

---

## Performance Tips

### Optimize Image Processing
- Pre-compress images before upload
- Use PNG for lossless, JPG for faster processing
- Limit image size to < 5MB for faster processing

### API Performance
- Use connection pooling with requests
- Implement caching for repeated analyses
- Monitor API response times

### Streamlit Performance
- Use @st.cache_data for expensive operations
- Minimize re-renders with st.form
- Use st.columns() for layout efficiency

---

## Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Streamlit Documentation**: https://docs.streamlit.io/
- **Groq API Docs**: https://console.groq.com/docs/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html
- **PEP 8 Style Guide**: https://pep8.org/

---

**Last Updated**: January 12, 2024  
**Maintainer**: Leaf Disease Detection Team  
**License**: MIT
