#!/usr/bin/env python3
"""
Script pour tester l'accès aux fichiers uploadés via ngrok
"""

import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# Charger les variables d'environnement
load_dotenv(Path(__file__).with_name("config.env"))

def test_file_access():
    """Teste l'accès aux fichiers uploadés"""
    print("Test d'acces aux fichiers uploades")
    print("=" * 50)
    
    # URL ngrok du backend
    ngrok_url = os.getenv("NGROK_PUBLIC_URL")
    if not ngrok_url:
        print("❌ NGROK_PUBLIC_URL non defini")
        print("💡 Redemarrez le backend avec ngrok")
        return False
    
    print(f"URL ngrok backend: {ngrok_url}")
    
    # Test de santé du backend
    try:
        health_response = requests.get(f"{ngrok_url}/health", timeout=10)
        if health_response.status_code == 200:
            print("✅ Backend accessible via ngrok")
        else:
            print(f"❌ Backend répond avec code {health_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Impossible d'accéder au backend: {e}")
        return False
    
    # Test d'accès aux fichiers statiques
    test_file_url = f"{ngrok_url}/uploads/test.txt"
    try:
        # Créer un fichier de test
        os.makedirs("uploads", exist_ok=True)
        with open("uploads/test.txt", "w") as f:
            f.write("Test file for ngrok access")
        
        # Tester l'accès
        file_response = requests.get(test_file_url, timeout=10)
        if file_response.status_code == 200:
            print("✅ Fichiers statiques accessibles via ngrok")
            print(f"   Test URL: {test_file_url}")
            return True
        else:
            print(f"❌ Fichiers statiques non accessibles: {file_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur test fichiers: {e}")
        return False

if __name__ == "__main__":
    success = test_file_access()
    if success:
        print("\n✅ Test réussi! Colab peut accéder aux fichiers uploadés.")
    else:
        print("\n❌ Test échoué! Vérifiez la configuration ngrok.")
