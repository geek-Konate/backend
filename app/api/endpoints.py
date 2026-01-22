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
    return crud.create_project(db=db, project=project)


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
async def update_project_screenshots(project_id: int, new_files: List[UploadFile] = File(...),
                                     db: Session = Depends(get_db)):
    # ajouter des screenshot a un project existant
    # Vérifie le projet
    db_project = crud.get_project(db, project_id=project_id)
    if not db_project:
        raise HTTPException(404, "Project not found")
    # Upload les nouveaux fichiers
    upload_result = await upload_screenshots(new_files)
    new_urls = [item["url"] for item in upload_result["urls"]]
    # combinaison avec les anciens screenshots

    current_screenshot = db_project.screenshots or []
    updated_screenshots = current_screenshot + new_urls
    db_project.screenshots = updated_screenshots
    db.commit()
    db.refresh(db_project)

    return {
        "message": "Screenshots added successfully",
        "new_urls": new_urls,
        "total_screenshots": len(updated_screenshots),
        "project": schemas.Project.from_orm(db_project)
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
                    res = supabase.storage.from_('porfolio').remove([filename])
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


# pour gerer upload
@router.post("/upload/screenshots")
async def upload_screenshots(files: List[UploadFile] = File(...)):
    uploaded_urls = []


    for file in files:
        # Genère un nom de fichier unique
        file_extension = file.filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        # lire le contenu du fichier
        content = await file.read()
        # Envoyer vers Supabase Storage
        response = supabase.storage.from_('porfolio').upload(unique_filename, content)
        if response.get("error"):
            return {"error": response["error"]}

        # URL d'accès - PAS BESOIN DU /static ici car on monte /uploads
        url = supabase.storage.from_('porfolio').get_public_url(unique_filename)
        uploaded_urls.append(url['publicURL'])

    return {"urls": uploaded_urls}


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

        # 1. Préparer email
        msg = MIMEMultipart()
        msg['Subject'] = f"📩 Portfolio: {contact.topic}"
        msg['From'] = f"Portfolio <{EMAIL_USER}>"
        msg['To'] = EMAIL_USER  # Toi
        msg['Reply-To'] = f"{contact.first_name} {contact.last_name} <{contact.email}>"

        # 2. Contenu
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
                <p>   La réponse ira automatiquement à: {contact.email}</p>
            </div>
        </div>
        """
        msg.attach(MIMEText(html, 'html'))

        # 3. Envoyer email
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()  # Démarre la connexion sécurisée
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email envoyé avec Reply-To: {contact.email}")
        return {"success": True}

    except Exception as e:
        print(f"❌ Erreur SMTP: {str(e)}")
        return {"success": False}


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