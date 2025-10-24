#!/usr/bin/env python3
"""
Script pour démarrer l'API Auxilium
"""

import uvicorn
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def start_api():
    """Démarrer l'API FastAPI"""
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8002))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    print("Demarrage de l'API Auxilium...")
    print(f"URL: http://{host}:{port}")
    print(f"Documentation: http://{host}:{port}/docs")
    print(f"Debug: {debug}")
    print("=" * 50)
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,  # Désactiver le reload pour éviter les redémarrages
        log_level="info"
    )

if __name__ == "__main__":
    start_api()
