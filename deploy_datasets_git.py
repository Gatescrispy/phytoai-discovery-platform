#!/usr/bin/env python3
"""
Script de déploiement des datasets PhytoAI via Git
Copie les datasets essentiels et les prépare pour le déploiement
"""

import os
import shutil
import json
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Exécute une commande shell et retourne le résultat"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution de: {cmd}")
        print(f"Code d'erreur: {e.returncode}")
        print(f"Sortie d'erreur: {e.stderr}")
        return None

def copy_essential_datasets():
    """Copie les datasets essentiels vers le dépôt Git"""
    print("📁 Copie des datasets essentiels...")
    
    # Chemins source (relatifs au projet principal)
    source_base = Path("../phytotherapy-ai-discovery/phytoai/data/processed")
    mega_dataset_path = source_base / "MEGA_FINAL_DATASET_20250602_135508.json"
    
    # Dossier de destination
    dest_dir = Path("./datasets")
    dest_dir.mkdir(exist_ok=True)
    
    # Copier le dataset MEGA principal
    if mega_dataset_path.exists():
        dest_mega = dest_dir / "mega_final_dataset.json"
        shutil.copy2(mega_dataset_path, dest_mega)
        print(f"✅ Dataset MEGA copié: {dest_mega}")
        
        # Vérifier la taille du fichier
        size_mb = dest_mega.stat().st_size / (1024 * 1024)
        print(f"📊 Taille du dataset: {size_mb:.2f} MB")
        
        if size_mb > 100:
            print("⚠️  ATTENTION: Le fichier est volumineux pour Git!")
            print("💡 Considérez Git LFS ou un dataset réduit")
    else:
        print(f"❌ Dataset MEGA non trouvé: {mega_dataset_path}")
    
    # Copier les autres datasets
    other_datasets = [
        ("../mega_streamlit_50k.csv", "mega_streamlit_50k.csv"),
        ("./real_compounds_dataset.csv", "real_compounds_dataset.csv"),
        ("./real_bioactivities_dataset.csv", "real_bioactivities_dataset.csv")
    ]
    
    for src, dst in other_datasets:
        src_path = Path(src)
        if src_path.exists():
            dest_path = dest_dir / dst
            shutil.copy2(src_path, dest_path)
            size_mb = dest_path.stat().st_size / (1024 * 1024)
            print(f"✅ Dataset copié: {dst} ({size_mb:.2f} MB)")
        else:
            print(f"⚠️  Dataset non trouvé: {src}")

def create_dataset_summary():
    """Crée un fichier de résumé des datasets"""
    print("📝 Création du résumé des datasets...")
    
    datasets_dir = Path("./datasets")
    summary = {
        "timestamp": "2025-01-06",
        "description": "Datasets PhytoAI pour déploiement",
        "files": []
    }
    
    if datasets_dir.exists():
        for file_path in datasets_dir.glob("*"):
            if file_path.is_file():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                file_info = {
                    "name": file_path.name,
                    "size_mb": round(size_mb, 2),
                    "description": get_dataset_description(file_path.name)
                }
                summary["files"].append(file_info)
    
    summary_path = datasets_dir / "datasets_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Résumé créé: {summary_path}")
    return summary

def get_dataset_description(filename):
    """Retourne une description du dataset basée sur son nom"""
    descriptions = {
        "mega_final_dataset.json": "Dataset principal MEGA avec 352 composés et 1314 bioactivités",
        "mega_streamlit_50k.csv": "Dataset optimisé pour Streamlit (50k entrées)",
        "real_compounds_dataset.csv": "Composés réels avec propriétés moléculaires",
        "real_bioactivities_dataset.csv": "Bioactivités réelles et références"
    }
    return descriptions.get(filename, "Dataset PhytoAI")

