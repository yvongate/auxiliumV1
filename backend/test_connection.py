#!/usr/bin/env python3
"""
Script pour tester la connexion à Supabase
"""

from database import engine, SessionLocal
from sqlalchemy import text

def test_connection():
    """Tester la connexion à la base de données"""
    try:
        print("🔍 Test de connexion à Supabase...")
        
        # Test avec l'engine
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Connexion réussie ! Version PostgreSQL: {version}")
            
        # Test avec une session
        db = SessionLocal()
        try:
            result = db.execute(text("SELECT current_database(), current_user"))
            db_info = result.fetchone()
            print(f"✅ Session active - Base: {db_info[0]}, Utilisateur: {db_info[1]}")
            return True
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_tables():
    """Tester l'existence des tables"""
    try:
        print("\n🔍 Test des tables...")
        db = SessionLocal()
        try:
            # Vérifier les tables
            result = db.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                print("✅ Tables trouvées:")
                for table in tables:
                    print(f"  - {table}")
            else:
                print("⚠️  Aucune table trouvée")
                
            return True
        finally:
            db.close()
    except Exception as e:
        print(f"❌ Erreur lors du test des tables: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Test de connexion Supabase pour Auxilium")
    print("=" * 50)
    
    if test_connection():
        test_tables()
    else:
        print("\n💡 Vérifiez vos coordonnées Supabase dans database.py")
