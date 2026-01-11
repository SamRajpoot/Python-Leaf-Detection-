# API Documentation

## Leaf Disease Detection API Reference

Complete API documentation for the Leaf Disease Detection System FastAPI service.

### Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://leaf-diseases-detect.vercel.app`

### Authentication
Currently, no authentication is required. API keys may be added in future versions.

---

## Endpoints

### 1. Get API Information

**Endpoint**: `GET /`

**Description**: Retrieve API metadata and available endpoints

**Request**:
```bash
curl -X GET "http://localhost:8000/"
```

**Response** (200 OK):
```json
{
  "message": "Leaf Disease Detection API",
  "version": "1.0.0",
  "description": "AI-powered leaf disease detection using Groq Llama Vision models",
  "endpoints": {
    "disease_detection": "/disease-detection-file (POST)",
    "health_check": "/health (GET)",
    "documentation": "/docs (GET)"
  },
  "status": "operational"
}
```

---

### 2. Health Check

**Endpoint**: `GET /health`

**Description**: Check API health and availability

**Request**:
```bash
curl -X GET "http://localhost:8000/health"
```

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "Leaf Disease Detection API"
}
```

**Use Case**: Monitoring, load balancers, readiness checks

---

### 3. Detect Disease (Main Endpoint)

**Endpoint**: `POST /disease-detection-file`

**Description**: Analyze a leaf image for diseases using AI-powered image analysis

**Request Headers**:
```
Content-Type: multipart/form-data
```

**Request Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | Yes | Leaf image file (JPG, PNG, WebP) |

**Request Examples**:

Using curl:
```bash
curl -X POST "http://localhost:8000/disease-detection-file" \
  -H "accept: application/json" \
  -F "file=@leaf_image.jpg"
```

Using Python requests:
```python
import requests

with open('leaf_image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/disease-detection-file',
        files=files
    )
    result = response.json()
    print(result)
```

Using JavaScript/Fetch:
```javascript
const formData = new FormData();
formData.append('file', document.getElementById('fileInput').files[0]);

