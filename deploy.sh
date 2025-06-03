#!/bin/bash
# 🚀 Script de déploiement PhytoAI Portfolio

echo "🧬 PhytoAI - Déploiement Portfolio Streamlit"
echo "=========================================="

# 1. Vérification des prérequis
echo "📋 Vérification des fichiers..."
required_files=("streamlit_app.py" "requirements_streamlit.txt" ".streamlit/config.toml")

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

# 3. Validation du code
echo ""
echo "🔍 Validation du code Python..."
python -m py_compile streamlit_app.py && echo "✅ Code valide" || {
    echo "❌ Erreur dans le code Python"
    exit 1
}

# 4. Commit et push
echo ""
echo "📤 Push vers GitHub..."
git add .
git commit -m "🚀 Déploiement Portfolio PhytoAI - $(date '+%Y-%m-%d %H:%M')"

# Note: Le push nécessite l'authentification GitHub
echo "⚠️  Pour pousser vers GitHub, utilisez:"
echo "git push origin main"

# 5. Instructions déploiement Streamlit Cloud
echo ""
echo "🌐 Instructions Streamlit Cloud:"
echo "1. Aller sur https://share.streamlit.io"
echo "2. Connectez-vous avec GitHub"
echo "3. Repository: cedrictantcheu/phytoai-discovery-platform"
echo "4. Branch: main"
echo "5. Main file: streamlit_app.py"
echo ""
echo "🎯 URL finale: https://phytoai-portfolio.streamlit.app"
echo ""
echo "✨ Déploiement préparé avec succès !" 