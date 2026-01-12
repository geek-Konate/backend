# backend/init_db.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, Base, SessionLocal
from models import Project, Skill  # Importez vos modèles
from datetime import datetime


def init_database():
    """Peupler la base avec des données initiales"""
    print("🔄 Initialisation de la base de données...")

    # Créer les tables si elles n'existent pas
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Vérifier si des données existent déjà
        existing_projects = db.query(Project).count()

        if existing_projects == 0:
            print("📦 Ajout des données initiales...")

            # Ajouter des projets
            projects = [
                Project(
                    title="Portfolio Full-Stack",
                    description="Portfolio personnel avec React et FastAPI",
                    technologies="React, FastAPI, PostgreSQL, TailwindCSS",
                    image_url="https://via.placeholder.com/300x200",
                    github_url="https://github.com/votreusername/portfolio",
                    live_url="https://portfolio-frontend-p72r.onrender.com",
                    featured=True,
                    created_at=datetime.now()
                ),
                Project(
                    title="API REST",
                    description="API REST avec authentification JWT",
                    technologies="FastAPI, JWT, SQLAlchemy, PostgreSQL",
                    image_url="https://via.placeholder.com/300x200",
                    github_url="https://github.com/votreusername/api-rest",
                    featured=True,
                    created_at=datetime.now()
                ),
                Project(
                    title="Application E-commerce",
                    description="Site e-commerce avec panier et paiement",
                    technologies="React, Node.js, Stripe, MongoDB",
                    image_url="https://via.placeholder.com/300x200",
                    github_url="https://github.com/votreusername/ecommerce",
                    featured=False,
                    created_at=datetime.now()
                )
            ]

            for project in projects:
                db.add(project)

            db.commit()
            print(f"✅ {len(projects)} projets ajoutés")

        else:
            print(f"✅ Base déjà initialisée ({existing_projects} projets existants)")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()