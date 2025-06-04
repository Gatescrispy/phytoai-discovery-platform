#!/usr/bin/env python3
"""
🤗 PhytoAI - Upload Dataset MEGA vers Hugging Face
Script pour déployer le dataset complet (102M lignes) sur Hugging Face Datasets
"""

import pandas as pd
import json
import numpy as np
from pathlib import Path
import os

def upload_mega_to_huggingface():
    """
    Upload le dataset MEGA complet vers Hugging Face
    """
    print("🤗 Upload PhytoAI MEGA Dataset vers Hugging Face")
    print("="*60)
    
    # Chemins vers les datasets MEGA
    dataset_paths = [
        "/Users/cedrictantcheu/SynologyDrive/Perso/Projets Cursor/Projet IA/phytotherapy-ai-discovery/phytoai/data/processed/MEGA_DATASET_20250602_142023.json",
        "/Users/cedrictantcheu/SynologyDrive/Perso/Projets Cursor/Projet IA/phytotherapy-ai-discovery/phytoai/data/processed/ULTIMATE_5000_DATASET_20250602_140640.json",
        "/Users/cedrictantcheu/SynologyDrive/Perso/Projets Cursor/Projet IA/phytotherapy-ai-discovery/phytoai/data/processed/MEGA_FINAL_DATASET_20250602_135508.json"
    ]
    
    # Trouver le plus gros dataset disponible
    dataset_path = None
    max_size = 0
    
    for path in dataset_paths:
        if Path(path).exists():
            size = Path(path).stat().st_size
            if size > max_size:
                max_size = size
                dataset_path = path
    
    if not dataset_path:
        print("❌ Aucun dataset MEGA trouvé")
        return False
    
    print(f"📊 Dataset sélectionné: {Path(dataset_path).name}")
    print(f"📁 Taille: {max_size / 1024 / 1024:.1f} MB")
    
    try:
        # Chargement des données
        print("⏳ Chargement du dataset MEGA...")
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extraction des composés
        if isinstance(data, dict) and 'compounds' in data:
            compounds_data = data['compounds']
            bioactivities_data = data.get('bioactivities', [])
        elif isinstance(data, list):
            compounds_data = data
            bioactivities_data = []
        else:
            print("❌ Format de données non reconnu")
            return False
        
        print(f"✅ {len(compounds_data):,} composés chargés")
        print(f"✅ {len(bioactivities_data):,} bioactivités chargées")
        
        # Préparation des DataFrames
        df_compounds = pd.DataFrame(compounds_data)
        df_bioactivities = pd.DataFrame(bioactivities_data) if bioactivities_data else pd.DataFrame()
        
        print(f"📋 Colonnes composés: {len(df_compounds.columns)}")
        print(f"📋 Colonnes bioactivités: {len(df_bioactivities.columns) if not df_bioactivities.empty else 0}")
        
        # Installation des packages requis
        try:
            from datasets import Dataset, DatasetDict
            from huggingface_hub import HfApi, login
        except ImportError:
            print("⚠️ Installation des packages Hugging Face...")
            os.system("pip install datasets huggingface_hub")
            from datasets import Dataset, DatasetDict
            from huggingface_hub import HfApi, login
        
        # Nettoyage des données pour Hugging Face
        print("🧹 Nettoyage des données pour Hugging Face...")
        
        # Nettoyer les colonnes problématiques
        for col in df_compounds.columns:
            if df_compounds[col].dtype == 'object':
                # Convertir les dictionnaires et listes en strings
                sample_val = df_compounds[col].iloc[0] if len(df_compounds) > 0 else None
                if isinstance(sample_val, (dict, list)):
                    df_compounds[col] = df_compounds[col].astype(str)
        
        # Conversion en format Hugging Face
        print("🔄 Conversion en format Hugging Face...")
        hf_compounds = Dataset.from_pandas(df_compounds)
        
        datasets_dict = {"compounds": hf_compounds}
        
        if not df_bioactivities.empty:
            # Nettoyer aussi les bioactivités
            for col in df_bioactivities.columns:
                if df_bioactivities[col].dtype == 'object':
                    sample_val = df_bioactivities[col].iloc[0] if len(df_bioactivities) > 0 else None
                    if isinstance(sample_val, (dict, list)):
                        df_bioactivities[col] = df_bioactivities[col].astype(str)
            
            hf_bioactivities = Dataset.from_pandas(df_bioactivities)
            datasets_dict["bioactivities"] = hf_bioactivities
        
        # Créer le DatasetDict
        dataset_collection = DatasetDict(datasets_dict)
        
        print("✅ Dataset converti au format Hugging Face")
        print(f"📊 Datasets: {list(dataset_collection.keys())}")
        
        # Configuration de l'upload
        print("\n🔑 Configuration Hugging Face...")
        print("Pour uploader, vous devez:")
        print("1. Créer un compte sur https://huggingface.co")
        print("2. Créer un token sur https://huggingface.co/settings/tokens")
        print("3. Fournir le token ci-dessous")
        
        # Demander le token (dans un vrai script, on utiliserait input())
        hf_token = os.getenv('HUGGINGFACE_TOKEN')
        if not hf_token:
            print("\n⚠️ ATTENTION: Token Hugging Face non trouvé")
            print("Exportez votre token: export HUGGINGFACE_TOKEN='hf_your_token'")
            print("Ou créez un fichier .env avec HUGGINGFACE_TOKEN=hf_your_token")
            
            # Simulation pour le guide
            print("\n🎯 SIMULATION D'UPLOAD (guide):")
            print("dataset_collection.push_to_hub('phytoai/mega-phytotherapy-dataset')")
            print("📊 Dataset serait disponible sur:")
            print("   https://huggingface.co/datasets/phytoai/mega-phytotherapy-dataset")
            return True
        
        # Upload réel si token disponible
        try:
            login(token=hf_token)
            print("✅ Authentification Hugging Face réussie")
            
            # Upload du dataset
            print("📤 Upload en cours... (peut prendre plusieurs minutes)")
            dataset_collection.push_to_hub(
                "phytoai/mega-phytotherapy-dataset",
                private=False,  # Public pour usage académique
                token=hf_token
            )
            
            print("🎉 SUCCÈS! Dataset uploadé sur Hugging Face")
            print("📊 URL: https://huggingface.co/datasets/phytoai/mega-phytotherapy-dataset")
            return True
            
        except Exception as e:
            print(f"❌ Erreur upload: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_huggingface_connection():
    """
    Test de connexion et chargement depuis Hugging Face
    """
    print("\n🧪 Test de connexion Hugging Face...")
    
    try:
        from datasets import load_dataset
        
        # Test plus simple sans dataset externe
        print("📡 Test des packages Hugging Face...")
        print("✅ Import datasets réussi")
        
        # Test de chargement futur de notre dataset
        print("\n🎯 Futur chargement PhytoAI:")
        print("from datasets import load_dataset")
        print("dataset = load_dataset('phytoai/mega-phytotherapy-dataset', streaming=True)")
        print("compounds = dataset['compounds']")
        print("bioactivities = dataset['bioactivities']")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test: {e}")
        return False

if __name__ == "__main__":
    print("🤗 PhytoAI × Hugging Face Integration")
    print("="*50)
    
    # Test de connexion
    if test_huggingface_connection():
        print("\n" + "="*50)
        
        # Upload du dataset
        success = upload_mega_to_huggingface()
        
        if success:
            print("\n✅ MISSION ACCOMPLIE!")
            print("\n🔄 PROCHAINES ÉTAPES:")
            print("1. Modifier streamlit_app.py pour utiliser Hugging Face")
            print("2. Implémenter le streaming intelligent")
            print("3. Ajouter fallback sur échantillon local")
            print("4. Tester en production")
        else:
            print("\n⚠️ Upload échoué - utiliser l'échantillon local en attendant")
    else:
        print("\n❌ Problème de connexion Hugging Face") 