def setup_git_lfs():
    """Configure Git LFS pour les gros fichiers"""
    print("🔧 Configuration de Git LFS...")
    
    # Vérifier si Git LFS est installé
    lfs_check = run_command("git lfs version")
    if lfs_check is None:
        print("⚠️  Git LFS n'est pas installé")
        print("💡 Installez avec: brew install git-lfs (macOS)")
        return False
    
    # Initialiser Git LFS
    run_command("git lfs install")
    
    # Tracker les fichiers volumineux
    lfs_patterns = [
        "*.json",
        "*.csv",
        "datasets/*"
    ]
    
    for pattern in lfs_patterns:
        run_command(f"git lfs track '{pattern}'")
        print(f"📎 Git LFS tracking: {pattern}")
    
    return True

def git_commit_and_push():
    """Commit et push les datasets vers Git"""
    print("🚀 Déploiement Git des datasets...")
    
    # Ajouter les fichiers
    run_command("git add datasets/")
    run_command("git add .gitattributes")
    
    # Vérifier le statut
    status = run_command("git status --porcelain")
    if not status:
        print("ℹ️  Aucun changement à commiter")
        return
    
    # Commit
    commit_msg = "Deploy PhytoAI datasets and models for production"
    result = run_command(f'git commit -m "{commit_msg}"')
    if result is None:
        print("❌ Erreur lors du commit")
        return
    
    print(f"✅ Commit créé: {commit_msg}")
    
    # Push
    push_result = run_command("git push origin main")
    if push_result is None:
        print("❌ Erreur lors du push")
        return
    
    print("✅ Push réussi vers origin/main")

def create_huggingface_upload_script():
    """Crée un script pour uploader vers Hugging Face"""
    script_content = '''#!/usr/bin/env python3
"""
Script d'upload des datasets PhytoAI vers Hugging Face
"""

from huggingface_hub import HfApi, upload_file
import os
from pathlib import Path

def upload_to_hf():
    """Upload les datasets vers Hugging Face"""
    api = HfApi()
    
    # Configuration
    repo_id = "cedrictantcheu/phytoai-datasets"
    token = os.getenv("HF_TOKEN")
    
    if not token:
        print("❌ Token Hugging Face manquant")
        print("💡 Définissez HF_TOKEN dans vos variables d'environnement")
        return
    
    datasets_dir = Path("./datasets")
    
    for file_path in datasets_dir.glob("*"):
        if file_path.is_file():
            print(f"📤 Upload: {file_path.name}")
            
            upload_file(
                path_or_fileobj=str(file_path),
                path_in_repo=file_path.name,
                repo_id=repo_id,
                token=token,
                repo_type="dataset"
            )
            
            print(f"✅ Uploadé: {file_path.name}")

if __name__ == "__main__":
    upload_to_hf()
'''
    
    script_path = Path("upload_datasets_hf.py")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # Rendre exécutable
    os.chmod(script_path, 0o755)
    print(f"✅ Script HF créé: {script_path}")

def main():
    """Fonction principale"""
    print("🚀 Déploiement des datasets PhytoAI via Git")
    print("=" * 50)
    
    # Étape 1: Copier les datasets
    copy_essential_datasets()
    
    # Étape 2: Créer le résumé
    summary = create_dataset_summary()
    print(f"📊 Datasets trouvés: {len(summary['files'])}")
    
    # Étape 3: Configurer Git LFS
    lfs_success = setup_git_lfs()
    
    # Étape 4: Créer le script Hugging Face
    create_huggingface_upload_script()
    
    # Étape 5: Git commit et push
    print("\n🤔 Voulez-vous commiter et pusher maintenant? (y/n)")
    choice = input().lower().strip()
    
    if choice in ['y', 'yes', 'oui']:
        git_commit_and_push()
        print("\n✅ Déploiement terminé!")
        print("🌐 Prochaine étape: Configurez votre dépôt sur GitHub/GitLab")
    else:
        print("\n⏸️  Déploiement Git reporté")
        print("💡 Lancez manuellement: git add datasets/ && git commit -m 'Deploy datasets'")
    
    print("\n📋 Résumé des fichiers:")
    for file_info in summary['files']:
        print(f"  • {file_info['name']} ({file_info['size_mb']} MB)")

if __name__ == "__main__":
    main() 