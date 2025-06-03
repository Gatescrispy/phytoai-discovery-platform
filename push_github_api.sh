#!/bin/bash
# 🚀 Push PhytoAI Portfolio vers GitHub via API

echo "🧬 PhytoAI - Push via API GitHub"
echo "================================"

# Vérifier si un token GitHub est fourni
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Variable GITHUB_TOKEN requise"
    echo "📋 Pour configurer:"
    echo "1. Aller sur https://github.com/settings/tokens"
    echo "2. Générer un token avec permissions 'repo'"
    echo "3. export GITHUB_TOKEN='votre_token_ici'"
    echo "4. Relancer ce script"
    exit 1
fi

REPO_NAME="phytoai-discovery-platform"
OWNER="cedrictantcheu"

echo "🔧 Création du repository $REPO_NAME..."

# Créer le repository via API GitHub
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{
    \"name\": \"$REPO_NAME\",
    \"description\": \"🧬 PhytoAI - Plateforme de découverte phytothérapeutique assistée par IA | Projet M1 IA School 2024-2025\",
    \"private\": false,
    \"auto_init\": false,
    \"homepage\": \"https://phytoai-portfolio.streamlit.app\"
  }"

echo ""
echo "📤 Push du code vers GitHub..."

# Configurer le remote avec le token
git remote set-url origin https://$GITHUB_TOKEN@github.com/$OWNER/$REPO_NAME.git

# Push vers GitHub
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCÈS ! Repository créé et code pushé"
    echo "🌐 Repository: https://github.com/$OWNER/$REPO_NAME"
    echo "📋 Prochaine étape: Déploiement Streamlit Cloud"
    echo "   1. https://share.streamlit.io"
    echo "   2. Repository: $OWNER/$REPO_NAME"
    echo "   3. Branch: main"
    echo "   4. File: streamlit_app.py"
    echo "   5. URL finale: https://phytoai-portfolio.streamlit.app"
else
    echo "❌ Erreur lors du push"
    echo "🔍 Vérifiez votre token GitHub et réessayez"
fi 