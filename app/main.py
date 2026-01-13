import os
import sys
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Permet les imports relatifs
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 🔥 On importe la base et l'engine depuis database.py
from app.database import engine, Base

# ────────────────────────────────────────────────
# FastAPI
# ────────────────────────────────────────────────

app = FastAPI()

# ────────────────────────────────────────────────
# Static files (uploads)
# ────────────────────────────────────────────────

try:
    os.makedirs("static/uploads/screenshots", exist_ok=True)
    app.mount("/uploads", StaticFiles(directory="static/uploads"), name="uploads")
    print("✅ Static files serving configuré")
except Exception as e:
    print(f"⚠️ Erreur configuration static files: {e}")

# ────────────────────────────────────────────────
# CORS
# ────────────────────────────────────────────────

origins = [
    "https://portfolio-frontend-p72r.onrender.com",
    "http://portfolio-frontend-p72r.onrender.com",

    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ────────────────────────────────────────────────
# Routes API
# ────────────────────────────────────────────────

try:
    from app.api.endpoints import router as api_router
    app.include_router(api_router, prefix="/api")
    print("✅ Router API chargé")
except Exception as e:
    print(f"❌ Erreur chargement router: {e}")

# ────────────────────────────────────────────────
# Health & root
# ────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "message": "🚀 Portfolio Backend API",
        "status": "online",
        "docs": "/docs"
    }

@app.get("/api/health")
def health():
    return {"status": "healthy"}

@app.get("/api/ping")
def ping():
    return {"status": "alive", "time": datetime.utcnow().isoformat()}

# ────────────────────────────────────────────────
# Création des tables
# ────────────────────────────────────────────────

try:
    Base.metadata.create_all(bind=engine)
    print("✅ Tables synchronisées avec la base")
except Exception as e:
    print(f"❌ Erreur création tables: {e}")

# ────────────────────────────────────────────────
# Uvicorn
# ────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
