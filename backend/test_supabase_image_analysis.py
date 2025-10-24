#!/usr/bin/env python3
"""
Script pour tester l'analyse IA avec la vraie image Supabase
"""

import requests
from ia_client import analyze_emergency_with_ai

def test_supabase_image_analysis():
    """Teste l'analyse IA avec la vraie image Supabase"""
    print("Test d'analyse IA avec vraie image Supabase")
    print("=" * 50)
    
    # Utiliser l'image qui vient d'être uploadée
    test_image_url = "https://vuknogfptlcilsthhdgj.supabase.co/storage/v1/object/public/emergencies/real_image_1761274423.jpg"
    test_transcription = "Il y a un feu dans mon appartement avec beaucoup de fumee"
    
    print(f"Image Supabase: {test_image_url}")
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
    success = test_supabase_image_analysis()
    if success:
        print("\n✅ Test reussi! Colab peut analyser les vraies images Supabase.")
    else:
        print("\n❌ Test echoue! Verifiez la connexion Colab.")
