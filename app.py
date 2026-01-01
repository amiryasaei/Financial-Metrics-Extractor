"""
Main Streamlit application for Portfolio Metrics Assistant.
"""

import streamlit as st
import time
from config.settings import setup_page_config, check_api_key
from ui.layout import render_header
from ui.sidebar import render_sidebar
from ui.results import render_results
from ui.style import inject_style
from utils.state import init_session_state
from extractor import process_all


def main():
    """Main application entry point."""
    setup_page_config()
    inject_style()
    init_session_state()
    
    render_header()
    
    # Check API key
    if not check_api_key():
        st.error("OPENAI_API_KEY not found in environment. Please set it in your .env file.")
        st.stop()
    
    # Sidebar
    uploaded_files, selected_metrics = render_sidebar()
    
    if not uploaded_files:
        st.info("Please upload PDF files using the sidebar to get started.")
        return
    
    if not selected_metrics:
        st.warning("Please select at least one metric to extract.")
        return
    
    # Process button
    if st.button("Extract Metrics", type="primary"):
        with st.spinner("Processing PDFs..."):
            start_time = time.time()
            results = process_all(uploaded_files, selected_metrics)
            end_time = time.time()
            processing_time = end_time - start_time
            
            st.session_state.extraction_results = results
            
            # Update summary
            st.session_state.processing_summary = {
                'total_files': len(results),
                'successful': sum(1 for _, _, err in results if not err),
                'failed': sum(1 for _, _, err in results if err),
                'processing_time': processing_time
            }
    
    # Display results
    if st.session_state.extraction_results:
        render_results(st.session_state.extraction_results)


if __name__ == "__main__":
    main()

