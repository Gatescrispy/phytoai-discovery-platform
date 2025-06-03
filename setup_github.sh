#!/bin/bash
# 🚀 Configuration GitHub et Push PhytoAI Portfolio

echo "🧬 PhytoAI - Configuration GitHub Repository"
echo "============================================"

# 1. Vérifications préalables
echo "📋 Vérification de l'état Git..."
git status

echo ""
echo "🔍 Configuration Git actuelle:"
echo "Repository: $(git remote get-url origin 2>/dev/null || echo 'Non configuré')"
echo "Branch: $(git branch --show-current)"
echo "Derniers commits:"
git log --oneline -n 3

# 2. Instructions pour créer le repository GitHub
echo ""
echo "🌐 ÉTAPES POUR CRÉER LE REPOSITORY GITHUB:"
echo "=========================================="
echo ""
echo "1. 🌍 Aller sur https://github.com/new"
echo "2. 📝 Nom du repository: phytoai-discovery-platform"
echo "3. 📄 Description: 🧬 PhytoAI - Plateforme de découverte phytothérapeutique assistée par IA | Projet M1 IA School 2024-2025"
echo "4. 🔓 Public repository (pour portfolio)"
echo "5. ❌ NE PAS initialiser avec README (on a déjà les fichiers)"
echo "6. ✅ Cliquer 'Create repository'"

echo ""
echo "🔑 APRÈS CRÉATION DU REPOSITORY:"
echo "==============================="
echo ""
echo "Option A - Push avec token GitHub:"
echo "1. Générer un token: https://github.com/settings/tokens"
echo "2. Permissions: repo (full control)"
echo "3. Copier le token généré"
echo "4. Exécuter: git push https://[TOKEN]@github.com/cedrictantcheu/phytoai-discovery-platform.git main"

echo ""
echo "Option B - Configuration SSH (recommandé):"
echo "1. ssh-keygen -t ed25519 -C 'votre-email@example.com'"
echo "2. cat ~/.ssh/id_ed25519.pub (copier la clé)"
echo "3. Ajouter la clé SSH sur GitHub: Settings > SSH keys"
echo "4. git remote set-url origin git@github.com:cedrictantcheu/phytoai-discovery-platform.git"
echo "5. git push origin main"

echo ""
echo "Option C - GitHub CLI (si installé):"
echo "1. gh auth login"
echo "2. gh repo create phytoai-discovery-platform --public --source=. --push"

echo ""
echo "🎯 APRÈS LE PUSH RÉUSSI:"
echo "======================="
echo "1. Repository: https://github.com/cedrictantcheu/phytoai-discovery-platform"
echo "2. Streamlit Cloud: https://share.streamlit.io"
echo "3. Configurer: Repository > Branch: main > File: streamlit_app.py"
echo "4. URL finale: https://phytoai-portfolio.streamlit.app"

echo ""
echo "📂 FICHIERS PRÊTS POUR LE PUSH:"
echo "==============================="
ls -la | grep -E '\.(py|txt|toml|md|sh)$'

echo ""
echo "✨ Tout est prêt ! Suivez les étapes ci-dessus pour déployer." 