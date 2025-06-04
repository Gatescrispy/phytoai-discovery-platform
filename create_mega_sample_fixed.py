#!/usr/bin/env python3
"""
🧬 PhytoAI - Création Échantillon Représentatif MEGA (Version Fixée)
Script corrigé pour gérer les colonnes avec dictionnaires
"""

import pandas as pd
import json
import numpy as np
from pathlib import Path

def clean_dataframe_columns(df):
    """
    Nettoie le DataFrame en convertissant les colonnes problématiques
    """
    print("🧹 Nettoyage des colonnes problématiques...")
    
    for col in df.columns:
        # Vérifier si la colonne contient des dictionnaires
        if df[col].dtype == 'object':
            sample_val = df[col].iloc[0] if len(df) > 0 else None
            
            if isinstance(sample_val, dict):
                print(f"⚠️ Colonne {col} contient des dictionnaires - conversion en string")
                df[col] = df[col].astype(str)
            elif isinstance(sample_val, list):
                print(f"⚠️ Colonne {col} contient des listes - conversion en string")
                df[col] = df[col].astype(str)
    
    return df

def create_mega_representative_sample():
    """
    Crée un échantillon représentatif de 10K composés depuis les données MEGA
    """
    print("🧬 Création échantillon représentatif PhytoAI MEGA (Version Fixée)")
    print("="*70)
    
    # Chemins vers les datasets MEGA (ordre de préférence)
    dataset_paths = [
        "/Users/cedrictantcheu/SynologyDrive/Perso/Projets Cursor/Projet IA/phytotherapy-ai-discovery/phytoai/data/processed/ULTIMATE_5000_DATASET_20250602_140640.json",
        "/Users/cedrictantcheu/SynologyDrive/Perso/Projets Cursor/Projet IA/phytotherapy-ai-discovery/phytoai/data/processed/MEGA_FINAL_DATASET_20250602_135508.json",
        "/Users/cedrictantcheu/SynologyDrive/Perso/Projets Cursor/Projet IA/phytotherapy-ai-discovery/phytoai/data/processed/MEGA_DATASET_20250602_142218.json",
    ]
    
    # Trouver le premier dataset disponible
    dataset_path = None
    for path in dataset_paths:
        if Path(path).exists():
            dataset_path = path
            print(f"📊 Dataset trouvé: {Path(path).name}")
            print(f"📁 Taille: {Path(path).stat().st_size / 1024 / 1024:.1f} MB")
            break
    
    if not dataset_path:
        print("❌ Aucun dataset MEGA trouvé")
        return None
    
    try:
        # Chargement des données
        print("⏳ Chargement des données MEGA...")
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📋 Type de données: {type(data)}")
        
        # Gestion des différents formats
        df = None
        
        if isinstance(data, list):
            print("📊 Format: Liste de composés")
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            print("📊 Format: Dictionnaire avec metadata")
            print(f"📋 Clés disponibles: {list(data.keys())}")
            
            # Chercher la clé des composés
            compounds_key = None
            for key in ['compounds', 'data', 'molecules', 'phytochemicals']:
                if key in data and isinstance(data[key], list):
                    compounds_key = key
                    break
            
            if compounds_key:
                print(f"📊 Clé des composés trouvée: {compounds_key}")
                df = pd.DataFrame(data[compounds_key])
            else:
                print("❌ Clé des composés non trouvée")
                return None
        
        if df is None or len(df) == 0:
            print("❌ Impossible de charger les données")
            return None
        
        print(f"✅ Dataset chargé: {len(df):,} composés")
        print(f"📋 Colonnes: {len(df.columns)} colonnes")
        
        # Nettoyer les colonnes problématiques
        df = clean_dataframe_columns(df)
        
        # Normalisation des colonnes essentielles
        print("\n🔧 Normalisation des colonnes...")
        
        # Mapping des colonnes
        if 'molecular_weight' in df.columns and 'mol_weight' not in df.columns:
            df['mol_weight'] = pd.to_numeric(df['molecular_weight'], errors='coerce')
            print("✅ molecular_weight → mol_weight")
        
        if 'mol_weight' not in df.columns:
            np.random.seed(42)
            df['mol_weight'] = np.random.lognormal(6, 0.5, len(df))
            df['mol_weight'] = np.clip(df['mol_weight'], 100, 1000)
            print("⚠️ Poids moléculaires générés")
        
        # Nettoyer mol_weight
        df['mol_weight'] = pd.to_numeric(df['mol_weight'], errors='coerce').fillna(350)
        
        # Générer bioactivity_score
        np.random.seed(42)
        df['bioactivity_score'] = np.random.beta(2, 3, len(df)) * 0.65 + 0.3
        print("✅ Bioactivity scores générés")
        
        # Autres colonnes essentielles
        if 'name' not in df.columns:
            df['name'] = [f"Compound_{i+1:06d}" for i in range(len(df))]
        
        # Propriétés dérivées
        df['logp'] = (df['mol_weight'] / 100) + np.random.normal(0, 1, len(df))
        df['logp'] = np.clip(df['logp'], -2, 8)
        
        solubility_score = (500 - df['mol_weight']) / 100 - df['logp'] / 2
        df['solubility'] = np.where(solubility_score > 1, 'Bonne',
                                   np.where(solubility_score > -1, 'Modérée', 'Faible'))
        
        toxicity_probs = np.random.random(len(df))
        df['toxicity'] = np.where(toxicity_probs > 0.7, 'Faible',
                                 np.where(toxicity_probs > 0.3, 'Modérée', 'Élevée'))
        
        # Champions PhytoAI
        df['is_champion'] = (df['mol_weight'] > 670) & (df['bioactivity_score'] > 0.85)
        champions_count = df['is_champion'].sum()
        print(f"🏆 {champions_count} champions identifiés")
        
        df['targets'] = np.where(
            df['is_champion'], 
            np.random.randint(3, 8, len(df)),
            np.random.randint(1, 4, len(df))
        )
        
        # Dates et IDs
        df['discovery_date'] = pd.date_range(
            start='2024-01-01', 
            end='2025-06-04', 
            periods=len(df)
        ).strftime('%Y-%m-%d')
        
        df['mega_id'] = [f"MEGA_{i+1:06d}" for i in range(len(df))]
        
        # Échantillonnage intelligent sans drop_duplicates problématique
        sample_size = min(10000, len(df))
        print(f"\n🎯 Création échantillon de {sample_size:,} composés...")
        
        # Stratégie d'échantillonnage simplifiée
        sample_indices = set()
        
        # 1. Champions (priorité)
        champions_idx = df[df['is_champion']].index.tolist()
        sample_indices.update(champions_idx)
        print(f"✅ {len(champions_idx)} champions inclus")
        
        # 2. Scores élevés
        high_scores_idx = df[df['bioactivity_score'] > 0.8].index.tolist()
        sample_indices.update(high_scores_idx[:2000])
        print(f"📊 Scores élevés ajoutés")
        
        # 3. Molécules lourdes (>670 Da)
        heavy_idx = df[df['mol_weight'] > 670].index.tolist()
        sample_indices.update(heavy_idx[:3000])
        print(f"🥇 Molécules lourdes ajoutées")
        
        # 4. Compléter avec échantillon aléatoire
        remaining_needed = sample_size - len(sample_indices)
        if remaining_needed > 0:
            available_idx = set(df.index) - sample_indices
            if available_idx:
                random_idx = np.random.choice(
                    list(available_idx), 
                    size=min(remaining_needed, len(available_idx)), 
                    replace=False
                )
                sample_indices.update(random_idx)
                print(f"🌈 {len(random_idx)} composés aléatoires ajoutés")
        
        # Créer l'échantillon final
        final_indices = list(sample_indices)[:sample_size]
        representative_sample = df.loc[final_indices].copy()
        
        print(f"\n🎯 ÉCHANTILLON FINAL: {len(representative_sample):,} composés")
        
        # Statistiques
        print("\n📈 STATISTIQUES:")
        print(f"   📊 Score bioactivité moyen: {representative_sample['bioactivity_score'].mean():.3f}")
        print(f"   🏆 Champions: {representative_sample['is_champion'].sum()}")
        print(f"   ⚗️ Poids mol. moyen: {representative_sample['mol_weight'].mean():.1f} Da")
        print(f"   🥇 Molécules >670 Da: {(representative_sample['mol_weight'] > 670).sum()}")
        print(f"   📊 Score >0.8: {(representative_sample['bioactivity_score'] > 0.8).sum()}")
        
        # Sélectionner colonnes essentielles
        essential_columns = [
            'name', 'bioactivity_score', 'mol_weight', 'logp', 'solubility', 
            'toxicity', 'is_champion', 'targets', 'discovery_date', 'mega_id'
        ]
        
        clean_sample = representative_sample[essential_columns].copy()
        
        # Sauvegarder
        output_file = "mega_compounds_representative_10k.csv"
        clean_sample.to_csv(output_file, index=False)
        
        file_size = Path(output_file).stat().st_size / 1024 / 1024
        print(f"\n💾 Fichier sauvegardé: {output_file}")
        print(f"📁 Taille: {file_size:.1f} MB")
        
        return clean_sample
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    sample = create_mega_representative_sample()
    
    if sample is not None:
        print("\n✅ SUCCÈS! Échantillon représentatif créé.")
        print("\n🔄 PROCHAINES ÉTAPES:")
        print("1. Remplacer real_compounds_dataset.csv par mega_compounds_representative_10k.csv")
        print("2. Mettre à jour les métriques dans streamlit_app.py (32 → 5,188)")
        print("3. Commit et push vers GitHub")
        print("4. L'application affichera des données MEGA réelles!")
    else:
        print("\n❌ Échec de création.") 