import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.staticfiles import StaticFiles

# Ajouter le chemin pour les imports relatifs
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuration DATABASE_URL pour Render
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://portfolio_user:03trhKSbCvRNAgSzzSdIg7dsvjBJPh3S@dpg-d5hql7fpm1nc73ea5540-a.frankfurt-postgres.render.com:5432/portfolio_db_lc12"
)

# S'assurer que c'est postgresql:// et non postgres://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"🔗 Connexion à la base: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}")

# Créer l'engine SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app
app = FastAPI()

# Servir les fichiers statiques (uploads)
try:
    # Créer le dossier si nécessaire
    os.makedirs("static/uploads/screenshots", exist_ok=True)
    # Monter le dossier static
    app.mount("/uploads", StaticFiles(directory="static/uploads"), name="uploads")
    print("✅ Static files serving configuré")
except Exception as e:
    print(f"⚠️  Erreur configuration static files: {e}")
# CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://portfolio-frontend-p72r.onrender.com",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ⭐⭐ IMPORT CORRECT POUR VOTRE STRUCTURE ⭐⭐
try:
    # Essayer d'importer depuis app.api.endpoints
    from app.api.endpoints import router as api_router

    app.include_router(api_router, prefix="/api")
    print("✅ Router API chargé avec succès depuis app.api.endpoints")
except ImportError as e:
    print(f"❌ Erreur chargement router: {e}")

    # Essayer une autre approche
    try:
        # Importer le module directement
        import importlib

        endpoints_module = importlib.import_module("app.api.endpoints")
        app.include_router(endpoints_module.router, prefix="/api")
        print("✅ Router chargé via importlib")
    except Exception as e2:
        print(f"❌ Échec import alternatif: {e2}")
        print("⚠️  Les routes API (/api/projects, etc.) ne seront pas disponibles")


@app.get("/")
def root():
    return {
        "message": "🚀 Portfolio Backend API",
        "status": "online",
        "database": "PostgreSQL on Render",
        "docs": "/docs"
    }


@app.get("/api/health")
def health():
    return {"status": "healthy", "service": "portfolio-backend"}


# Créer les tables au démarrage
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès")
except Exception as e:
    print(f"⚠️  Erreur création tables: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=port)