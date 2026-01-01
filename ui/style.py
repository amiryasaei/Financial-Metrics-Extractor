"""
UI styling and theme injection.
"""

import streamlit as st
from config.colors import PRIMARY_NAVY, ACCENT_GOLD, BG_COLOR


def inject_style():
    """Inject custom CSS styling into Streamlit app."""
    st.markdown(f"""
    <style>
        .main {{
            background-color: {BG_COLOR};
        }}
        .stButton>button {{
            background-color: {PRIMARY_NAVY};
            color: {ACCENT_GOLD};
            border-radius: 5px;
            border: none;
            padding: 0.5rem 1rem;
        }}
        .stButton>button:hover {{
            background-color: {ACCENT_GOLD};
            color: {PRIMARY_NAVY};
        }}
        h1 {{
            color: {PRIMARY_NAVY};
        }}
    </style>
    """, unsafe_allow_html=True)
