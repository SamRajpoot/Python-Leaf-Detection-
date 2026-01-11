"""
Leaf Disease Detection System - FastAPI Backend

A production-ready REST API service for detecting plant leaf diseases using AI-powered
image analysis. Provides secure file upload handling, comprehensive error management,
and JSON response formatting.

Author: Leaf Disease Detection Team
Version: 1.0.0
License: MIT
"""

from fastapi import FastAPI, Request, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from utils import convert_image_to_base64_and_test

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="Leaf Disease Detection API",
    description="AI-powered leaf disease detection system with advanced image analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["info"])
async def root():
    """
    Root endpoint providing API information and available endpoints.
    
    Returns:
        dict: API metadata and endpoint documentation
    """
    return {
        "message": "Leaf Disease Detection API",
        "version": "1.0.0",
        "description": "AI-powered leaf disease detection using Groq Llama Vision models",
        "endpoints": {
            "disease_detection": "/disease-detection-file (POST) - Upload image for disease detection",
            "health_check": "/health (GET) - API health status",
            "documentation": "/docs (GET) - Interactive API documentation"
        },
        "status": "operational"
    }


@app.get("/health", tags=["info"])
async def health_check():
    """
    Health check endpoint for monitoring API availability.
    
    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "service": "Leaf Disease Detection API"
    }


@app.post(
    '/disease-detection-file',
    tags=["disease-detection"],
    summary="Detect disease in leaf image",
    response_description="Disease analysis result with confidence scores and treatment recommendations"
)
async def disease_detection_file(file: UploadFile = File(...)):
    """
    Detect diseases in leaf images using AI analysis.
    
    This endpoint accepts an image file upload and analyzes it for plant leaf diseases.
    Supports JPEG, PNG, and WebP formats. Returns comprehensive disease information
    including identification, severity assessment, confidence scores, and treatment
    recommendations.
    
    Args:
        file (UploadFile): Image file containing the leaf to analyze.
                          Supported formats: JPG, JPEG, PNG, WebP
    
    Returns:
        JSONResponse: Disease analysis result containing:
            - disease_detected (bool): Whether a disease was detected
            - disease_name (str): Name of the detected disease
            - disease_type (str): Category of disease (fungal, bacterial, viral, etc.)
            - severity (str): Severity level (mild, moderate, severe)
            - confidence (float): Confidence percentage (0-100)
            - symptoms (list): Observable disease symptoms
            - possible_causes (list): Environmental/biological factors
            - treatment (list): Evidence-based treatment recommendations
            - analysis_timestamp (str): ISO 8601 timestamp of analysis
    
    Raises:
        HTTPException 400: Invalid file format or no file provided
        HTTPException 413: File size exceeds maximum limit
        HTTPException 500: Internal server error during processing
    
    Example:
        curl -X POST "http://localhost:8000/disease-detection-file" \\
             -H "accept: application/json" \\
             -F "file=@leaf_image.jpg"
    """
    # Validate file upload
    if not file:
        logger.warning("Disease detection requested with no file")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )
    
    # Validate file type
    allowed_types = {"image/jpeg", "image/png", "image/webp"}
    if file.content_type not in allowed_types:
        logger.warning(f"Invalid file type attempted: {file.content_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Supported: {', '.join(allowed_types)}"
        )
    
    try:
        logger.info(f"Processing image for disease detection: {file.filename}")
        
        # Read uploaded file into memory
        contents = await file.read()
        
        # Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024
        if len(contents) > max_size:
            logger.warning(f"File exceeds size limit: {len(contents)} bytes")
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds maximum limit of 10MB"
            )
        
        if len(contents) == 0:
            logger.warning("Empty file provided for disease detection")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is empty"
            )
        
        # Process file and perform disease detection
        result = convert_image_to_base64_and_test(contents)
        
        if result is None:
            logger.error("Failed to process image file")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process image file. Please try again."
            )
        
        logger.info(f"Disease detection completed successfully for: {file.filename}")
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in disease detection: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error. Please try again later."
        )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled exceptions.
    
    Args:
        request (Request): The incoming request
        exc (Exception): The exception that was raised
    
    Returns:
        JSONResponse: Error response with appropriate status code
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
