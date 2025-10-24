#!/usr/bin/env python3
"""
Script pour tester l'upload d'une vraie image vers Supabase
"""

import asyncio
import requests
from supabase_service import supabase_service

async def test_real_image_upload():
    """Teste l'upload d'une vraie image vers Supabase"""
    print("Test d'upload d'une vraie image vers Supabase")
    print("=" * 50)
    
    try:
        # Télécharger une vraie image depuis internet
        print("Telechargement d'une vraie image...")
        image_response = requests.get("https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500")
        
        if image_response.status_code != 200:
            print(f"Erreur telechargement image: {image_response.status_code}")
            return False
        
        image_content = image_response.content
        print(f"Image telechargee: {len(image_content)} bytes")
        
        # Upload vers Supabase
        import time
        filename = f"real_image_{int(time.time())}.jpg"
        print(f"Upload vers Supabase: {filename}")
        
        photo_url = await supabase_service.upload_photo(image_content, filename)
        
        print(f"Upload reussi!")
        print(f"URL: {photo_url}")
        
        # Tester l'accès à l'URL
        print("Test d'acces a l'URL...")
        url_response = requests.get(photo_url, timeout=10)
        
        if url_response.status_code == 200:
            print(f"Image accessible: {len(url_response.content)} bytes")
            if len(url_response.content) == len(image_content):
                print("✅ Image complete accessible!")
                return True
            else:
                print(f"❌ Image incomplete: {len(url_response.content)} vs {len(image_content)}")
                return False
        else:
            print(f"❌ Image non accessible: {url_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_real_image_upload())
    if success:
        print("\n✅ Supabase peut stocker des vraies images!")
    else:
        print("\n❌ Problème avec l'upload d'images vers Supabase.")
