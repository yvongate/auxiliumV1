#!/usr/bin/env python3
"""
Test de configuration ngrok
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from pyngrok import ngrok

# Charger les variables d'environnement
load_dotenv(Path(__file__).with_name("config.env"))

def test_ngrok():
    """Test de la configuration ngrok"""
    try:
        ngrok_token = os.getenv("NGROK_AUTH_TOKEN")
        print(f"Token ngrok: {ngrok_token[:10]}..." if ngrok_token else "Token non trouvé")
        
        if ngrok_token:
            ngrok.set_auth_token(ngrok_token)
            print("Token ngrok configuré avec succès")
            
            # Créer un tunnel sur un port différent pour éviter le conflit
            public_url = ngrok.connect(8001)
            print(f"Tunnel créé: {public_url}")
            
            return str(public_url)
        else:
            print("Erreur: Token ngrok non configuré")
            return None
            
    except Exception as e:
        print(f"Erreur: {e}")
        return None

if __name__ == "__main__":
    url = test_ngrok()
    if url:
        print(f"\nURL publique: {url}")
        print("Copiez cette URL dans votre Colab pour tester la connexion")
    else:
        print("\nEchec de la configuration ngrok")
