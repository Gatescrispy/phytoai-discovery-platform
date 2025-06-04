# 🧬 PhytoAI - Dockerfile pour déploiement
FROM python:3.9-slim

# Informations du projet
LABEL maintainer="TANTCHEU Noussi Cédric <cedric.tantcheu@ia-school.fr>"
LABEL description="PhytoAI - Plateforme IA pour découverte phytothérapeutique"
LABEL version="2.0.0"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false

# Répertoire de travail
WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers de dépendances
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copie du code source et des données
COPY streamlit_app.py .
COPY src/ src/
COPY docs/ docs/
COPY real_compounds_dataset.csv .
COPY real_bioactivities_dataset.csv .
COPY .streamlit/ .streamlit/

# Port d'exposition
EXPOSE 8501

# Point d'entrée
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Commande de démarrage - Point d'entrée correct
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"] 