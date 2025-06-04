# 🚀 Guide de Déploiement PhytoAI

## 📋 Instructions Streamlit Cloud

### 1. **Préparation GitHub**
```bash
# Assurer que tous les fichiers sont pushés
git add .
git commit -m "🚀 Configuration Streamlit Cloud"
git push origin main
```

### 2. **Déploiement sur Streamlit Cloud**

#### Étape 1: Connexion
1. Aller sur [share.streamlit.io](https://share.streamlit.io)
2. Se connecter avec votre compte GitHub
3. Cliquer sur "New app"

#### Étape 2: Configuration
- **Repository:** `Gatescrispy/phytoai-discovery-platform`
- **Branch:** `main`
- **Main file path:** `PhytoAI-Portfolio/streamlit_app.py`
- **App URL:** `phytoai-portfolio-platform` (URL actuelle)

#### Étape 3: Dépendances
Le fichier `requirements.txt` contient les dépendances optimisées pour le cloud.

### 3. **URLs Finales**
- **App Streamlit:** https://phytoai-portfolio-platform.streamlit.app
- **Repository GitHub:** https://github.com/Gatescrispy/phytoai-discovery-platform
- **Documentation:** Lien vers le rapport PDF

## 🔧 Configuration Avancée

### Variables d'environnement (si nécessaire)
```toml
# Dans Streamlit Cloud > Settings > Advanced
ENVIRONMENT = "production"
DEBUG = "false"
GEMINI_API_KEY = "votre_clé_api_gemini"
```

### 📊 Métriques de Performance
- **Temps de chargement:** < 3 secondes
- **Mémoire requise:** < 1GB
- **Compatibilité:** Python 3.9+

## 🎯 Fonctionnalités Déployées
- ✅ Interface principale PhytoAI (9 pages)
- ✅ Assistant IA avec Gemini intégré
- ✅ Données réelles (32 composés + 229 bioactivités)
- ✅ Visualisations interactives
- ✅ Prédictions IA temps réel
- ✅ Export résultats
- ✅ Mode portfolio optimisé

## 🚨 Troubleshooting

### Erreur de dépendances
```bash
# Si problème avec Google Generative AI
pip install google-generativeai>=0.8.3
```

### Problème de mémoire
- Utiliser chunks pour chargement données
- Optimiser les imports conditionnels

### Authentification GitHub
```bash
# Configurer le token GitHub
git remote set-url origin https://[TOKEN]@github.com/Gatescrispy/phytoai-discovery-platform.git
```

## 📱 Test Local
```bash
# Lancer en local avant déploiement
cd PhytoAI-Portfolio
streamlit run streamlit_app.py

# Ou avec port spécifique
streamlit run streamlit_app.py --server.port=8502
```

## 🎨 Personnalisation

### Thème PhytoAI
Le fichier `.streamlit/config.toml` définit:
- Couleurs principales: #667eea
- Layout: wide mode
- Interface: optimisée portfolio

### 🔗 Intégrations
- Assistant IA avec clé Gemini
- GitHub badge automatique
- Liens vers documentation
- Mode démo portfolio

---

**🎓 Projet M1 IA School 2024-2025**  
**📧 Support:** [Issues GitHub](https://github.com/Gatescrispy/phytoai-discovery-platform/issues) 