#!/usr/bin/env python3
"""
Script simple pour démarrer le backend avec ngrok
"""

import os
import uvicorn
from dotenv import load_dotenv
from pathlib import Path
from pyngrok import ngrok

# Charger les variables d'environnement
load_dotenv(Path(__file__).with_name("config.env"))

def main():
    """Démarrer le backend avec ngrok"""
    print("Demarrage du backend avec ngrok...")
    
    # Configuration ngrok
    ngrok_token = os.getenv("NGROK_AUTH_TOKEN")
    if ngrok_token:
        try:
            ngrok.set_auth_token(ngrok_token)
            # Utiliser un port différent pour éviter le conflit avec Colab
            public_url = ngrok.connect(8002, subdomain="auxilium-backend")
            os.environ["NGROK_PUBLIC_URL"] = str(public_url)
            print(f"Backend expose via ngrok: {public_url}")
            print(f"URL pour Colab: {public_url}")
        except Exception as e:
            print(f"Erreur ngrok: {e}")
            print("Tentative avec un port different...")
            try:
                # Essayer avec un port différent
                public_url = ngrok.connect(8003)
                os.environ["NGROK_PUBLIC_URL"] = str(public_url)
                print(f"Backend expose via ngrok (port 8003): {public_url}")
                print(f"URL pour Colab: {public_url}")
            except Exception as e2:
                print(f"Erreur ngrok port 8003: {e2}")
                return
    
    # Démarrer le backend
    print("Demarrage de l'API sur le port 8002...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()
