from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select, desc, col, case
from typing import List, Optional
from .models import Medecin
from .database import get_session
from sqlalchemy import func

app = FastAPI(title="PNAS API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API du Pôle Numérique Algérien de Santé"}

@app.post("/api/medecins", response_model=Medecin)
def create_medecin(medecin: Medecin, session: Session = Depends(get_session)):
    session.add(medecin)
    session.commit()
    session.refresh(medecin)
    return medecin

@app.get("/api/medecins/{id}", response_model=Medecin)
def get_medecin(id: int, session: Session = Depends(get_session)):
    medecin = session.get(Medecin, id)
    if not medecin:
        raise HTTPException(status_code=404, detail="Medecin not found")
    return medecin

@app.get("/api/medecins/recherche", response_model=List[Medecin])
def search_medecins(
    q: Optional[str] = None,
    wilaya: Optional[str] = None,
    specialite: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    session: Session = Depends(get_session)
):
    query = select(Medecin)

    # Filters
    if wilaya:
        query = query.where(func.lower(Medecin.wilaya) == wilaya.lower())
    if specialite:
        query = query.where(func.lower(Medecin.specialite) == specialite.lower())
    
    # Trigram Search for Q (using ilike for now for compatibility if extension not active, usually we use matches)
    if q:
        # Simple ilike on multiple fields
        query = query.where(
            (func.lower(Medecin.nom_complet).contains(q.lower())) |
            (func.lower(Medecin.specialite).contains(q.lower()))
        )

    # Sorting Logic (Monetization tiers)
    # 3: Sponsor, 2: Complete profile, 1: Recently updated, 0: Alphabetical
    
    # Order by priority class first (descending)
    # Then break ties based on specific logic per class
    query = query.order_by(
        desc(Medecin.priorite_pub),
        
        # Tie breakers
        case(
            (Medecin.priorite_pub == 3, desc(Medecin.date_derniere_mise_a_jour)), # Sponsors sorted by Recency? or Random? Let's say Recency.
            (Medecin.priorite_pub == 2, desc(Medecin.completude_profil)),          # Tier 2 by completeness
            (Medecin.priorite_pub == 1, desc(Medecin.date_derniere_mise_a_jour)),  # Tier 1 by update
            else_=Medecin.nom_complet                                              # Tier 0 (default) alphabetical
        )
    )

    query = query.offset(skip).limit(limit)
    
    results = session.exec(query).all()
    return results
