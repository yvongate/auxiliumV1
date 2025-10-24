#!/usr/bin/env python3
"""
Script pour obtenir l'URL ngrok du backend
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from pyngrok import ngrok

# Charger les variables d'environnement
load_dotenv(Path(__file__).with_name("config.env"))

def get_ngrok_url():
    """Obtenir l'URL ngrok du backend"""
    try:
        ngrok_token = os.getenv("NGROK_AUTH_TOKEN")
        if ngrok_token:
            ngrok.set_auth_token(ngrok_token)
            
            # Lister les tunnels existants
            tunnels = ngrok.get_tunnels()
            for tunnel in tunnels:
                if tunnel.public_url and ":8001" in tunnel.config.get("addr", ""):
                    return tunnel.public_url
            
            # Si aucun tunnel trouvé, en créer un nouveau sur un port différent
            public_url = ngrok.connect(8002)
            return str(public_url)
        else:
            print("Token ngrok non configuré")
            return None
            
    except Exception as e:
        print(f"Erreur: {e}")
        return None

if __name__ == "__main__":
    url = get_ngrok_url()
    if url:
        print(f"URL ngrok: {url}")
        print(f"Test: {url}/health")
    else:
        print("Impossible d'obtenir l'URL ngrok")
