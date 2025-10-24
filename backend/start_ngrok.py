"""
Script pour démarrer ngrok et exposer le serveur local
"""
import subprocess
import time
import requests
import json

def start_ngrok(port=8000):
    """Démarrer ngrok pour exposer le port local"""
    try:
        print(f"🌐 Démarrage ngrok pour le port {port}...")
        
        # Démarrer ngrok
        process = subprocess.Popen(
            ["ngrok", "http", str(port), "--log=stdout"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Attendre que ngrok démarre
        time.sleep(3)
        
        # Récupérer l'URL publique
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            if response.status_code == 200:
                data = response.json()
                tunnels = data.get("tunnels", [])
                if tunnels:
                    public_url = tunnels[0]["public_url"]
                    print(f"✅ Ngrok démarré!")
                    print(f"🌐 URL publique: {public_url}")
                    print(f"📍 URL locale: http://localhost:{port}")
                    return public_url
        except:
            pass
        
        print("⚠️ Impossible de récupérer l'URL ngrok automatiquement")
        print("💡 Vérifiez manuellement sur http://localhost:4040")
        
        return None
        
    except FileNotFoundError:
        print("❌ Ngrok n'est pas installé ou pas dans le PATH")
        print("📥 Téléchargez ngrok depuis: https://ngrok.com/download")
        return None
    except Exception as e:
        print(f"❌ Erreur ngrok: {e}")
        return None

if __name__ == "__main__":
    start_ngrok()

