#!/bin/bash
# 🚀 Script de déploiement PhytoAI Portfolio

echo "🧬 PhytoAI - Déploiement Portfolio Streamlit"
echo "=========================================="

# 1. Vérification des prérequis
echo "📋 Vérification des fichiers..."
required_files=("streamlit_app.py" "requirements.txt" ".streamlit/config.toml" "real_compounds_dataset.csv")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file manquant"
        exit 1
    fi
done

# 2. Test local de l'application
echo ""
echo "🧪 Test de l'application Streamlit..."
python -c "import streamlit as st; print('✅ Streamlit installé')" || {
    echo "❌ Streamlit non installé. Installation..."
    pip install streamlit
}

# 3. Test des dépendances IA
echo ""
echo "🤖 Vérification des dépendances IA..."
python -c "import google.generativeai as genai; print('✅ Google Generative AI installé')" || {
    echo "❌ Google Generative AI manquant. Installation..."
    pip install google-generativeai>=0.8.3
}

# 4. Validation du code
echo ""
echo "🔍 Validation du code Python..."
python -m py_compile streamlit_app.py && echo "✅ Code principal valide" || {
    echo "❌ Erreur dans streamlit_app.py"
    exit 1
}

python -c "from src.dashboard.pages_advanced import *; print('✅ Modules avancés valides')" || {
    echo "⚠️ Modules avancés non disponibles (mode dégradé)"
}

# 5. Test du chargement des données
echo ""
echo "📊 Test du chargement des données..."
python -c "
import pandas as pd
try:
    df = pd.read_csv('real_compounds_dataset.csv')
    print(f'✅ Données réelles: {len(df)} composés')
except:
    print('❌ Erreur chargement données')
    exit(1)
"

# 6. Commit et push
echo ""
echo "📤 Push vers GitHub..."
git add .
git commit -m "🚀 Déploiement Portfolio PhytoAI v2.0 - $(date '+%Y-%m-%d %H:%M')"

# Note: Le push nécessite l'authentification GitHub
echo "⚠️  Pour pousser vers GitHub, utilisez:"
echo "git push origin main"

# 7. Instructions déploiement Streamlit Cloud
echo ""
echo "🌐 Instructions Streamlit Cloud:"
echo "1. Aller sur https://share.streamlit.io"
echo "2. Connectez-vous avec GitHub"
echo "3. Repository: Gatescrispy/phytoai-discovery-platform"
echo "4. Branch: main"
echo "5. Main file: PhytoAI-Portfolio/streamlit_app.py"
echo ""
echo "🎯 URL actuelle: https://phytoai-portfolio-platform.streamlit.app"
echo ""
echo "🔑 N'oubliez pas d'ajouter GEMINI_API_KEY dans les secrets Streamlit Cloud!"
echo ""
echo "✨ Déploiement préparé avec succès !" 