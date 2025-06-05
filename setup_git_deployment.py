#!/usr/bin/env python3
"""
Configuration Git pour le déploiement des datasets PhytoAI
Script simplifié pour préparer le déploiement
"""

import os
import subprocess
import sys
from pathlib import Path

def run_cmd(cmd):
    """Exécute une commande et affiche le résultat"""
    print(f"🔧 Exécution: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Succès: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Erreur: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def check_git_status():
    """Vérifie le statut Git actuel"""
    print("🔍 Vérification du statut Git...")
    
    if not Path(".git").exists():
        print("❌ Pas de dépôt Git trouvé!")
        return False
    
    run_cmd("git status")
    run_cmd("git remote -v")
    return True

def check_git_lfs():
    """Vérifie si Git LFS est disponible"""
    print("🔍 Vérification de Git LFS...")
    return run_cmd("git lfs version")

def list_large_files():
    """Liste les fichiers volumineux du projet"""
    print("📊 Analyse des fichiers volumineux...")
    
    large_files = []
    
    # Chercher les fichiers > 10MB
    for file_path in Path(".").rglob("*"):
        if file_path.is_file() and not file_path.is_symlink():
            try:
                size_mb = file_path.stat().st_size / (1024 * 1024)
                if size_mb > 10:
                    large_files.append((str(file_path), size_mb))
            except (OSError, PermissionError):
                continue
    
    if large_files:
        print("⚠️  Fichiers volumineux détectés (>10MB):")
        for file_path, size_mb in sorted(large_files, key=lambda x: x[1], reverse=True):
            print(f"  • {file_path}: {size_mb:.1f} MB")
        
        print("\n💡 Options pour les gros fichiers:")
        print("  1. Utiliser Git LFS (recommandé)")
        print("  2. Les exclure avec .gitignore")
        print("  3. Les déplacer vers un service cloud")
    else:
        print("✅ Aucun fichier volumineux détecté")
    
    return large_files

def setup_git_lfs_for_datasets():
    """Configure Git LFS pour les datasets"""
    print("🔧 Configuration de Git LFS pour les datasets...")
    
    if not check_git_lfs():
        print("📦 Installation de Git LFS nécessaire:")
        print("  macOS: brew install git-lfs")
        print("  Ubuntu: sudo apt install git-lfs")
        print("  Windows: Télécharger depuis git-lfs.github.io")
        return False
    
    # Initialiser Git LFS
    run_cmd("git lfs install")
    
    # Configurer le tracking pour les fichiers de données
    lfs_patterns = [
        "*.csv",
        "*.json", 
        "*.pkl",
        "*.model",
        "datasets/*"
    ]
    
    for pattern in lfs_patterns:
        if run_cmd(f"git lfs track '{pattern}'"):
            print(f"📎 Git LFS trackera: {pattern}")
    
    # Ajouter .gitattributes
    run_cmd("git add .gitattributes")
    
    return True

def suggest_deployment_strategy():
    """Suggère une stratégie de déploiement"""
    print("\n🚀 Stratégies de déploiement recommandées:")
    print("=" * 50)
    
    print("1. 🌐 GITHUB + GIT LFS (Recommandé)")
    print("   • Gratuit jusqu'à 1GB LFS")
    print("   • Intégration CI/CD native")
    print("   • Visibilité publique")
    
    print("\n2. 🤗 HUGGING FACE DATASETS")
    print("   • Spécialisé pour ML datasets")
    print("   • Datasets discovery native")
    print("   • API intégrée")
    
    print("\n3. 🦋 GITLAB + GIT LFS")
    print("   • 10GB LFS gratuit")
    print("   • Repos privés illimités")
    print("   • CI/CD intégré")
    
    print("\n4. ☁️  CLOUD STORAGE + GIT")
    print("   • Code sur Git, data sur cloud")
    print("   • URLs de téléchargement")
    print("   • Scalabilité maximale")

def interactive_setup():
    """Configuration interactive"""
    print("🎯 Configuration interactive du déploiement")
    print("=" * 45)
    
    # Vérifier Git
    if not check_git_status():
        print("⚠️  Veuillez d'abord initialiser un dépôt Git")
        return
    
    # Analyser les fichiers
    large_files = list_large_files()
    
    # Suggérer les stratégies
    suggest_deployment_strategy()
    
    # Choix utilisateur
    print("\n🤔 Que voulez-vous faire?")
    print("1. Configurer Git LFS pour les gros fichiers")
    print("2. Voir les commandes Git pour commiter")
    print("3. Créer un script de déploiement Hugging Face")
    print("4. Afficher l'aide pour GitHub")
    print("5. Quitter")
    
    try:
        choice = input("\nChoix (1-5): ").strip()
        
        if choice == "1":
            setup_git_lfs_for_datasets()
        elif choice == "2":
            show_git_commands()
        elif choice == "3":
            create_hf_script()
        elif choice == "4":
            show_github_help()
        elif choice == "5":
            print("👋 Au revoir!")
        else:
            print("❌ Choix invalide")
            
    except KeyboardInterrupt:
        print("\n👋 Annulé par l'utilisateur")

def show_git_commands():
    """Affiche les commandes Git recommandées"""
    print("\n📋 Commandes Git pour déployer:")
    print("=" * 35)
    
    commands = [
        "git add .",
        "git commit -m 'Deploy PhytoAI datasets and models'",
        "git push origin main"
    ]
    
    for cmd in commands:
        print(f"  {cmd}")
    
    print("\n💡 Si vous avez configuré Git LFS:")
    print("  git lfs ls-files  # Voir les fichiers LFS")
    print("  git lfs push origin main  # Push LFS files")

def create_hf_script():
    """Crée un script Hugging Face basique"""
    script_content = '''#!/usr/bin/env python3
"""Script de déploiement Hugging Face pour PhytoAI"""

import os
from pathlib import Path

def check_hf_setup():
    """Vérifie la configuration Hugging Face"""
    try:
        from huggingface_hub import HfApi
        token = os.getenv("HF_TOKEN")
        
        if not token:
            print("❌ Token HF manquant")
            print("💡 Obtenez votre token: https://huggingface.co/settings/tokens")
            print("💡 Exportez-le: export HF_TOKEN=your_token")
            return False
        
        api = HfApi()
        user = api.whoami(token=token)
        print(f"✅ Connecté comme: {user['name']}")
        return True
        
    except ImportError:
        print("❌ huggingface_hub non installé")
        print("💡 Installez: pip install huggingface_hub")
        return False

if __name__ == "__main__":
    check_hf_setup()
'''
    
    script_path = Path("check_hf_setup.py")
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    print(f"✅ Script créé: {script_path}")

def show_github_help():
    """Affiche l'aide pour GitHub"""
    print("\n🐙 Guide GitHub:")
    print("=" * 20)
    print("1. Créez un repo sur github.com")
    print("2. Ajoutez le remote:")
    print("   git remote add origin https://github.com/USERNAME/REPO.git")
    print("3. Push initial:")
    print("   git push -u origin main")
    print("\n💡 Pour Git LFS sur GitHub:")
    print("   • Gratuit: 1GB stockage + 1GB bande passante")
    print("   • Payant: 50$/mois pour 50GB")

def main():
    """Fonction principale"""
    print("🚀 PhytoAI - Configuration Git pour déploiement")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        # Mode automatique
        check_git_status()
        list_large_files()
        setup_git_lfs_for_datasets()
        show_git_commands()
    else:
        # Mode interactif
        interactive_setup()

if __name__ == "__main__":
    main() 