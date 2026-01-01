"""
Session state initialization utilities.
"""

import streamlit as st


def init_session_state():
    """Initialize session state variables if they don't exist."""
    if 'extraction_results' not in st.session_state:
        st.session_state.extraction_results = []
    
    if 'processing_summary' not in st.session_state:
        st.session_state.processing_summary = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'processing_time': 0.0
        }

