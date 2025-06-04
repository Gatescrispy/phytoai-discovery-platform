#!/usr/bin/env python3
"""
🤗 PhytoAI × Hugging Face Integration
Module pour charger les données MEGA depuis Hugging Face avec fallback intelligent
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Optional, Tuple
import logging

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@st.cache_data(ttl=3600, show_spinner=True)
def load_mega_from_huggingface(
    dataset_name: str = "phytoai/mega-phytotherapy-dataset",
    max_compounds: int = 10000,
    streaming: bool = True
) -> Tuple[pd.DataFrame, pd.DataFrame, dict]:
    """
    Charge les données MEGA depuis Hugging Face avec streaming intelligent
    
    Args:
        dataset_name: Nom du dataset sur Hugging Face
        max_compounds: Nombre max de composés à charger (pour limiter la mémoire)
        streaming: Utiliser le streaming ou charger tout
    
    Returns:
        Tuple[compounds_df, bioactivities_df, metadata]
    """
    
    try:
        # Tentative d'import des packages Hugging Face
        from datasets import load_dataset
        logger.info("🤗 Packages Hugging Face disponibles")
        
        # Configuration du chargement
        load_config = {
            "streaming": streaming,
            "trust_remote_code": True  # Pour datasets personnalisés
        }
        
        st.info(f"🔄 Chargement depuis Hugging Face: {dataset_name}")
        
        # Chargement du dataset
        try:
            dataset = load_dataset(dataset_name, **load_config)
            
            if streaming:
                # Mode streaming - charge par chunks
                compounds_data = []
                bioactivities_data = []
                
                # Charger les composés en streaming
                if 'compounds' in dataset:
                    st.write("📊 Chargement des composés en streaming...")
                    compounds_stream = dataset['compounds']
                    
                    # Prendre un échantillon intelligent
                    count = 0
                    for compound in compounds_stream:
                        compounds_data.append(compound)
                        count += 1
                        
                        if count >= max_compounds:
                            break
                    
                    st.success(f"✅ {len(compounds_data):,} composés chargés depuis Hugging Face")
                
                # Charger les bioactivités si disponibles
                if 'bioactivities' in dataset:
                    st.write("🧪 Chargement des bioactivités...")
                    bioactivities_stream = dataset['bioactivities']
                    
                    count = 0
                    for bioactivity in bioactivities_stream:
                        bioactivities_data.append(bioactivity)
                        count += 1
                        
                        if count >= max_compounds * 3:  # Plus de bioactivités que de composés
                            break
                    
                    st.success(f"✅ {len(bioactivities_data):,} bioactivités chargées")
                
            else:
                # Mode complet - charge tout (attention mémoire!)
                st.warning("⚠️ Chargement complet - peut être lent avec gros datasets")
                
                compounds_data = list(dataset['compounds']) if 'compounds' in dataset else []
                bioactivities_data = list(dataset['bioactivities']) if 'bioactivities' in dataset else []
        
        except Exception as hf_error:
            logger.error(f"Erreur Hugging Face: {hf_error}")
            raise hf_error
        
        # Conversion en DataFrames
        compounds_df = pd.DataFrame(compounds_data) if compounds_data else pd.DataFrame()
        bioactivities_df = pd.DataFrame(bioactivities_data) if bioactivities_data else pd.DataFrame()
        
        # Métadonnées
        metadata = {
            'source': 'huggingface',
            'dataset_name': dataset_name,
            'compounds_count': len(compounds_df),
            'bioactivities_count': len(bioactivities_df),
            'streaming_used': streaming,
            'max_loaded': max_compounds
        }
        
        logger.info(f"✅ Données chargées depuis Hugging Face: {metadata}")
        return compounds_df, bioactivities_df, metadata
        
    except ImportError:
        logger.warning("⚠️ Packages Hugging Face non installés")
        raise ImportError("Packages Hugging Face manquants")
        
    except Exception as e:
        logger.error(f"❌ Erreur chargement Hugging Face: {e}")
        raise e

@st.cache_data(ttl=1800)
def load_local_fallback() -> Tuple[pd.DataFrame, pd.DataFrame, dict]:
    """
    Fallback sur les données locales si Hugging Face échoue
    """
    try:
        # Chargement du dataset local (échantillon représentatif)
        compounds_df = pd.read_csv("real_compounds_dataset.csv")
        
        # Pas de bioactivités séparées dans le fallback local
        bioactivities_df = pd.DataFrame()
        
        metadata = {
            'source': 'local_fallback',
            'compounds_count': len(compounds_df),
            'bioactivities_count': 0,
            'note': 'Échantillon représentatif local'
        }
        
        return compounds_df, bioactivities_df, metadata
        
    except Exception as e:
        logger.error(f"❌ Erreur fallback local: {e}")
        raise e

def load_phytoai_data_smart(
    prefer_huggingface: bool = True,
    max_compounds: int = 10000
) -> Tuple[pd.DataFrame, pd.DataFrame, dict]:
    """
    Chargement intelligent des données PhytoAI avec stratégie de fallback
    
    Args:
        prefer_huggingface: Essayer Hugging Face d'abord
        max_compounds: Limite de composés pour éviter surcharge mémoire
    
    Returns:
        Tuple[compounds_df, bioactivities_df, metadata]
    """
    
    st.markdown("### 🔄 Chargement Intelligent des Données PhytoAI")
    
    if prefer_huggingface:
        try:
            # Tentative Hugging Face
            st.info("🎯 Stratégie #1: Hugging Face (dataset complet)")
            compounds_df, bioactivities_df, metadata = load_mega_from_huggingface(
                max_compounds=max_compounds
            )
            
            if len(compounds_df) > 0:
                st.success(f"🎉 Succès Hugging Face! {len(compounds_df):,} composés chargés")
                return compounds_df, bioactivities_df, metadata
            
        except Exception as e:
            st.warning(f"⚠️ Hugging Face indisponible: {str(e)[:100]}...")
            logger.warning(f"Fallback nécessaire: {e}")
    
    # Fallback sur données locales
    st.info("🎯 Stratégie #2: Dataset local (échantillon représentatif)")
    try:
        compounds_df, bioactivities_df, metadata = load_local_fallback()
        st.success(f"✅ Fallback réussi! {len(compounds_df):,} composés locaux")
        return compounds_df, bioactivities_df, metadata
        
    except Exception as e:
        st.error(f"❌ Échec des deux stratégies: {e}")
        # Dataset vide en dernier recours
        return pd.DataFrame(), pd.DataFrame(), {'source': 'empty', 'error': str(e)}

def display_data_source_info(metadata: dict):
    """
    Affiche les informations sur la source des données
    """
    source = metadata.get('source', 'unknown')
    
    if source == 'huggingface':
        st.success(f"""
        🤗 **Source: Hugging Face** (Dataset MEGA complet)
        - 📊 Composés: {metadata.get('compounds_count', 0):,}
        - 🧪 Bioactivités: {metadata.get('bioactivities_count', 0):,}
        - 🔄 Streaming: {'Oui' if metadata.get('streaming_used') else 'Non'}
        - 📈 Limite chargée: {metadata.get('max_loaded', 'N/A'):,}
        """)
        
    elif source == 'local_fallback':
        st.info(f"""
        💾 **Source: Échantillon Local** (Fallback)
        - 📊 Composés: {metadata.get('compounds_count', 0):,}
        - ℹ️ Note: {metadata.get('note', 'Données représentatives')}
        """)
        
    elif source == 'empty':
        st.error(f"""
        ❌ **Aucune donnée disponible**
        - Erreur: {metadata.get('error', 'Inconnue')}
        """)

def get_enhanced_metrics(compounds_df: pd.DataFrame, metadata: dict) -> dict:
    """
    Calcule des métriques améliorées basées sur les données chargées
    """
    if len(compounds_df) == 0:
        return {}
    
    base_metrics = {
        'total_compounds': len(compounds_df),
        'data_source': metadata.get('source', 'unknown')
    }
    
    # Métriques spécifiques selon les colonnes disponibles
    if 'mol_weight' in compounds_df.columns:
        base_metrics['avg_mol_weight'] = compounds_df['mol_weight'].mean()
        base_metrics['heavy_molecules'] = (compounds_df['mol_weight'] > 670).sum()
    
    if 'bioactivity_score' in compounds_df.columns:
        base_metrics['avg_bioactivity'] = compounds_df['bioactivity_score'].mean()
        base_metrics['high_activity'] = (compounds_df['bioactivity_score'] > 0.8).sum()
    
    if 'is_champion' in compounds_df.columns:
        base_metrics['champions'] = compounds_df['is_champion'].sum()
    
    return base_metrics

# Interface Streamlit pour tester l'intégration
def test_integration_ui():
    """
    Interface de test pour l'intégration Hugging Face
    """
    st.title("🧪 Test Intégration Hugging Face")
    
    st.markdown("### Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        prefer_hf = st.checkbox("Préférer Hugging Face", value=True)
        max_compounds = st.slider("Max composés", 1000, 50000, 10000)
    
    with col2:
        dataset_name = st.text_input(
            "Dataset Hugging Face", 
            value="phytoai/mega-phytotherapy-dataset"
        )
    
    if st.button("🚀 Tester Chargement"):
        with st.spinner("Chargement en cours..."):
            compounds_df, bioactivities_df, metadata = load_phytoai_data_smart(
                prefer_huggingface=prefer_hf,
                max_compounds=max_compounds
            )
        
        # Afficher les résultats
        display_data_source_info(metadata)
        
        if len(compounds_df) > 0:
            st.markdown("### 📊 Aperçu des Données")
            st.dataframe(compounds_df.head())
            
            # Métriques
            metrics = get_enhanced_metrics(compounds_df, metadata)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Composés Total", metrics.get('total_compounds', 0))
            with col2:
                st.metric("Champions", metrics.get('champions', 'N/A'))
            with col3:
                st.metric("Poids Mol. Moyen", f"{metrics.get('avg_mol_weight', 0):.1f} Da")

if __name__ == "__main__":
    test_integration_ui() 