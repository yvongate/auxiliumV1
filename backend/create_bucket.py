"""
Script pour créer le bucket Supabase Storage
"""
import os
from dotenv import load_dotenv
from pathlib import Path
from supabase import create_client

# Charger les variables d'environnement
load_dotenv(Path(__file__).with_name("config.env"))

def create_emergencies_bucket():
    """Créer le bucket emergencies dans Supabase Storage"""
    try:
        url = os.getenv("SUPABASE_URL")
        service_key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not url or not service_key:
            print("Configuration Supabase manquante")
            return False
        
        # Créer le client
        supabase = create_client(url, service_key)
        
        # Créer le bucket
        try:
            result = supabase.storage.create_bucket(
                "emergencies",
                options={
                    "public": True,
                    "file_size_limit": 50 * 1024 * 1024,  # 50MB
                    "allowed_mime_types": ["image/*", "audio/*"]
                }
            )
            print("Bucket 'emergencies' cree avec succes!")
            return True
        except Exception as e:
            if "already exists" in str(e).lower():
                print("Bucket 'emergencies' existe deja!")
                return True
            else:
                print(f"Erreur creation bucket: {e}")
                return False
                
    except Exception as e:
        print(f"Erreur configuration: {e}")
        return False

if __name__ == "__main__":
    create_emergencies_bucket()
