from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from .database import Base


class Project(Base):
    __tablename__ = "Projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    technologies = Column(JSON, default=list)
    github_url = Column(String)
    live_url = Column(String)
    screenshots = Column(JSON, default=list)
    image_url = Column(String)          # ← AJOUT ICI
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