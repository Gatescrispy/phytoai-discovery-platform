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
- **Repository:** `cedrictantcheu/phytoai-discovery-platform`
- **Branch:** `main`
- **Main file path:** `streamlit_app.py`
- **App URL:** `phytoai-portfolio` (ou votre choix)

#### Étape 3: Dépendances
Le fichier `requirements_streamlit.txt` contient les dépendances optimisées pour le cloud.

### 3. **URLs Finales**
- **App Streamlit:** https://phytoai-portfolio.streamlit.app
- **Repository GitHub:** https://github.com/cedrictantcheu/phytoai-discovery-platform
- **Documentation:** Lien vers le rapport PDF

## 🔧 Configuration Avancée

### Variables d'environnement (si nécessaire)
```toml
# Dans Streamlit Cloud > Settings > Advanced
ENVIRONMENT = "production"
DEBUG = "false"
```

### 📊 Métriques de Performance
- **Temps de chargement:** < 3 secondes
- **Mémoire requise:** < 1GB
- **Compatibilité:** Python 3.9+

## 🎯 Fonctionnalités Déployées
- ✅ Interface principale PhytoAI
- ✅ Visualisations interactives
- ✅ Prédictions IA temps réel
- ✅ Export résultats
- ✅ Mode portfolio optimisé

## 🚨 Troubleshooting

### Erreur de dépendances
```bash
# Si problème avec RDKit sur Streamlit Cloud
pip install rdkit-pypi==2022.9.5
```

### Problème de mémoire
- Utiliser `requirements_streamlit.txt` (version allégée)
- Optimiser les imports conditionnels

### Authentification GitHub
```bash
# Configurer le token GitHub
git remote set-url origin https://[TOKEN]@github.com/cedrictantcheu/phytoai-discovery-platform.git
```

## 📱 Test Local
```bash
# Lancer en local avant déploiement
streamlit run streamlit_app.py

# Ou avec configuration spécifique
streamlit run streamlit_app.py --server.port=8501
```

## 🎨 Personnalisation

### Thème PhytoAI
Le fichier `.streamlit/config.toml` définit:
- Couleurs principales: #667eea
- Layout: wide mode
- Interface: optimisée portfolio

### 🔗 Intégrations
- GitHub badge automatique
- Liens vers documentation
- Mode démo portfolio

---

**🎓 Projet M1 IA School 2024-2025**  
**📧 Support:** [Issues GitHub](https://github.com/cedrictantcheu/phytoai-discovery-platform/issues) 