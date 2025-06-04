#!/usr/bin/env python3
"""
🚀 PhytoAI - Intégration MEGA 1.4M Molécules pour Streamlit
Connexion directe aux 1.4M molécules avec streaming intelligent
"""

import streamlit as st
import pandas as pd
import json
import numpy as np
from pathlib import Path
import random
from datetime import datetime, timedelta

class MegaDatabaseConnector:
    def __init__(self):
        # Chemins vers le dataset MEGA de 1.4M molécules
        self.mega_path = "./phytotherapy-ai-discovery/phytoai/data/processed/MEGA_DATASET_20250602_142023.json"
        self.fallback_path = "./real_compounds_dataset.csv"
        
        # Cache pour optimiser les performances
        self._mega_data = None
        self._mega_loaded = False
        
    @st.cache_data(ttl=3600)
    def load_mega_dataset(_self):
        """
        Chargement intelligent du dataset MEGA de 1.4M molécules
        """
        print("🚀 Chargement du dataset MEGA 1.4M molécules...")
        
        try:
            # Vérification de l'existence du fichier MEGA
            if not Path(_self.mega_path).exists():
                print(f"⚠️ Dataset MEGA non trouvé: {_self.mega_path}")
                return _self._load_fallback_dataset()
            
            # Chargement du dataset MEGA complet
            with open(_self.mega_path, 'r') as f:
                mega_data = json.load(f)
            
            if 'compounds' in mega_data:
                compounds = mega_data['compounds']
                bioactivities = mega_data.get('bioactivities', [])
                
                print(f"✅ Dataset MEGA chargé: {len(compounds):,} molécules")
                
                # Conversion en format optimisé pour Streamlit
                compounds_df = pd.DataFrame(compounds)
                bioactivities_df = pd.DataFrame(bioactivities)
                
                _self._mega_data = {
                    'compounds': compounds_df,
                    'bioactivities': bioactivities_df,
                    'raw_compounds': compounds
                }
                _self._mega_loaded = True
                
                return compounds_df, bioactivities_df, "🟢 CONNECTÉ aux 1.4M molécules MEGA"
            else:
                print("❌ Structure MEGA invalide")
                return _self._load_fallback_dataset()
                
        except Exception as e:
            print(f"❌ Erreur chargement MEGA: {e}")
            return _self._load_fallback_dataset()
    
    def _load_fallback_dataset(self):
        """Fallback sur l'échantillon local si MEGA non disponible"""
        try:
            compounds_df = pd.read_csv(self.fallback_path)
            bioactivities_df = pd.DataFrame()  # Vide pour l'échantillon
            
            print(f"⚠️ Fallback activé: {len(compounds_df):,} molécules")
            return compounds_df, bioactivities_df, "🟡 Échantillon local actif"
            
        except Exception as e:
            print(f"❌ Erreur fallback: {e}")
            return pd.DataFrame(), pd.DataFrame(), "🔴 Données non disponibles"
    
    @st.cache_data(ttl=1800)
    def search_molecules(_self, search_term, max_results=100):
        """
        Recherche intelligente dans les 1.4M molécules
        """
        if not _self._mega_loaded:
            compounds_df, _, status = _self.load_mega_dataset()
        else:
            compounds_df = _self._mega_data['compounds']
            status = "🟢 CONNECTÉ aux 1.4M molécules MEGA"
        
        if compounds_df.empty:
            return pd.DataFrame(), "🔴 Aucune donnée disponible"
        
        # Recherche case-insensitive dans les noms
        search_term_lower = search_term.lower()
        
        # Filtre principal sur le nom
        mask = compounds_df['name'].str.lower().str.contains(search_term_lower, na=False)
        results = compounds_df[mask].head(max_results)
        
        # Si peu de résultats, recherche élargie
        if len(results) < 10 and len(search_term) >= 3:
            # Recherche partielle plus permissive
            partial_mask = compounds_df['name'].str.lower().str.contains(
                search_term_lower[:3], na=False
            )
            additional_results = compounds_df[partial_mask & ~mask].head(max_results - len(results))
            results = pd.concat([results, additional_results])
        
        search_status = f"🔍 {len(results)} résultats pour '{search_term}'"
        return results, f"{status} | {search_status}"
    
    @st.cache_data(ttl=300)
    def get_random_molecules(_self, count=10):
        """
        Sélection aléatoire VRAIE dans les 1.4M molécules
        """
        if not _self._mega_loaded:
            compounds_df, _, status = _self.load_mega_dataset()
        else:
            compounds_df = _self._mega_data['compounds']
            status = "🟢 CONNECTÉ aux 1.4M molécules MEGA"
        
        if compounds_df.empty:
            return pd.DataFrame(), "🔴 Aucune donnée disponible"
        
        # Génération d'indices aléatoires SANS seed fixe
        max_index = len(compounds_df) - 1
        random_indices = random.sample(range(max_index), min(count, max_index))
        
        random_molecules = compounds_df.iloc[random_indices].copy()
        
        random_status = f"🎲 {len(random_molecules)} molécules aléatoires"
        return random_molecules, f"{status} | {random_status}"
    
    @st.cache_data(ttl=3600)
    def get_dataset_stats(_self):
        """
        Statistiques du dataset MEGA
        """
        if not _self._mega_loaded:
            compounds_df, bioactivities_df, status = _self.load_mega_dataset()
        else:
            compounds_df = _self._mega_data['compounds']
            bioactivities_df = _self._mega_data['bioactivities']
            status = "🟢 CONNECTÉ aux 1.4M molécules MEGA"
        
        if compounds_df.empty:
            return {}, "🔴 Données non disponibles"
        
        stats = {
            "total_molecules": len(compounds_df),
            "total_bioactivities": len(bioactivities_df),
            "avg_molecular_weight": compounds_df['molecular_weight'].mean() if 'molecular_weight' in compounds_df.columns else 0,
            "champion_molecules": len(compounds_df[compounds_df.get('is_champion', False) == True]) if 'is_champion' in compounds_df.columns else 0,
            "unique_targets": compounds_df['targets'].sum() if 'targets' in compounds_df.columns else 0,
            "high_bioactivity": len(compounds_df[compounds_df.get('bioactivity_score', 0) > 0.8]) if 'bioactivity_score' in compounds_df.columns else 0
        }
        
        return stats, status
    
    def create_mega_status_widget(self):
        """
        Widget d'état de connexion MEGA pour la sidebar
        """
        stats, status = self.get_dataset_stats()
        
        # Indicateur de statut principal
        if "🟢" in status:
            st.sidebar.success(f"🚀 MEGA DATASET CONNECTÉ")
            st.sidebar.metric("💊 Molécules disponibles", f"{stats.get('total_molecules', 0):,}")
            
            if stats.get('champion_molecules', 0) > 0:
                st.sidebar.metric("🏆 Molécules Champion", f"{stats['champion_molecules']:,}")
            
            if stats.get('high_bioactivity', 0) > 0:
                st.sidebar.metric("⚡ Haute bioactivité", f"{stats['high_bioactivity']:,}")
            
            st.sidebar.info("Dataset complet de 1.4M molécules actif")
            
        elif "🟡" in status:
            st.sidebar.warning("📊 Mode Échantillon")
            st.sidebar.metric("Molécules disponibles", f"{stats.get('total_molecules', 0):,}")
            st.sidebar.info("Échantillon représentatif actif")
            
        else:
            st.sidebar.error("❌ Données non disponibles")
    
    def create_mega_search_interface(self):
        """
        Interface de recherche optimisée pour le dataset MEGA
        """
        st.subheader("🔍 Recherche dans les 1.4M Molécules")
        
        # Recherche par terme
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_term = st.text_input(
                "Rechercher une molécule:",
                placeholder="Ex: curcumin, quercetin, resveratrol...",
                help="Recherche dans la base de 1.4M molécules phytothérapeutiques"
            )
        
        with col2:
            max_results = st.selectbox(
                "Résultats max:",
                [10, 25, 50, 100],
                index=1
            )
        
        # Recherche en temps réel
        if search_term and len(search_term) >= 2:
            with st.spinner("🔍 Recherche en cours dans les 1.4M molécules..."):
                results, search_status = self.search_molecules(search_term, max_results)
                
                st.info(search_status)
                
                if not results.empty:
                    # Affichage des résultats avec métriques
                    for idx, (_, molecule) in enumerate(results.iterrows()):
                        with st.expander(f"🧬 {molecule['name']}", expanded=(idx < 3)):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric(
                                    "Poids moléculaire", 
                                    f"{molecule.get('molecular_weight', 0):.1f} Da"
                                )
                                
                            with col2:
                                st.metric(
                                    "Score bioactivité", 
                                    f"{molecule.get('bioactivity_score', 0):.2f}"
                                )
                                
                            with col3:
                                st.metric(
                                    "Cibles", 
                                    molecule.get('targets', 0)
                                )
                            
                            # Indicateurs spéciaux
                            if molecule.get('is_champion', False):
                                st.success("🏆 Molécule Champion (MW > 670 Da)")
                            
                            if molecule.get('bioactivity_score', 0) > 0.85:
                                st.success("⚡ Bioactivité élevée")
                else:
                    st.warning(f"Aucun résultat trouvé pour '{search_term}'")
                    
                    # Suggestions automatiques
                    st.info("💡 Essayez: curcumin, quercetin, resveratrol, genistein, kaempferol")
    
    def create_random_discovery_widget(self):
        """
        Widget de découverte aléatoire de molécules
        """
        st.subheader("🎲 Découverte Aléatoire")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("🔄 Générer nouvelles molécules aléatoires", type="primary"):
                st.session_state.random_refresh = datetime.now()
        
        with col2:
            random_count = st.selectbox("Nombre:", [5, 10, 15, 20], index=1)
        
        # Génération de molécules aléatoires
        if st.button("🎯 Découvrir maintenant") or 'random_refresh' in st.session_state:
            with st.spinner("🎲 Sélection aléatoire dans les 1.4M molécules..."):
                random_molecules, random_status = self.get_random_molecules(random_count)
                
                st.info(random_status)
                
                if not random_molecules.empty:
                    # Affichage en grid
                    cols = st.columns(min(3, len(random_molecules)))
                    
                    for idx, (_, molecule) in enumerate(random_molecules.iterrows()):
                        with cols[idx % 3]:
                            st.markdown(f"""
                            <div style="border: 1px solid #ddd; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
                                <h4>🧬 {molecule['name']}</h4>
                                <p><strong>MW:</strong> {molecule.get('molecular_weight', 0):.1f} Da</p>
                                <p><strong>Score:</strong> {molecule.get('bioactivity_score', 0):.2f}</p>
                                <p><strong>Cibles:</strong> {molecule.get('targets', 0)}</p>
                            </div>
                            """, unsafe_allow_html=True)

