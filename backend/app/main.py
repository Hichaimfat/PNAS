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

# Scheduler Configuration for Automatic Scraping
# On Vercel (Serverless), we cannot use BackgroundScheduler as the instance freezes/dies.
# We use Vercel Cron to call an endpoint instead.
import subprocess
import os
import logging
from fastapi import Header, HTTPException

logger = logging.getLogger("uvicorn")

@app.get("/api/trigger-scrape")
def trigger_scrape(authorization: Optional[str] = Header(None)):
    # Simple security check (Authorization: Bearer <CRON_SECRET>)
    # For now, we'll just log it. In prod, set CRON_SECRET env var.
    cron_secret = os.getenv("CRON_SECRET")
    if cron_secret and authorization != f"Bearer {cron_secret}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    logger.info("Triggering scraper job via API...")
    try:
        # Determine paths
        # Assuming run from root (Render/Vercel)
        cwd = os.getcwd()
        scraping_dir = os.path.join(cwd, "scraping")
        
        # Fallback for local dev if running from backend folder
        if not os.path.exists(scraping_dir):
            scraping_dir = os.path.join(cwd, "..", "scraping")
            
        if os.path.exists(scraping_dir):
            # Run scrapy as a subprocess
            # Note: In pure serverless, subprocess might be limited. 
            # Ideally, scraping should be a separate service or Cloud Run job.
            # But for Vercel, we can try running it if it fits within timeout (10s-60s).
            # If it takes too long, it will timeout.
            # A better approach for Vercel is to keep this simple or assume it runs fast.
            subprocess.Popen(["scrapy", "crawl", "medecins"], cwd=scraping_dir)
            return {"message": "Scraper triggered successfully"}
        else:
            logger.error("Scraping directory not found.")
            return {"error": "Scraping directory not found"}, 500
    except Exception as e:
        logger.error(f"Failed to run scraper: {e}")
        return {"error": str(e)}, 500

# Migration route (Helper for running migrations from Vercel)
from alembic.config import Config
from alembic import command as alembic_command
import io
from contextlib import redirect_stdout

@app.get("/api/run-migrations")
def run_migrations(authorization: Optional[str] = Header(None)):
    # Security check
    cron_secret = os.getenv("CRON_SECRET")
    if cron_secret and authorization != f"Bearer {cron_secret}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    logger.info("Running migrations via API...")
    try:
        # Capture output
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            # Get paths
            base_dir = os.path.dirname(os.path.abspath(__file__))  # app/
            backend_dir = os.path.dirname(base_dir)  # backend/
            ini_path = os.path.join(backend_dir, "alembic.ini")
            
            alembic_cfg = Config(ini_path)
            alembic_cfg.set_main_option("script_location", os.path.join(backend_dir, "migrations"))
            
            alembic_command.upgrade(alembic_cfg, "head")
            
        return {"message": "Migrations successful", "output": output_buffer.getvalue()}
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return {"error": str(e)}, 500
