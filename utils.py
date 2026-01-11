"""
Utility functions for Leaf Disease Detection System

This module provides image processing, base64 encoding, and utility functions
for the leaf disease detection system. It handles image conversion and
communication with the AI detection engine.

Functions:
    test_with_base64_data: Test disease detection with base64 encoded images
    convert_image_to_base64_and_test: Convert image bytes and perform detection

Author: Leaf Disease Detection Team
License: MIT
"""

import json
import sys
import os
import base64
from pathlib import Path
from typing import Optional, Dict, Any
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Add the Leaf Disease directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "Leaf Disease"))

try:
    from main import LeafDiseaseDetector
except ImportError as e:
    logger.error(f"Could not import LeafDiseaseDetector: {str(e)}")
    raise ImportError(f"Failed to import LeafDiseaseDetector module: {str(e)}")


def test_with_base64_data(base64_image_string: str) -> Optional[Dict[str, Any]]:
    """
    Test disease detection with base64 encoded image data.
    
    Takes a base64 encoded image string and sends it to the LeafDiseaseDetector
    for AI-powered analysis. Returns structured disease analysis results.
    
    Args:
        base64_image_string (str): Base64 encoded image data without data URI prefix
    
    Returns:
        Optional[Dict[str, Any]]: Disease analysis result dictionary containing:
            - disease_detected (bool): Whether a disease was detected
            - disease_name (str): Identified disease name
            - disease_type (str): Category (fungal, bacterial, viral, etc.)
            - severity (str): Severity level (mild, moderate, severe)
            - confidence (float): Confidence percentage (0-100)
            - symptoms (list): Observable symptoms
            - possible_causes (list): Environmental/biological factors
            - treatment (list): Treatment recommendations
            - analysis_timestamp (str): ISO 8601 timestamp
        
        Returns None if detection fails.
    
    Raises:
        ValueError: If base64_image_string is empty or invalid
        Exception: If API communication fails
    
    Example:
        >>> base64_data = "iVBORw0KGgoAAAANS..."
        >>> result = test_with_base64_data(base64_data)
        >>> if result and result.get('disease_detected'):
        ...     print(f"Disease found: {result['disease_name']}")
    """
    if not base64_image_string or not isinstance(base64_image_string, str):
        logger.error("Invalid base64 image string provided")
        return None
    
    try:
        logger.info("Initializing LeafDiseaseDetector for base64 analysis")
        detector = LeafDiseaseDetector()
        
        logger.info("Analyzing leaf image with AI engine")
        result = detector.analyze_leaf_image_base64(base64_image_string)
        
        logger.info("Disease detection completed successfully")
        return result
    
    except Exception as e:
        logger.error(f"Error during base64 disease detection: {str(e)}", exc_info=True)
        return None


def convert_image_to_base64_and_test(image_bytes: bytes) -> Optional[Dict[str, Any]]:
    """
    Convert image bytes to base64 and perform disease detection.
    
    This is the primary function for converting image file data to base64 format
    and passing it to the disease detection engine. Handles the complete workflow
    from raw image bytes to structured disease analysis results.
    
    Args:
        image_bytes (bytes): Raw image data in bytes format
    
    Returns:
        Optional[Dict[str, Any]]: Disease analysis result (see test_with_base64_data
            return value). Returns None if conversion or detection fails.
    
    Raises:
        ValueError: If image_bytes is empty
        Exception: If base64 encoding or detection fails
    
    Example:
        >>> with open('leaf_image.jpg', 'rb') as f:
        ...     image_data = f.read()
        >>> result = convert_image_to_base64_and_test(image_data)
        >>> if result:
        ...     print(json.dumps(result, indent=2))
    """
    if not image_bytes or len(image_bytes) == 0:
        logger.error("No image bytes provided for conversion")
        return None
    
    try:
        logger.info(f"Converting image to base64 ({len(image_bytes)} bytes)")
        
        # Encode image bytes to base64 string
        base64_string = base64.b64encode(image_bytes).decode('utf-8')
        logger.info(f"Base64 encoding completed ({len(base64_string)} characters)")
        
        # Perform disease detection with base64 data
        return test_with_base64_data(base64_string)
    
    except UnicodeDecodeError as e:
        logger.error(f"Error decoding base64 string: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error during image conversion: {str(e)}", exc_info=True)
        return None


def main():
    """
    Main function for standalone testing (not typically used in production).
    
    Demonstrates how to use the conversion functions with a local image file.
    """
    logger.info("Starting standalone utility test")
    image_path = "Media/brown-spot-4 (1).jpg"
    
    if not os.path.exists(image_path):
        logger.error(f"Test image not found: {image_path}")
        return
    
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        result = convert_image_to_base64_and_test(image_data)
        if result:
            print(json.dumps(result, indent=2))
        else:
            logger.error("Failed to analyze image")
    
    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()