# Instance globale du connecteur
mega_connector = MegaDatabaseConnector()

def render_mega_interface():
    """
    Interface principale pour le dataset MEGA
    """
    st.title("🚀 PhytoAI - Dataset MEGA 1.4M Molécules")
    
    # Widget de statut dans la sidebar
    mega_connector.create_mega_status_widget()
    
    # Tabs principales
    tab1, tab2, tab3 = st.tabs(["🔍 Recherche", "🎲 Découverte", "📊 Statistiques"])
    
    with tab1:
        mega_connector.create_mega_search_interface()
    
    with tab2:
        mega_connector.create_random_discovery_widget()
    
    with tab3:
        stats, status = mega_connector.get_dataset_stats()
        st.info(status)
        
        if stats:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Molécules", f"{stats['total_molecules']:,}")
                st.metric("Champion Molécules", f"{stats.get('champion_molecules', 0):,}")
            
            with col2:
                st.metric("Bioactivités", f"{stats['total_bioactivities']:,}")
                st.metric("Haute Bioactivité", f"{stats.get('high_bioactivity', 0):,}")
            
            with col3:
                st.metric("MW Moyen", f"{stats.get('avg_molecular_weight', 0):.1f} Da")
                st.metric("Total Cibles", f"{stats.get('unique_targets', 0):,}")

if __name__ == "__main__":
    render_mega_interface() 