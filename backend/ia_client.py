"""
Client pour communiquer avec le serveur IA dans Colab
À utiliser dans ton backend FastAPI (Cursor)
"""

import requests
import os
from typing import Dict, Optional
from dotenv import load_dotenv
from pathlib import Path

# Charger les variables d'environnement depuis config.env (même dossier que ce fichier)
load_dotenv(Path(__file__).with_name("config.env"))

# ═══════════════════════════════════════════════════════════════════════════
# 🔧 CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

# URL Ngrok de ton Colab (à mettre dans .env)
COLAB_AI_URL = os.getenv("COLAB_AI_URL", "https://abc123.ngrok.io")
TIMEOUT = 30  # Timeout en secondes

# ═══════════════════════════════════════════════════════════════════════════
# 🤖 FONCTION PRINCIPALE
# ═══════════════════════════════════════════════════════════════════════════

def analyze_emergency_with_ai(
    image_url: str,
    transcription: str,
    session_id: Optional[int] = None
) -> Dict:
    """
    Envoie une requête au serveur IA Colab pour analyser une urgence.
    
    Args:
        image_url: URL de l'image uploadée
        transcription: Texte transcrit de l'audio
        session_id: ID de la session d'urgence
    
    Returns:
        dict: Résultat de l'analyse IA
        
    Example:
        >>> result = analyze_emergency_with_ai(
        ...     "https://storage.../photo.jpg",
        ...     "Il y a un feu dans mon appartement",
        ...     session_id=123
        ... )
        >>> print(result["result"]["urgence_pompiers"])
        True
    """
    try:
        # Vérifier que le serveur IA est accessible
        health_check = requests.get(f"{COLAB_AI_URL}/", timeout=5)
        if health_check.status_code != 200:
            return {
                "success": False,
                "error": "Serveur IA inaccessible"
            }
        
        # Envoyer la requête d'analyse
        response = requests.post(
            f"{COLAB_AI_URL}/analyze",
            json={
                "image_url": image_url,
                "transcription": transcription,
                "session_id": session_id
            },
            timeout=TIMEOUT
        )
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Timeout: Le serveur IA met trop de temps à répondre"
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Erreur de connexion: Vérifiez que Colab est démarré et que l'URL Ngrok est correcte"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur inattendue: {str(e)}"
        }

# ═══════════════════════════════════════════════════════════════════════════
# 🧪 FONCTION DE TEST
# ═══════════════════════════════════════════════════════════════════════════

def test_ia_connection() -> bool:
    """
    Teste la connexion avec le serveur IA Colab.
    
    Returns:
        bool: True si connexion OK, False sinon
    """
    try:
        response = requests.get(f"{COLAB_AI_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"Serveur IA connecte!")
            print(f"   Modele: {data.get('model')}")
            print(f"   Device: {data.get('device')}")
            return True
        else:
            print(f"Serveur IA repond avec code {response.status_code}")
            return False
    except Exception as e:
        print(f"Impossible de se connecter au serveur IA: {e}")
        print(f"Verifiez:")
        print(f"   1. Colab notebook est en cours d'execution")
        print(f"   2. URL Ngrok dans .env est correcte: {COLAB_AI_URL}")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# 🧪 TEST MANUEL (si exécuté directement)
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🧪 Test du client IA...")
    
    # Test connexion
    if test_ia_connection():
        print("\n📝 Exemple d'analyse:")
        
        # Exemple avec image de test
        result = analyze_emergency_with_ai(
            image_url="https://example.com/fire.jpg",
            transcription="Il y a un feu dans mon appartement avec beaucoup de fumée",
            session_id=999
        )
        
        print(f"\nRésultat:")
        print(f"  Success: {result.get('success')}")
        if result.get('success'):
            print(f"  Urgence pompiers: {result['result'].get('urgence_pompiers')}")
            print(f"  Niveau danger: {result['result'].get('niveau_danger')}")
            print(f"  Description: {result['result'].get('description')}")
