
from sqlalchemy.orm import Session
from . import models, schemas
def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()


def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project_update: schemas.ProjectUpdate):
    db_project = get_project(db, project_id)
    if db_project:
        # Convertit l'objet Pydantic en dict, en excluant les valeurs None
        update_data = project_update.dict(exclude_unset=True)
        # Met à jour chaque champ
        for field, value in update_data.items():
            setattr(db_project, field, value)
        db.commit()
        db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)

    if db_project:
        db.delete(db_project)
        db.commit()

    return db_project.
    from sqlalchemy import create_engine


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://portfolio_user:9725@localhost:5432/portfolio_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close().
        from fastapi import FastAPI


from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints import router
from .database import engine, Base
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Portfolio API", version="1.0.0")

# cors pour react

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Dev local
        "http://127.0.0.1:5173",  # Alternative
        "http://10.210.115.254:5173",  # TON IP réseau
        "http://192.168.1.*",  # Réseau local (wildcard)
        "*"  # TEMPORAIRE pour test
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/uploads", StaticFiles(directory="static/uploads"), name="uploads")
app.include_router(router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Portfolio API is running"}.
    from sqlalchemy import Column, Integer, Boolean, DateTime, String, Text, JSON


from sqlalchemy.sql import func
from .database import Base


class Project(Base):
    __tablename__ = "Projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    technologies = Column(JSON)
    github_url = Column(String(300))
    live_url = Column(String(300))
    screenshots = Column(JSON, default=[])
    image_url = Column(String(300))
    featured = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    slug = Column(String(200), unique=True, index=True)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))  # frontend, backend, database, tools, design
    level = Column(Integer, default=3)  # 1-5
    icon_url = Column(String(300))
    description = Column(Text)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    from pydantic import BaseModel, HttpUrl, EmailStr


from typing import Optional, List
from datetime import datetime
from fastapi.responses import JSONResponse


class ProjectBase(BaseModel):
    title: str
    description: str
    technologies: List[str]
    screenshots: List[str] = []
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    image_url: Optional[str] = None
    featured: bool = False


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    title: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[List[str]] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    featured: Optional[bool] = None
    screenshots: Optional[List[str]] = None


class ContactForm(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    topic: str
    message: str
    agree_terms: bool


class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True.
        import axios
        from
        "axios";


const
API_BASE_URL = "http://localhost:8000/api";
export
const
api = axios.create({
    baseURL: API_BASE_URL,
});

// reccupreation
de
tous
les
projects
export
const
getProjects = async () = > {
    const
response = await api.get("/projects");
return response.data;
};

// créer
un
projects

export
const
createProject = async (projectData) = > {
const
response = await api.post("/projects", projectData);
return response.data;
};
// supprimer
un
project
export
const
deleteProject = async (id) = > {
const
response = await api.delete(` / projects /${id}
`);

return response.data;
};
// met
à
jour
un
project
export
const
updateProject = async (id, projectData) = > {
const
response = await api.put(` / projects /${id}
`, projectData);
return response.data;
};
// Récupère
un
seul
projet
export
const
getProject = async (id) = > {
const
response = await api.get(` / projects /${id}
`);
return response.data;
};
// Ajoute
des
screenshots
à
un
projet
existant
export
const
addScreenshotsToProject = async (projectId, files) = > {
const
formData = new
FormData();
files.forEach((file) = > {
    formData.append("new_files", file);
});
const
response = await api.patch(
    ` / projects /${projectId} / screenshots
`,
formData,
{
    headers: {
        "Content-Type": "multipart/form-data",
    },
}
);
return response.data;
};
export
const
uploadScreenshots = async (files) = > {
const
formData = new
FormData();

files.forEach((file) = > {
    formData.append("files", file); // Nom
important: 'files'(pluriel)
});

try {
const response = await api.post("/upload/screenshots", formData, {
headers: {
    "Content-Type": "multipart/form-data",
},
});

// Retourne
seulement
les
URLs
return response.data.urls;
} catch(error)
{
console.error("Upload error:", error.response?.data | | error.message);
throw
error;
}
};

// pourquoi
est
ce
que
sur
mon
telephone, les
données
du
backend
ne
se
charge
pas, mais
avec
l
'ordinateur , c'
est
nickel.