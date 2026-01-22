from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi import File, UploadFile
import shutil
import uuid
import os


from .. import crud, schemas
from ..database import get_db
from ..models import Skill
import socket 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

from app.storage import supabase

load_dotenv()
router = APIRouter()
@router.get("/projects", response_model=List[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = crud.get_projects(db, skip=skip, limit=limit)

    return projects
@router.post("/projects", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_project(db=db, project=project)
    except Exception as e:
        print("❌ Erreur création projet:", e)
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    #    mettre a jour un project existant
    # verifier si le project exist
    db_project = crud.get_project(db, project_id=project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project no found"

        )
    project_update = crud.update_project(
        db=db,
        project_id=project_id,
        project_update=project
    )

    return project_update


# modification des screenshots du project
@router.patch("/projects/{project_id}/screenshots")
async def update_project_screenshots(
    project_id: int,
    new_files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    db_project = crud.get_project(db, project_id)
    if not db_project:
        raise HTTPException(404, "Project not found")

    new_urls = await upload_files_to_supabase(new_files)

    current = db_project.screenshots or []
    db_project.screenshots = current + new_urls

    db.commit()
    db.refresh(db_project)

    return {
        "message": "Screenshots added successfully",
        "new_urls": new_urls,
        "total_screenshots": len(db_project.screenshots)
    }



# suppression d'un project
@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    # supprimer un project et ses screensht
    # recupérer le project
    db_project = crud.get_project(db, project_id=project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    # suppression des fichiers screenshot liée au project
    if db_project.screenshots:
        for screenshot in db_project.screenshots:
            if screenshot and isinstance(screenshot, str):
                # extraire le nom du fichier de l'url
                filename = screenshot.split("/")[-1]

                try:
                    res = supabase.storage.from_('portfolio').remove([filename])
                    if res.get('error'):
                        print(f"Failed to remove {filename} : {res['error']}")

                except Exception as e:
                    print(f"Exception deleting {filename}: {e}")

    # suprimer de la base de données
    crud.delete_project(db, project_id=project_id)
    return {
        "message": "Project deleted successfully",
        "deleted_id": project_id
    }
@router.post("/upload/screenshots")
async def upload_screenshots(files: List[UploadFile] = File(...)):
    urls = []

    for file in files:
        ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"

        content = await file.read()

        try:
            supabase.storage.from_("portfolio").upload(
                path=filename,
                file=content,
                file_options={"content-type": file.content_type}
            )

            public_url = supabase.storage.from_("portfolio").get_public_url(filename)
            urls.append(public_url)  # 👈 plus de dict, juste la string

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Supabase upload failed: {str(e)}"
            )

    return {"urls": urls}
@router.get("/skills")
def get_skills(db: Session = Depends(get_db)):
    try:
        # Essaie d'importer dynamiquement
        from ..models import Skill
        skills = db.query(Skill).order_by(Skill.display_order).all()
        return skills
    except ImportError:
        # Fallback: données en dur
        return [
            {"id": 1, "name": "React", "category": "frontend", "level": 4},
            {"id": 2, "name": "Python", "category": "backend", "level": 5},
            {"id": 3, "name": "FastAPI", "category": "backend", "level": 4},
            {"id": 4, "name": "PostgreSQL", "category": "database", "level": 4},
            {"id": 5, "name": "Git", "category": "tools", "level": 4},
        ]

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))  # CHANGE DE 465 À 587
EMAIL_USE_TLS = True  # AJOUTE CETTE LIGNE
@router.post("/contact")
async def submit_contact_form(contact: schemas.ContactForm):
    try:
        print(f"📨 {contact.first_name} ({contact.email})")

        # Log pour debug
        print(f"🔧 Configuration SMTP:")
        print(f"  Host: {EMAIL_HOST}")
        print(f"  Port: {EMAIL_PORT}")
        print(f"  User: {EMAIL_USER}")
        print(f"  TLS: {EMAIL_USE_TLS}")

        # 1. Préparer email
        msg = MIMEMultipart()
        msg['Subject'] = f"📩 Portfolio: {contact.topic}"
        msg['From'] = f"Portfolio <{EMAIL_USER}>"
        msg['To'] = EMAIL_USER  # Vous recevez l'email
        msg['Reply-To'] = f"{contact.first_name} {contact.last_name} <{contact.email}>"

        # 2. Contenu HTML
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px;">
            <h2 style="color: #2563eb;">Nouveau message portfolio</h2>
            <div style="background: #f3f4f6; padding: 20px; border-radius: 8px;">
                <p><strong>👤 Visiteur:</strong> {contact.first_name} {contact.last_name}</p>
                <p><strong>📧 Email:</strong> {contact.email}</p>
                <p><strong>📱 Téléphone:</strong> {contact.phone or 'Non fourni'}</p>
                <p><strong>🏷️ Sujet:</strong> {contact.topic}</p>
            </div>
            <div style="margin-top: 20px; padding: 20px; background: #f8fafc; border-left: 4px solid #2563eb;">
                <h4>💬 Message:</h4>
                <p style="white-space: pre-line;">{contact.message}</p>
            </div>
            <hr style="margin: 30px 0;">
            <div style="font-size: 12px; color: #6b7280;">
                <p>📅 Reçu le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
                <p>⚠️ <strong>Pour répondre:</strong> Clique sur "Répondre" dans ton client email.</p>
                <p>La réponse ira automatiquement à: {contact.email}</p>
            </div>
        </div>
        """

        # Alternative texte simple pour debug
        text = f"""
        Nouveau message portfolio:

        Nom: {contact.first_name} {contact.last_name}
        Email: {contact.email}
        Téléphone: {contact.phone or 'Non fourni'}
        Sujet: {contact.topic}

        Message:
        {contact.message}

        ---
        Reçu le {datetime.now().strftime('%d/%m/%Y à %H:%M')}
        """

        # Ajouter les deux versions
        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html'))

        # 3. Envoyer email avec timeout
        print(f"📤 Connexion SMTP à {EMAIL_HOST}:{EMAIL_PORT}...")

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=10) as server:
            print(f"🔒 Démarrage TLS...")
            server.starttls()  # Démarre la connexion sécurisée

            print(f"🔑 Authentification...")
            server.login(EMAIL_USER, EMAIL_PASSWORD)

            print(f"🚀 Envoi du message...")
            server.send_message(msg)
            print(f"✅ Email envoyé avec succès!")

        return {"success": True, "message": "Email envoyé avec succès"}

    except smtplib.SMTPException as e:
        print(f"❌ Erreur SMTP: {str(e)}")
        return {"success": False, "error": f"Erreur SMTP: {str(e)}"}
    except socket.error as e:
        print(f"❌ Erreur réseau: {str(e)}")
        return {"success": False, "error": f"Erreur réseau: {str(e)}"}
    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")
        return {"success": False, "error": f"Erreur: {str(e)}"}


@router.get("/mobile-test")
async def mobile_test():
    """Test spécifique pour mobile"""
    return {
        "mobile": True,
        "message": "✅ Backend accessible depuis mobile",
        "timestamp": datetime.now().isoformat(),
        "api_version": "1.0",
        "endpoints": {
            "projects": "/api/projects",
            "contact": "/api/contact",
            "skills": "/api/skills"
        }
    }


@router.get("/test-email")
async def test_email():
    """Test la connexion SMTP"""
    try:
        # Test de connexion sans envoyer d'email
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            print("✅ Connexion SMTP réussie")
            server.quit()

        return {
            "success": True,
            "message": "Connexion SMTP OK",
            "host": EMAIL_HOST,
            "port": EMAIL_PORT
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "host": EMAIL_HOST,
            "port": EMAIL_PORT
        }