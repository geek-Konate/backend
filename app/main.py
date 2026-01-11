import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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