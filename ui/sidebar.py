"""
Sidebar controls for file upload and metrics selection.
"""

import streamlit as st
from utils.metrics_utils import parse_custom_metrics, get_available_metrics
from typing import Tuple, List


def render_sidebar() -> Tuple[List, List[str]]:
    """
    Render sidebar with file upload and metrics selection.
    
    Returns:
        tuple: (uploaded_files, selected_metrics)
    """
    st.sidebar.header('Upload PDF Files')
    uploaded_files = st.sidebar.file_uploader(
        'Select PDF files to process',
        type=['pdf'],
        accept_multiple_files=True
    )
    
    st.sidebar.markdown('---')
    st.sidebar.header('Select Metrics')
    
    available_metrics = get_available_metrics()
    selected_predefined = []
    
    for key, label in available_metrics.items():
        if st.sidebar.checkbox(label, key=f"metric_{key}"):
            selected_predefined.append(key)
    
    st.sidebar.markdown('---')
    st.sidebar.header('Custom Metrics')
    custom_input = st.sidebar.text_input(
        'Enter custom metrics (comma-separated)',
        placeholder='e.g., EBITDA, Net Income'
    )
    
    custom_metrics = parse_custom_metrics(custom_input)
    all_metrics = selected_predefined + custom_metrics
    
    return uploaded_files, all_metrics

