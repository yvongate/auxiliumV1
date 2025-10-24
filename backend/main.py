from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional
from pyngrok import ngrok

from database import get_db, engine, Base
from models import *  # Importe tous les modèles
from schemas import UserCreate, UserResponse
from ia_client import analyze_emergency_with_ai, test_ia_connection
from supabase_service import supabase_service
from audio_transcription import audio_transcription_service

# Charger les variables d'environnement depuis config.env (même dossier)
load_dotenv(Path(__file__).with_name("config.env"))

# Créer les tables de la base de données
Base.metadata.create_all(bind=engine)

# Créer l'application FastAPI
app = FastAPI(
    title="Auxilium API",
    description="API Backend pour l'application Auxilium Mobile",
    version="1.0.0"
)

# Test connexion IA au démarrage
@app.on_event("startup")
async def startup_event():
    print("Test connexion serveur IA...")
    if test_ia_connection():
        print("Serveur IA pret!")
    else:
        print("Serveur IA non disponible. Les analyses IA ne fonctionneront pas.")
    
    # Configuration ngrok pour exposer le backend
    try:
        ngrok_token = os.getenv("NGROK_AUTH_TOKEN")
        if ngrok_token:
            ngrok.set_auth_token(ngrok_token)
            public_url = ngrok.connect(8002)
            # Stocker l'URL ngrok dans une variable d'environnement
            os.environ["NGROK_PUBLIC_URL"] = str(public_url)
            print(f"Backend expose via ngrok: {public_url}")
            print(f"URL publique pour Colab: {public_url}")
        else:
            print("Token ngrok non configure")
    except Exception as e:
        print(f"Erreur configuration ngrok: {e}")

# Configuration CORS pour permettre les requêtes depuis votre app React Native
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:19006", 
        "exp://192.168.1.100:8081",
        "exp://localhost:8081",
        "exp://localhost:8082",
        # Ajoutez d'autres origines si nécessaire
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Créer le dossier uploads s'il n'existe pas
os.makedirs("uploads", exist_ok=True)

# Servir les fichiers statiques
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Route de test
@app.get("/")
async def root():
    return {"message": "API Auxilium est en marche !"}

# Route de test de la base de données
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Test simple de connexion à la base de données
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# Route pour tester la connexion Supabase
@app.get("/test-db")
async def test_database(db: Session = Depends(get_db)):
    try:
        result = db.execute("SELECT version()")
        version = result.fetchone()[0]
        return {"message": "Connexion Supabase réussie !", "postgres_version": version}
    except Exception as e:
        return {"error": f"Erreur de connexion: {str(e)}"}

# Routes pour tester les modèles
@app.get("/models/info")
async def models_info():
    """Informations sur les modèles disponibles"""
    return {
        "models": [
            "User", "Operator", "EmergencySession", 
            "SessionUpdate", "Location", "AILog", "Call"
        ],
        "session_statuses": [status.value for status in SessionStatus],
        "description": "Modèles de données pour l'application d'urgence"
    }

@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    """Récupérer tous les utilisateurs"""
    try:
        users = db.query(User).all()
        return {"users": [{"id": u.id, "device_id": u.device_id, "verified": u.verified} for u in users]}
    except Exception as e:
        return {"error": f"Erreur lors de la récupération des utilisateurs: {str(e)}"}

@app.get("/operators")
async def get_operators(db: Session = Depends(get_db)):
    """Récupérer tous les opérateurs"""
    try:
        operators = db.query(Operator).all()
        return {"operators": [{"id": o.id, "name": o.name, "email": o.email, "role": o.role} for o in operators]}
    except Exception as e:
        return {"error": f"Erreur lors de la récupération des opérateurs: {str(e)}"}

@app.get("/emergency-sessions")
async def get_emergency_sessions(db: Session = Depends(get_db)):
    """Récupérer toutes les sessions d'urgence"""
    try:
        sessions = db.query(EmergencySession).all()
        return {"sessions": [{"id": s.id, "status": s.status.value if s.status else None, "created_at": s.created_at} for s in sessions]}
    except Exception as e:
        return {"error": f"Erreur lors de la récupération des sessions: {str(e)}"}

