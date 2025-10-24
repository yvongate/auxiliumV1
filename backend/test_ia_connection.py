#!/usr/bin/env python3
"""
Script pour tester la connexion avec le serveur IA Colab
"""

from ia_client import test_ia_connection, analyze_emergency_with_ai

def main():
    print("🧪 Test de connexion IA Colab")
    print("=" * 50)
    
    # Test connexion
    if test_ia_connection():
        print("\n📝 Test d'analyse d'urgence:")
        
        # Exemple d'analyse
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
        else:
            print(f"  Erreur: {result.get('error')}")
    else:
        print("\n❌ Impossible de se connecter au serveur IA")
        print("💡 Vérifiez:")
        print("   1. Colab notebook est en cours d'exécution")
        print("   2. URL Ngrok dans config.env est correcte")
        print("   3. Le serveur IA répond sur / et /analyze")

if __name__ == "__main__":
    main()
