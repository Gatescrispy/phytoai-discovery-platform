#!/usr/bin/env python3
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