# Routes pour la gestion des utilisateurs
@app.post("/users", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Créer un nouvel utilisateur"""
    try:
        # Vérifier si l'utilisateur existe déjà
        existing_user = db.query(User).filter(User.device_id == user_data.device_id).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Un utilisateur avec ce device_id existe déjà")
        
        # Créer le nouvel utilisateur
        db_user = User(
            device_id=user_data.device_id,
            card_recto_url=user_data.card_recto_url,
            card_verso_url=user_data.card_verso_url,
            verified=user_data.verified
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
        
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erreur d'intégrité: device_id doit être unique")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création de l'utilisateur: {str(e)}")

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Récupérer un utilisateur par son ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

@app.get("/users/device/{device_id}", response_model=UserResponse)
async def get_user_by_device_id(device_id: str, db: Session = Depends(get_db)):
    """Récupérer un utilisateur par son device_id"""
    user = db.query(User).filter(User.device_id == device_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
    """Mettre à jour un utilisateur"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        # Mettre à jour les champs
        user.device_id = user_data.device_id
        user.card_recto_url = user_data.card_recto_url
        user.card_verso_url = user_data.card_verso_url
        user.verified = user_data.verified
        
        db.commit()
        db.refresh(user)
        
        return user
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════
# 🤖 ENDPOINTS IA - ANALYSE D'URGENCE
# ═══════════════════════════════════════════════════════════════════════════

@app.post("/emergency-sessions")
async def create_emergency_session(
    user_id: int = Form(...),
    photo: UploadFile = File(...),
    audio: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    db: Session = Depends(get_db)
):
    """
    Créer une session d'urgence et l'analyser avec l'IA Colab
    """
    try:
        # 1. Upload vers Supabase Storage
        # Lire le contenu des fichiers
        photo_content = await photo.read()
        audio_content = await audio.read()
        
        # Générer les noms de fichiers
        photo_filename = f"photo_{user_id}_{latitude}_{longitude}.jpg"
        audio_filename = f"audio_{user_id}_{latitude}_{longitude}.m4a"
        
        try:
            # Upload vers Supabase (priorité)
            photo_url = await supabase_service.upload_photo(photo_content, photo_filename)
            audio_url = await supabase_service.upload_audio(audio_content, audio_filename)
            
            print(f"Fichiers uploades vers Supabase:")
            print(f"   Photo: {photo_url}")
            print(f"   Audio: {audio_url}")
            
        except Exception as e:
            print(f"Erreur upload Supabase: {e}")
            # Fallback : sauvegarder localement et utiliser image de test
            import os
            os.makedirs("uploads", exist_ok=True)
            
            with open(f"uploads/{photo_filename}", "wb") as f:
                f.write(photo_content)
            with open(f"uploads/{audio_filename}", "wb") as f:
                f.write(audio_content)
            
            # Pour l'IA, utiliser l'image uploadée via une URL publique temporaire
            # Solution temporaire : utiliser une image de test accessible
            photo_url = "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500"
            audio_url = f"http://192.168.1.5:8002/uploads/{audio_filename}"
            
            print(f"Fallback vers sauvegarde locale:")
            print(f"   Photo (test): {photo_url}")
            print(f"   Audio: {audio_url}")
            print(f"   Photo locale sauvegardee: uploads/{photo_filename}")
        
        # 2. Transcrire l'audio avec Whisper
        print("Transcription de l'audio...")
        transcription = await audio_transcription_service.transcribe_audio(audio_content, audio_filename)
        print(f"Transcription: {transcription}")
        
        # 3. Créer la session en BDD
        session = EmergencySession(
            user_id=user_id,
            photo_url=photo_url,
            audio_url=audio_url,
            transcript=transcription,
            location_lat=latitude,
            location_lng=longitude,
            status=SessionStatus.en_attente
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        # 4. Envoyer à l'IA Colab pour analyse
        print(f"Analyse IA pour session {session.id}...")
        ai_result = analyze_emergency_with_ai(
            image_url=photo_url,
            transcription=transcription,
            session_id=session.id
        )
        
        # 5. Mettre à jour avec résultat IA
        if ai_result.get("success"):
            result = ai_result.get("result", {})
            session.ia_result = str(result)
            
            # Logique de priorisation basée sur l'IA
            if result.get("urgence_pompiers"):
                session.status = SessionStatus.a_affecter
                print(f"URGENCE DETECTEE: {result.get('description', 'Urgence non specifiee')}")
            else:
                session.status = SessionStatus.cloture
                session.ia_reason = result.get("justification", "Analyse IA: Non urgent")
                print(f"Non urgent: {result.get('justification', 'Aucune urgence detectee')}")
            
            db.commit()
        else:
            print(f"Erreur IA: {ai_result.get('error', 'Erreur inconnue')}")
            session.ia_reason = f"Erreur IA: {ai_result.get('error', 'Erreur inconnue')}"
            db.commit()
        
        return {
            "session_id": session.id,
            "status": session.status.value,
            "ai_result": ai_result,
            "message": "Session d'urgence créée et analysée"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur création session: {str(e)}")

@app.get("/emergency-sessions/{session_id}/ai-result")
async def get_ai_result(session_id: int, db: Session = Depends(get_db)):
    """
    Récupérer le résultat de l'analyse IA pour une session
    """
    session = db.query(EmergencySession).filter(EmergencySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    
    return {
        "session_id": session.id,
        "ai_result": session.ia_result,
        "ai_reason": session.ia_reason,
        "status": session.status.value
    }

@app.post("/emergency-sessions/{session_id}/analyze")
async def reanalyze_session(session_id: int, db: Session = Depends(get_db)):
    """
    Réanalyser une session existante avec l'IA
    """
    session = db.query(EmergencySession).filter(EmergencySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    
    # Réanalyser avec l'IA
    ai_result = analyze_emergency_with_ai(
        image_url=session.photo_url,
        transcription=session.transcript,
        session_id=session.id
    )
    
    if ai_result.get("success"):
        result = ai_result.get("result", {})
        session.ia_result = str(result)
        
        if result.get("urgence_pompiers"):
            session.status = SessionStatus.a_affecter
        else:
            session.status = SessionStatus.cloture
            session.ia_reason = result.get("justification", "Réanalyse IA: Non urgent")
        
        db.commit()
    
    return {
        "session_id": session.id,
        "ai_result": ai_result,
        "status": session.status.value
    }

@app.get("/ai/status")
async def get_ai_status():
    """
    Vérifier le statut de la connexion IA
    """
    is_connected = test_ia_connection()
    return {
        "ai_available": is_connected,
        "message": "Serveur IA connecté" if is_connected else "Serveur IA non disponible"
    }

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8002))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug
    )
