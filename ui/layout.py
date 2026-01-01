"""
Layout components: header rendering.
"""

import streamlit as st
from config.colors import ACCENT_GOLD


def render_header():
    """Render the main header with title."""
    st.title('Portfolio Metrics Assistant')
    st.markdown('---')