fetch('http://localhost:8000/disease-detection-file', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

**Response** (200 OK - Disease Detected):
```json
{
  "disease_detected": true,
  "disease_name": "Early Blight",
  "disease_type": "fungal",
  "severity": "moderate",
  "confidence": 92.5,
  "symptoms": [
    "Brown circular lesions with concentric rings",
    "Lesions primarily on lower leaves",
    "Yellowing around affected areas",
    "Progressive spread up the plant"
  ],
  "possible_causes": [
    "High humidity and wet conditions",
    "Poor air circulation",
    "Overhead watering",
    "Warm temperatures (60-80°F)",
    "Infected crop residue"
  ],
  "treatment": [
    "Remove infected leaves and improve air circulation",
    "Avoid overhead watering; water at soil level",
    "Apply copper fungicide or sulfur-based treatments",
    "Ensure proper spacing between plants",
    "Mulch to prevent soil splash on leaves",
    "Apply fungicide every 7-10 days during growing season"
  ],
  "analysis_timestamp": "2024-01-12T15:30:45.123456+00:00"
}
```

**Response** (200 OK - Healthy Leaf):
```json
{
  "disease_detected": false,
  "disease_name": null,
  "disease_type": "healthy",
  "severity": "none",
  "confidence": 95.2,
  "symptoms": [],
  "possible_causes": [],
  "treatment": [
    "Continue regular maintenance routine",
    "Monitor for any changes in leaf appearance",
    "Maintain proper watering schedule",
    "Ensure adequate sunlight exposure"
  ],
  "analysis_timestamp": "2024-01-12T15:30:45.123456+00:00"
}
```

**Response** (200 OK - Invalid Image):
```json
{
  "disease_detected": false,
  "disease_name": null,
  "disease_type": "invalid_image",
  "severity": "unknown",
  "confidence": 0,
  "symptoms": [
    "Image does not contain a plant leaf",
    "Please upload a clear image of a plant leaf"
  ],
  "possible_causes": [
    "Image contains human, animal, or other non-plant objects",
    "Image is too blurry or unclear",
    "Image is not of a plant leaf"
  ],
  "treatment": [
    "Upload a clear image of a plant leaf",
    "Ensure the leaf fills most of the image",
    "Avoid shadows and ensure proper lighting",
    "Use JPG, PNG, or WebP format"
  ],
  "analysis_timestamp": "2024-01-12T15:30:45.123456+00:00"
}
```

**Error Responses**:

400 Bad Request - Invalid file type:
```json
{
  "detail": "Invalid file type. Supported: image/jpeg, image/png, image/webp"
}
```

400 Bad Request - No file provided:
```json
{
  "detail": "No file provided"
}
```

400 Bad Request - Empty file:
```json
{
  "detail": "File is empty"
}
```

413 Payload Too Large:
```json
{
  "detail": "File size exceeds maximum limit of 10MB"
}
```

500 Internal Server Error:
```json
{
  "detail": "Internal server error. Please try again later."
}
```

---

## Response Schema

### DiseaseAnalysisResult

Complete schema for disease analysis results:

```json
{
  "disease_detected": "boolean - Whether a disease was detected in the leaf",
  "disease_name": "string or null - Name of the detected disease",
  "disease_type": "string - Category: fungal, bacterial, viral, pest, nutrient_deficiency, healthy, or invalid_image",
  "severity": "string - Level: mild, moderate, severe, or none",
  "confidence": "number (0-100) - AI confidence percentage in the analysis",
  "symptoms": [
    "string - Observable disease symptoms"
  ],
  "possible_causes": [
    "string - Environmental or biological factors contributing to disease"
  ],
  "treatment": [
    "string - Evidence-based treatment recommendations"
  ],
  "analysis_timestamp": "string (ISO 8601) - When analysis was performed"
}
```

---

## Disease Categories

The API classifies diseases into the following categories:

| Category | Examples | Characteristics |
|----------|----------|-----------------|
| **Fungal** | Powdery Mildew, Early Blight, Leaf Spot | Spore-based, spreads in humid conditions |
| **Bacterial** | Bacterial Leaf Scorch, Blight | Water-borne, affect vascular system |
| **Viral** | Mosaic Viruses, Leaf Curl | Transmitted by insects, systemic |
| **Pest** | Mite damage, Thrip damage, Aphid damage | Direct feeding damage |
| **Nutrient Deficiency** | Nitrogen deficiency, Iron deficiency | Nutritional imbalance |
| **Healthy** | No disease present | Normal leaf condition |
| **Invalid Image** | Non-leaf images | Not a plant leaf |

---

## Severity Levels

| Severity | Description | Color |
|----------|-------------|-------|
| **Mild** | Early stage, minimal damage | Yellow |
| **Moderate** | Significant symptoms, moderate spread | Orange |
| **Severe** | Advanced disease, severe damage | Red |
| **None** | Healthy leaf | Green |

---

## Supported Image Formats

| Format | MIME Type | Extensions | Notes |
|--------|-----------|-----------|-------|
| JPEG | `image/jpeg` | `.jpg`, `.jpeg` | Most compatible |
| PNG | `image/png` | `.png` | Lossless, larger file size |
| WebP | `image/webp` | `.webp` | Modern, efficient format |

**File Size Limits**:
- Minimum: 1 KB
- Maximum: 10 MB
- Recommended: < 5 MB for faster processing

**Image Quality Recommendations**:
- Clear, well-lit photograph
- Leaf should fill 50-80% of image
- No blur or shadows
- Good color reproduction
- Macro/close-up shots preferred

---

## Rate Limiting

Current version has no rate limiting. Rate limiting may be implemented in future versions.

---

## Error Handling

### Status Codes

| Code | Meaning | Cause |
|------|---------|-------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid parameters |
| 413 | Payload Too Large | File exceeds limit |
| 500 | Internal Server Error | Server-side error |

### Error Response Format

All errors follow this format:
```json
{
  "detail": "Human-readable error message"
}
```

### Common Errors and Solutions

**Error**: "Invalid file type"
- **Cause**: Unsupported image format
- **Solution**: Use JPG, PNG, or WebP format

**Error**: "File size exceeds maximum limit"
- **Cause**: Image file > 10MB
- **Solution**: Compress image before uploading

**Error**: "Internal server error"
- **Cause**: API processing failure
- **Solution**: Retry after a moment; check server logs

---

## Performance Tips

### Optimization Suggestions

1. **Image Compression**
   - Compress before upload to reduce bandwidth
   - Typical: 100KB-1MB is optimal size
   
2. **Request Handling**
   - Implement request timeout: 30-60 seconds
   - Retry failed requests with exponential backoff
   - Use connection pooling for multiple requests

3. **Response Handling**
   - Cache results for identical images
   - Process responses asynchronously
   - Implement proper error handling

### Benchmark Metrics

- **Average Response Time**: 3-5 seconds
- **P95 Response Time**: < 10 seconds
- **Success Rate**: > 99%
- **Maximum Concurrent Requests**: Depends on deployment

---

## Code Examples

### Python

```python
import requests
import json
from pathlib import Path

def analyze_leaf(image_path: str) -> dict:
    """Analyze a leaf image for diseases."""
    url = "http://localhost:8000/disease-detection-file"
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files, timeout=30)
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.Timeout:
        print("Request timeout - API took too long to respond")
    except requests.exceptions.ConnectionError:
        print("Connection error - Could not reach API")
    except Exception as e:
        print(f"Error: {e}")
        return None

# Usage
result = analyze_leaf("leaf_image.jpg")
if result and result['disease_detected']:
    print(f"Disease detected: {result['disease_name']}")
    print(f"Confidence: {result['confidence']}%")
```

### JavaScript

```javascript
async function analyzeLeaf(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(
            'http://localhost:8000/disease-detection-file',
            {
                method: 'POST',
                body: formData,
                timeout: 30000
            }
        );
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.disease_detected) {
            console.log(`Disease: ${result.disease_name}`);
            console.log(`Confidence: ${result.confidence}%`);
        } else {
            console.log("Healthy leaf detected");
        }
        
        return result;
    } catch (error) {
        console.error('Error analyzing leaf:', error);
    }
}

// Usage
const fileInput = document.getElementById('imageInput');
const file = fileInput.files[0];
if (file) {
    analyzeLeaf(file);
}
```

### cURL

```bash
#!/bin/bash

# Analyze leaf image
curl -X POST "http://localhost:8000/disease-detection-file" \
  -H "accept: application/json" \
  -F "file=@leaf_image.jpg" \
  -o result.json

# Pretty print result
jq '.' result.json

# Extract disease name
jq '.disease_name' result.json

# Extract confidence score
jq '.confidence' result.json
```

---

## API Documentation Interface

When running locally, access interactive documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

---

## Support & Troubleshooting

### Common Issues

**Q: How long does analysis take?**
A: Typically 3-5 seconds depending on image size and server load.

**Q: What if the API returns "invalid_image"?**
A: Make sure the image is a clear photo of a plant leaf. The AI will reject images of humans, animals, or objects.

**Q: Can I batch process multiple images?**
A: Currently, each image must be processed separately. Send multiple requests for bulk analysis.

**Q: Is the API free?**
A: The API itself is free. Groq API has free tier usage limits.

### Getting Help

- Check [GitHub Issues](https://github.com/shukur-alom/leaf-diseases-detect/issues)
- Review [README.md](README.md) for setup help
- Check [DEVELOPER.md](DEVELOPER.md) for troubleshooting

---

**API Version**: 1.0.0  
**Last Updated**: January 12, 2024  
**License**: MIT
