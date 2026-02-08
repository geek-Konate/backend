# backend/init_db.py
import sys
import os

from app.main import existing_skills

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


            Skills = [
                Skill(
                    name="React.js",
                    category="frontend",
                    level=4,
                    icon_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg",
                    description="une bibliothèque JavaScript utilisée pour construire des composants d'interface utilisateur réutilisables",
                    display_order=1

                ),
                Skill(
                    name="Python",
                    category="backend",
                    level=5,
                    icon_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
                    description="Langage de programmation polyvalut pour le développement web et l'analyse de données",
                    display_order=2
                ),
                Skill(
                    name="FastAPI",
                    category="backend",
                    level=4,
                    icon_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg",
                    description="Framework web moderne et rapide pour construire des APIs avec Python",
                    display_order=3
                ),
                Skill(
                    name="PostgreSQL",
                    category="database",
                    level=4,
                    icon_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg",
                    description="Système de gestion de base de données relationnelle open source",
                    display_order=4
                ),
                Skill(
                    name="JavaScript",
                    category="frontend",
                    level=4,
                    icon_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg",
                    description="Langage de programmation pour créer des pages web interactives",
                    display_order=5
                ),
                Skill(
                    name="HTML5",
                    category="frontend",
                    level=5,
                    icon_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg",
                    description="Langage de balisage pour structurer le contenu web",
                    display_order=6
                ),
                Skill(
                    name="CSS3",
                    category="frontend",
                    level=4,
                    icon_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg",
                    description="Langage de style pour mettre en forme les pages web",
                    display_order=7
                ),
                Skill(
                    name="Git",
                    category="tools",
                    level=4,
                    icon_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg",
                    description="Système de contrôle de version distribué",
                    display_order=8
                ),
                Skill(
                    name="Tkinter",
                    category="frontend",
                    level=5,
                    icon_url="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg",
                    description="Bibliothèque Python pour interfaces graphiques",
                    display_order=9
                ),
                Skill(
                    name="SQLite",
                    category="database",
                    level=5,
                    icon_url="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg",
                    description="Base de données légère embarquée",
                    display_order=10
                )
            ]

            existing_skills = db.query(Skill).all()
            existing_names = {skill.name for skill in existing_skills}
            print(f"📊 Compétences existantes: {len(existing_skills)}")
            print(f"📋 Noms existants: {existing_names}")

            missing_skills = []
            for skill_data in Skills:
                if skill_data.name not in existing_names:
                    missing_skills.append(skill_data)
            if missing_skills:
                print(f"🔍 {len(missing_skills)} compétences manquantes trouvées")

            # Créer les objets Skill pour les compétences manquantes
            skills_to_add = []

            for data in missing_skills:
                skill = Skill(
                    name=data["name"],
                    category=data["category"],
                    level=data["level"],
                    icon_url=data["icon_url"],
                    description=data["description"],
                    display_order=data["display_order"]
                )
                skills_to_add.append(skill)
                print(f"   + {data['name']} (display_order: {data['display_order']})")

            db.add_all(skills_to_add)
            db.commit()
            print(f"✅ {len(Skills)} Skills ajoutés")


    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()