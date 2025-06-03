#!/usr/bin/env python3
"""
🧬 PhytoAI - Portfolio Streamlit
Point d'entrée principal pour le déploiement Streamlit Cloud
"""

import streamlit as st
import sys
from pathlib import Path

# Ajouter le dossier src au path Python
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import et lancement de l'application
from dashboard.app import *

if __name__ == "__main__":
    # L'application est déjà configurée dans app.py
    pass 