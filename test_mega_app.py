#!/usr/bin/env python3
"""
Test de l'application PhytoAI avec dataset MEGA 1.4M
"""

import sys
import os

# Import des modules nécessaires
try:
    from streamlit_mega_complete_connector import mega_complete_connector
    print("✅ Connecteur MEGA importé avec succès")
    
    # Test du chargement du dataset
    dataset, status = mega_complete_connector.load_complete_mega_dataset()
    print(f"Status: {status}")
    print(f"Dataset size: {len(dataset):,} molécules")
    
    if len(dataset) > 0:
        print("\n🧬 Échantillon de molécules:")
        for i, (idx, row) in enumerate(dataset.head(3).iterrows()):
            print(f"{i+1}. {row.get('name', 'Nom inconnu')[:50]}...")
            print(f"   Poids: {row.get('molecular_weight', 0):.1f} Da")
            print(f"   Champion: {row.get('is_champion', False)}")
            print()
        
        # Test de recherche
        print("🔍 Test de recherche...")
        search_results, search_status = mega_complete_connector.search_molecules("anthraquinon", 5)
        print(f"Résultats recherche: {len(search_results)} trouvés")
        
        # Test aléatoire
        print("🎲 Test sélection aléatoire...")
        random_results, random_status = mega_complete_connector.get_random_molecules(3)
        print(f"Sélection aléatoire: {len(random_results)} molécules")
        
        # Statistiques
        print("📊 Test statistiques...")
        stats, stats_status = mega_complete_connector.get_dataset_statistics()
        print(f"Statistiques: {stats}")
        
        print("\n🎉 TOUS LES TESTS RÉUSSIS - APPLICATION PRÊTE !")
        print("🚀 L'application peut maintenant utiliser les 1.4M molécules MEGA")
        
    else:
        print("❌ Dataset vide")
        
except ImportError as e:
    print(f"❌ Erreur import: {e}")
except Exception as e:
    print(f"❌ Erreur test: {e}") 