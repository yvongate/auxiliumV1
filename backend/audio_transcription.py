"""
Service de transcription audio avec Whisper
"""
import whisper
import tempfile
import os
from typing import Optional

class AudioTranscriptionService:
    def __init__(self):
        # Charger le modèle Whisper (base pour un bon compromis vitesse/qualité)
        print("Chargement du modele Whisper...")
        self.model = whisper.load_model("base")
        print("Modele Whisper charge!")
    
    async def transcribe_audio(self, audio_content: bytes, filename: str = "audio.m4a") -> str:
        """
        Transcrit un fichier audio en texte
        
        Args:
            audio_content: Contenu binaire du fichier audio
            filename: Nom du fichier (pour l'extension)
            
        Returns:
            str: Texte transcrit
        """
        try:
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{filename.split('.')[-1]}") as temp_file:
                temp_file.write(audio_content)
                temp_path = temp_file.name
            
            try:
                # Transcrire avec Whisper
                print(f"Transcription de l'audio: {filename}")
                result = self.model.transcribe(temp_path, language="fr")
                transcription = result["text"].strip()
                
                print(f"Transcription reussie: {transcription[:100]}...")
                return transcription
                
            finally:
                # Nettoyer le fichier temporaire
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            print(f"Erreur transcription: {e}")
            # Retourner une transcription par défaut en cas d'erreur
            return "Erreur de transcription audio - contenu non disponible"

# Instance globale
audio_transcription_service = AudioTranscriptionService()
