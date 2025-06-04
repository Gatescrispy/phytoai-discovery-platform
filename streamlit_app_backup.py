#!/usr/bin/env python3
"""
🧬 PhytoAI - Application Complète Multi-Pages
Interface Portfolio avec Navigation Intelligente
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Configuration Streamlit
st.set_page_config(
    page_title="🧬 PhytoAI - Découverte Phytothérapeutique",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Gatescrispy/phytoai-discovery-platform',
        'Report a bug': 'https://github.com/Gatescrispy/phytoai-discovery-platform/issues',
        'About': '🧬 PhytoAI - M1 IA School 2024-2025'
    }
)

# Session state
if 'user_session' not in st.session_state:
    st.session_state.user_session = {
        'selected_compounds': [],
        'analysis_history': [],
        'chat_history': [],
        'preferences': {'theme': 'light', 'auto_refresh': True}
    }

# CSS moderne
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(45deg, #667eea, #764ba2);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        transition: transform 0.3s ease;
        margin: 0.5rem 0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 40px rgba(0,0,0,0.15);
    }
    
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .discovery-card {
        background: linear-gradient(135deg, #ff7b7b 0%, #667eea 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .nav-button {
        width: 100%;
        margin: 0.25rem 0;
        padding: 0.75rem;
        border: none;
        border-radius: 10px;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .nav-button:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
</style>
