"""
File handling utilities for company name extraction and favicon processing.
"""

import os
from pathlib import Path
from PIL import Image


def get_company_name(filename: str) -> str:
    """
    Extract company name from filename.
    
    Args:
        filename: Name of the uploaded file
        
    Returns:
        str: Extracted company name
    """
    # Remove extension
    name = os.path.splitext(filename)[0]
    # Replace underscores and hyphens with spaces
    name = name.replace('_', ' ').replace('-', ' ')
    # Capitalize words
    return ' '.join(word.capitalize() for word in name.split())


def process_favicon() -> str:
    """
    Process favicon for Streamlit page icon.
    
    Returns:
        str: Path to processed favicon, or default emoji if processing fails
    """
    # Try to find and process favicon
    favicon_paths = ['assets/favicon.png', 'favicon.png']
    
    for path in favicon_paths:
        if os.path.exists(path):
            try:
                img = Image.open(path)
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                return path
            except Exception:
                pass
    
    # Return empty if no favicon found
    return ''

