"""
Service Supabase pour l'upload de fichiers
"""
import os
from supabase import create_client, Client  
from dotenv import load_dotenv
from pathlib import Path

# Charger les variables d'environnement
load_dotenv(Path(__file__).with_name("config.env"))

class SupabaseService:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.service_key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not self.url or not self.service_key:
            raise ValueError("Configuration Supabase manquante")
        
        self.supabase: Client = create_client(self.url, self.service_key)
    
    async def upload_photo(self, file_content: bytes, filename: str) -> str:
        """Upload une photo vers Supabase Storage"""
        try:
            # Créer le bucket s'il n'existe pas
            try:
                self.supabase.storage.create_bucket("emergencies")
            except Exception:
                pass  # Le bucket existe déjà
            
            # Upload du fichier
            result = self.supabase.storage.from_("emergencies").upload(
                filename, 
                file_content,
                file_options={"content-type": "image/jpeg"}
            )
            
            # Vérifier le résultat (API Supabase v2)
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erreur upload photo: {result.error}")
            
            # Retourner l'URL publique
            return f"{self.url}/storage/v1/object/public/emergencies/{filename}"
            
        except Exception as e:
            print(f"Erreur upload photo: {e}")
            raise e
    
    async def upload_audio(self, file_content: bytes, filename: str) -> str:
        """Upload un audio vers Supabase Storage"""
        try:
            # Créer le bucket s'il n'existe pas
            try:
                self.supabase.storage.create_bucket("emergencies")
            except Exception:
                pass  # Le bucket existe déjà
            
            # Upload du fichier
            result = self.supabase.storage.from_("emergencies").upload(
                filename, 
                file_content,
                file_options={"content-type": "audio/m4a"}
            )
            
            # Vérifier le résultat (API Supabase v2)
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erreur upload audio: {result.error}")
            
            # Retourner l'URL publique
            return f"{self.url}/storage/v1/object/public/emergencies/{filename}"
            
        except Exception as e:
            print(f"Erreur upload audio: {e}")
            raise e

# Instance globale
supabase_service = SupabaseService()
