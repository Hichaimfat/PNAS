from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, Column, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Index

class Wilaya(SQLModel, table=True):
    __tablename__ = "wilayas"
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str = Field(index=True, unique=True)

class Specialite(SQLModel, table=True):
    __tablename__ = "specialites"
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str = Field(index=True, unique=True)

class Medecin(SQLModel, table=True):
    __tablename__ = "medecins"
    id: Optional[int] = Field(default=None, primary_key=True)
    nom_complet: str = Field(index=True)
    specialite: str = Field(index=True)
    wilaya: str = Field(index=True)
    adresse: Optional[str] = None
    telephone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    site_web: Optional[str] = None
    photo_url: Optional[str] = None
    priorite_pub: int = Field(default=0)
    completude_profil: float = Field(default=0.5)
    date_derniere_mise_a_jour: datetime = Field(default_factory=datetime.now)
    
    # JSONB field for additional info
    informations_additionnelles: Dict[str, Any] = Field(default={}, sa_column=Column(JSONB))

    # Review Trigram/GIN indexes separately in migration or here via __table_args__
    # For simplicity in SQLModel, we rely on Alembic for complex indexes usually, 
    # but we can try to define them in __table_args__.
    __table_args__ = (
        # Index("ix_medecin_nom_complet_trigram", "nom_complet", postgresql_ops={"nom_complet": "gin_trgm_ops"}, postgresql_using="gin"),
        # Leaving complex index definition for Alembic/SQL script logic to keep model simple first
    )
