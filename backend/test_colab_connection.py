#!/usr/bin/env python3
"""
Script de test pour vérifier la connexion avec le serveur IA Colab
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement depuis config.env
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config.env")
load_dotenv(config_path)

def test_colab_connection():
    """Teste la connexion avec le serveur IA Colab"""
    
    # Récupérer l'URL Colab depuis l'environnement
    colab_url = os.getenv("COLAB_AI_URL")
    
    # ... reste du code inchangé
    
    # Récupérer l'URL Colab depuis l'environnement
    colab_url = os.getenv("COLAB_AI_URL")
    
    if not colab_url or colab_url == "https://your-ngrok-url.ngrok.io":
        print("❌ ERREUR: URL Colab non configurée!")
        print("📝 Configurez COLAB_AI_URL dans backend/config.env")
        print("🔗 Exemple: COLAB_AI_URL=https://abc123.ngrok.io")
        return False
    
    print(f"🔄 Test de connexion avec: {colab_url}")
    
    try:
        # Test de santé
        print("1️⃣ Test de santé du serveur...")
        health_response = requests.get(f"{colab_url}/", timeout=10)
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Serveur IA accessible!")
            print(f"   Modèle: {health_data.get('model', 'Inconnu')}")
            print(f"   Device: {health_data.get('device', 'Inconnu')}")
            print(f"   Status: {health_data.get('status', 'Inconnu')}")
        else:
            print(f"❌ Serveur répond avec code {health_response.status_code}")
            return False
        
        # Test d'analyse
        print("\n2️⃣ Test d'analyse IA...")
        test_data = {
            "image_url": "https://example.com/test.jpg",
            "transcription": "Test d'urgence - il y a un feu dans mon appartement",
            "session_id": 999
        }
        
        analyze_response = requests.post(
            f"{colab_url}/analyze",
            json=test_data,
            timeout=30
        )
        
        if analyze_response.status_code == 200:
            result = analyze_response.json()
            print(f"✅ Analyse IA fonctionnelle!")
            print(f"   Success: {result.get('success')}")
            if result.get('success'):
                ai_result = result.get('result', {})
                print(f"   Urgence pompiers: {ai_result.get('urgence_pompiers')}")
                print(f"   Niveau danger: {ai_result.get('niveau_danger')}")
                print(f"   Description: {ai_result.get('description', 'N/A')}")
            else:
                print(f"   Erreur: {result.get('error')}")
        else:
            print(f"❌ Erreur analyse: {analyze_response.status_code}")
            print(f"   Réponse: {analyze_response.text}")
            return False
        
        print(f"\n🎉 Tous les tests sont passés!")
        print(f"✅ Votre serveur IA Colab est prêt à être utilisé!")
        return True
        
    except requests.exceptions.Timeout:
        print("❌ Timeout: Le serveur IA met trop de temps à répondre")
        print("💡 Vérifiez que Colab est en cours d'exécution")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Erreur de connexion: Impossible de joindre le serveur")
        print("💡 Vérifiez:")
        print("   1. Colab notebook est en cours d'exécution")
        print("   2. URL Ngrok est correcte dans config.env")
        print("   3. Tunnel Ngrok est actif")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Test de connexion avec le serveur IA Colab")
    print("=" * 50)
    
    success = test_colab_connection()
    
    if success:
        print("\n✅ CONNEXION RÉUSSIE!")
        print("🚀 Votre backend peut maintenant utiliser l'IA Colab")
    else:
        print("\n❌ CONNEXION ÉCHOUÉE!")
        print("🔧 Vérifiez la configuration et réessayez")
        sys.exit(1)
