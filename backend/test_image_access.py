#!/usr/bin/env python3
"""
Script pour tester l'accès aux images depuis Colab
"""

import requests
from ia_client import analyze_emergency_with_ai

def test_image_access():
    """Teste l'accès aux images depuis Colab"""
    print("Test d'acces aux images depuis Colab")
    print("=" * 50)
    
    # Test avec une image publique accessible
    test_image_url = "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500"
    test_transcription = "Il y a un feu dans mon appartement avec beaucoup de fumée"
    
    print(f"Image de test: {test_image_url}")
    print(f"Transcription: {test_transcription}")
    print()
    
    # Test de l'analyse
    print("Envoi de l'analyse a Colab...")
    result = analyze_emergency_with_ai(
        image_url=test_image_url,
        transcription=test_transcription,
        session_id=999
    )
    
    print(f"\nResultat:")
    print(f"   Success: {result.get('success')}")
    
    if result.get('success'):
        ai_result = result.get('result', {})
        print(f"   Urgence pompiers: {ai_result.get('urgence_pompiers')}")
        print(f"   Niveau danger: {ai_result.get('niveau_danger')}")
        print(f"   Description: {ai_result.get('description', 'N/A')}")
        print(f"   Justification: {ai_result.get('justification', 'N/A')}")
    else:
        print(f"   Erreur: {result.get('error')}")
    
    return result.get('success', False)

if __name__ == "__main__":
    success = test_image_access()
    if success:
        print("\nTest reussi! Colab peut analyser les images.")
    else:
        print("\nTest echoue! Verifiez la connexion Colab.")
