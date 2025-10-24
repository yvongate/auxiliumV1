#!/usr/bin/env python3
"""
Script pour créer les tables dans la base de données Supabase
"""

from database import engine, Base
from models import *

def create_tables():
    """Créer toutes les tables dans la base de données"""
    try:
        print("Création des tables dans Supabase...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables créées avec succès !")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        return False

def drop_tables():
    """Supprimer toutes les tables (ATTENTION: supprime toutes les données)"""
    try:
        print("⚠️  Suppression de toutes les tables...")
        Base.metadata.drop_all(bind=engine)
        print("✅ Tables supprimées avec succès !")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la suppression des tables: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        drop_tables()
    else:
        create_tables()
