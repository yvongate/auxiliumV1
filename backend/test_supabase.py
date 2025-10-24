#!/usr/bin/env python3
"""
Script pour tester l'upload Supabase
"""

import asyncio
from supabase_service import supabase_service

async def test_supabase_upload():
    """Teste l'upload vers Supabase"""
    print("Test d'upload Supabase")
    print("=" * 50)
    
    try:
        # Créer un fichier de test avec nom unique
        import time
        test_content = b"Test content for Supabase upload"
        test_filename = f"test_photo_{int(time.time())}.jpg"
        
        print(f"Upload du fichier: {test_filename}")
        photo_url = await supabase_service.upload_photo(test_content, test_filename)
        
        print("Upload reussi!")
        print(f"   URL: {photo_url}")
        
        # Tester l'accès à l'URL
        import requests
        try:
            response = requests.get(photo_url, timeout=10)
            if response.status_code == 200:
                print("Fichier accessible via URL publique")
                return True
            else:
                print(f"Fichier non accessible: {response.status_code}")
                return False
        except Exception as e:
            print(f"Erreur acces URL: {e}")
            return False
            
    except Exception as e:
        print(f"Erreur upload Supabase: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_supabase_upload())
    if success:
        print("\nSupabase fonctionne! Les images seront accessibles a Colab.")
    else:
        print("\nProbleme avec Supabase. Utilisation du fallback local.")