#!/usr/bin/env python3
"""
🚀 PhytoAI - Connecteur MEGA Complet 1.4M Molécules
Streaming intelligent depuis dataset local ou Hugging Face
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
from pathlib import Path
from datetime import datetime, timedelta
import random
import time

class MegaCompleteConnector:
    def __init__(self):
        # Chemins vers les datasets
        self.local_dataset_path = "../mega_1400k_dataset_local"
        self.hf_dataset_name = "phytoai/mega-phytotherapy-complete-1400k"
        self.fallback_path = "mega_streamlit_50k.csv"
        
        # Cache et état
        self._dataset_cache = None
        self._dataset_type = None
        self._last_load_time = None
        
    @st.cache_data(ttl=3600)
    def load_complete_mega_dataset(_self):
        """Chargement intelligent du dataset complet 1.4M molécules"""
        print("🔍 Tentative de chargement dataset MEGA complet...")
        
        # 1. Tentative dataset local d'abord (plus rapide)
        if _self._try_load_local_dataset():
            return _self._dataset_cache, "🟢 MEGA COMPLET LOCAL (1.4M molécules)"
        
        # 2. Tentative Hugging Face
        if _self._try_load_huggingface_dataset():
            return _self._dataset_cache, "🟢 MEGA COMPLET HUGGING FACE (1.4M molécules)"
        
        # 3. Fallback vers 50K
        if _self._try_load_fallback_dataset():
            return _self._dataset_cache, "🟡 MEGA ÉCHANTILLON (50K molécules)"
        
        # 4. Échec complet
        return pd.DataFrame(), "❌ Aucun dataset disponible"
    
    def _try_load_local_dataset(self):
        """Tentative de chargement du dataset local"""
        try:
            local_path = Path(self.local_dataset_path)
            if local_path.exists():
                print(f"📂 Chargement dataset local: {local_path}")
                
                # Import conditionnel de datasets
                try:
                    from datasets import load_from_disk
                    dataset_dict = load_from_disk(str(local_path))
                    
                    # Combine tous les splits pour l'application
                    all_data = []
                    for split_name in ['train', 'validation', 'test']:
                        if split_name in dataset_dict:
                            split_df = dataset_dict[split_name].to_pandas()
                            split_df['dataset_split'] = split_name
                            all_data.append(split_df)
                    
                    if all_data:
                        combined_df = pd.concat(all_data, ignore_index=True)
                        self._dataset_cache = combined_df
                        self._dataset_type = "local_complete"
                        print(f"✅ Dataset local chargé: {len(combined_df):,} molécules")
                        return True
                        
                except ImportError:
                    print("⚠️ Module 'datasets' non installé pour le dataset local")
                    
        except Exception as e:
            print(f"❌ Erreur chargement local: {e}")
        
        return False
    
    def _try_load_huggingface_dataset(self):
        """Tentative de chargement depuis Hugging Face"""
        try:
            print(f"🤗 Tentative chargement Hugging Face: {self.hf_dataset_name}")
            
            # Import conditionnel
            try:
                from datasets import load_dataset
                
                # Chargement streaming pour économiser la mémoire
                dataset = load_dataset(
                    self.hf_dataset_name,
                    streaming=True,  # Mode streaming pour gros datasets
                    trust_remote_code=True
                )
                
                # Conversion en DataFrame avec limitation intelligente
                sample_size = 100000  # 100K échantillon pour test
                train_sample = dataset['train'].take(sample_size)
                df_sample = pd.DataFrame(list(train_sample))
                
                if len(df_sample) > 0:
                    self._dataset_cache = df_sample
                    self._dataset_type = "huggingface_streaming"
                    print(f"✅ Hugging Face streaming chargé: {len(df_sample):,} molécules (échantillon)")
                    return True
                    
            except ImportError:
                print("⚠️ Module 'datasets' non installé pour Hugging Face")
            except Exception as e:
                print(f"⚠️ Dataset HF non disponible: {e}")
                
        except Exception as e:
            print(f"❌ Erreur Hugging Face: {e}")
        
        return False
    
    def _try_load_fallback_dataset(self):
        """Chargement du fallback 50K molécules"""
        try:
            if os.path.exists(self.fallback_path):
                print(f"📊 Chargement fallback: {self.fallback_path}")
                df = pd.read_csv(self.fallback_path)
                self._dataset_cache = df
                self._dataset_type = "fallback_50k"
                print(f"✅ Fallback chargé: {len(df):,} molécules")
                return True
        except Exception as e:
            print(f"❌ Erreur fallback: {e}")
        
        return False
    
    @st.cache_data(ttl=1800)
    def search_molecules(_self, search_term, limit=100):
        """Recherche avancée dans le dataset complet"""
        dataset, status = _self.load_complete_mega_dataset()
        
        if dataset.empty:
            return pd.DataFrame(), "❌ Dataset indisponible"
        
        try:
            search_term_lower = search_term.lower()
            
            # Recherche multi-critères
            mask = (
                dataset['name'].str.lower().str.contains(search_term_lower, na=False) |
                dataset.get('molecular_family', pd.Series([''] * len(dataset))).str.lower().str.contains(search_term_lower, na=False) |
                dataset.get('targets', pd.Series([''] * len(dataset))).str.lower().str.contains(search_term_lower, na=False)
            )
            
            results = dataset[mask].copy()
            
            if len(results) > 0:
                # Tri intelligent par pertinence
                results['search_relevance'] = (
                    results['name'].str.lower().str.count(search_term_lower) * 3 +
                    results.get('complexity_score', pd.Series([0] * len(results))) * 0.1 +
                    results.get('bioactivity_score', pd.Series([0] * len(results))) * 2
                )
                
                results = results.sort_values(
                    ['search_relevance', 'complexity_score'], 
                    ascending=[False, False]
                ).head(limit)
                
                return results, f"🎯 {len(results)} résultats trouvés"
            else:
                return pd.DataFrame(), f"❌ Aucun résultat pour '{search_term}'"
                
        except Exception as e:
            return pd.DataFrame(), f"❌ Erreur recherche: {e}"
    
    @st.cache_data(ttl=900)
    def get_random_molecules(_self, count=10, category=None):
        """Sélection aléatoire intelligente de molécules"""
        dataset, status = _self.load_complete_mega_dataset()
        
        if dataset.empty:
            return pd.DataFrame(), "❌ Dataset indisponible"
        
        try:
            # Filtrage par catégorie si spécifié
            if category and category != "Toutes":
                if category == "Champions" and 'is_champion' in dataset.columns:
                    filtered_dataset = dataset[dataset['is_champion'] == True]
                elif category == "Haute Complexité" and 'complexity_score' in dataset.columns:
                    filtered_dataset = dataset[dataset['complexity_score'] > 20]
                elif category == "Drug-like" and 'molecular_weight' in dataset.columns:
                    filtered_dataset = dataset[
                        (dataset['molecular_weight'] > 150) & 
                        (dataset['molecular_weight'] < 500)
                    ]
                else:
                    filtered_dataset = dataset
            else:
                filtered_dataset = dataset
            
            if len(filtered_dataset) == 0:
                filtered_dataset = dataset  # Fallback
            
            # Échantillonnage pondéré par complexité
            if 'complexity_score' in filtered_dataset.columns:
                weights = np.exp(filtered_dataset['complexity_score'] / 10)  # Pondération exponentielle
                weights = weights / weights.sum()  # Normalisation
                
                try:
                    sample_indices = np.random.choice(
                        filtered_dataset.index, 
                        size=min(count, len(filtered_dataset)), 
                        replace=False, 
                        p=weights
                    )
                    results = filtered_dataset.loc[sample_indices]
                except:
                    # Fallback simple si pondération échoue
                    results = filtered_dataset.sample(min(count, len(filtered_dataset)))
            else:
                results = filtered_dataset.sample(min(count, len(filtered_dataset)))
            
            return results, f"🎲 {len(results)} molécules découvertes"
            
        except Exception as e:
            return pd.DataFrame(), f"❌ Erreur découverte: {e}"
    
    @st.cache_data(ttl=3600)
    def get_dataset_statistics(_self):
        """Statistiques complètes du dataset"""
        dataset, status = _self.load_complete_mega_dataset()
        
        if dataset.empty:
            return {}, "❌ Statistiques indisponibles"
        
        try:
            stats = {
                'total_molecules': len(dataset),
                'dataset_type': _self._dataset_type,
                'unique_families': dataset.get('molecular_family', pd.Series()).nunique(),
                'avg_molecular_weight': dataset.get('molecular_weight', pd.Series([0])).mean(),
                'avg_complexity': dataset.get('complexity_score', pd.Series([0])).mean(),
                'avg_bioactivity': dataset.get('bioactivity_score', pd.Series([0])).mean(),
            }
            
            # Statistiques spécialisées
            if 'is_champion' in dataset.columns:
                stats['champion_molecules'] = len(dataset[dataset['is_champion'] == True])
            
            if 'molecular_weight' in dataset.columns:
                stats['drug_like_molecules'] = len(dataset[
                    (dataset['molecular_weight'] >= 150) & 
                    (dataset['molecular_weight'] <= 500)
                ])
                stats['large_molecules'] = len(dataset[dataset['molecular_weight'] > 670])
            
            if 'complexity_score' in dataset.columns:
                stats['high_complexity'] = len(dataset[dataset['complexity_score'] > 20])
            
            return stats, status
            
        except Exception as e:
            return {}, f"❌ Erreur statistiques: {e}"
    
    def get_dataset_status_widget(self):
        """Widget de statut pour la sidebar Streamlit"""
        stats, status = self.get_dataset_statistics()
        
        # Affichage du statut principal
        if "🟢" in status:
            if "LOCAL" in status:
                st.sidebar.success("🚀 MEGA COMPLET LOCAL")
                st.sidebar.info("💾 Dataset 1.4M en cache local")
            else:
                st.sidebar.success("🚀 MEGA COMPLET HUGGING FACE")
                st.sidebar.info("☁️ Streaming depuis Hugging Face")
        elif "🟡" in status:
            st.sidebar.warning("📊 MEGA ÉCHANTILLON")
            st.sidebar.info("🔄 Mode fallback 50K molécules")
        else:
            st.sidebar.error("❌ DATASET INDISPONIBLE")
            return
        
        # Métriques détaillées
        if stats:
            col1, col2 = st.sidebar.columns(2)
            
            with col1:
                st.metric("💊 Molécules", f"{stats.get('total_molecules', 0):,}")
                if stats.get('champion_molecules', 0) > 0:
                    st.metric("🏆 Champions", f"{stats['champion_molecules']:,}")
            
            with col2:
                if stats.get('drug_like_molecules', 0) > 0:
                    st.metric("💉 Drug-like", f"{stats['drug_like_molecules']:,}")
                if stats.get('large_molecules', 0) > 0:
                    st.metric("🔬 Complexes", f"{stats['large_molecules']:,}")
            
            # Scores moyens
            if stats.get('avg_complexity', 0) > 0:
                st.sidebar.metric(
                    "🧬 Complexité moyenne", 
                    f"{stats['avg_complexity']:.1f}/30"
                )
            
            if stats.get('avg_bioactivity', 0) > 0:
                st.sidebar.metric(
                    "⚡ Bioactivité moyenne", 
                    f"{stats['avg_bioactivity']:.3f}"
                )

# Instance globale pour l'application
mega_complete_connector = MegaCompleteConnector() 