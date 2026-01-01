"""
Application settings and configuration.
"""

import os
import streamlit as st
from utils.file_utils import process_favicon


def setup_page_config():
    """Configure Streamlit page settings including favicon."""
    favicon_path = process_favicon()
    st.set_page_config(
        page_title='Portfolio Metrics Assistant',
        page_icon=favicon_path,
        layout='wide',
        initial_sidebar_state='expanded'
    )


def check_api_key() -> bool:
    """
    Check if OPENAI_API_KEY is set in environment.
    
    Returns:
        bool: True if API key exists, False otherwise
    """
    return os.getenv('OPENAI_API_KEY') is not None

