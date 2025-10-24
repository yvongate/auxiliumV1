import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URL de connexion Supabase avec vos coordonnées
# Format: postgresql://postgres:[PASSWORD]@[PROJECT_REF].supabase.co:5432/postgres
SUPABASE_DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:auxiliumseralechangement1%40@db.vuknogfptlcilsthhdgj.supabase.co:5432/postgres"
)

# Créer l'engine SQLAlchemy
engine = create_engine(
    SUPABASE_DB_URL,
    echo=True,  # Mettre à False en production
    pool_pre_ping=True,  # Vérifie la connexion avant utilisation
    pool_size=10,
    max_overflow=20
)

# Créer la session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()

# Fonction helper pour obtenir une session
def get_db():
    """
    Générateur de session pour FastAPI dependency injection
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
