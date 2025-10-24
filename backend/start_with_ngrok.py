#!/usr/bin/env python3
"""
Script pour démarrer le backend avec ngrok
"""

import os
import time
import subprocess
import threading
from dotenv import load_dotenv
from pathlib import Path
from pyngrok import ngrok

# Charger les variables d'environnement
load_dotenv(Path(__file__).with_name("config.env"))

def start_backend():
    """Démarrer le backend FastAPI"""
    print("Démarrage du backend FastAPI...")
    subprocess.run(["python", "start_api.py"])

def start_ngrok():
    """Démarrer ngrok et exposer le backend"""
    try:
        ngrok_token = os.getenv("NGROK_AUTH_TOKEN")
        if not ngrok_token:
            print("❌ Token ngrok non configuré")
            return None
        
        print("Configuration de ngrok...")
        ngrok.set_auth_token(ngrok_token)
        
        # Attendre que le backend démarre
        time.sleep(5)
        
        print("Création du tunnel ngrok...")
        public_url = ngrok.connect(8002)
        
        print(f"✅ Backend exposé via ngrok: {public_url}")
        print(f"📝 URL publique pour Colab: {public_url}")
        print(f"🔗 Test: {public_url}/health")
        
        return str(public_url)
        
    except Exception as e:
        print(f"❌ Erreur ngrok: {e}")
        return None

def main():
    """Fonction principale"""
    print("🚀 Démarrage du backend avec ngrok...")
    
    # Démarrer le backend en arrière-plan
    backend_thread = threading.Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Démarrer ngrok
    ngrok_url = start_ngrok()
    
    if ngrok_url:
        print(f"\n✅ Configuration terminée!")
        print(f"🌐 Backend accessible via: {ngrok_url}")
        print(f"📱 Frontend mobile: http://192.168.1.5:8002")
        print(f"🤖 Colab IA: https://unsage-ethyl-personably.ngrok-free.dev")
        print("\n⏸️  Appuyez sur Ctrl+C pour arrêter")
        
        try:
            # Garder le script actif
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Arrêt du serveur...")
            ngrok.disconnect(ngrok_url)
    else:
        print("❌ Échec de la configuration")

if __name__ == "__main__":
    main()
