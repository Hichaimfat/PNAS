# Pôle Numérique Algérien de Santé (PNAS)

Plateforme full-stack pour l'annuaire des médecins algériens.

## Structure du Projet

- `backend/`: API FastAPI + Base de données SQLModel.
- `frontend/`: Interface utilisateur Next.js + Tailwind CSS.
- `scraping/`: Moteur de scraping Scrapy.
- `migrations/`: Scripts Alembic pour PostgreSQL.

## Instructions de Démarrage (Local)

### 1. Base de Données (PostgreSQL)
Assurez-vous que PostgreSQL est installé et créez une base :
```sql
CREATE DATABASE pnas_db;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

### 2. Backend
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
pip install -r requirements.txt

# Migrations
alembic upgrade head

# Lancer le serveur
uvicorn app.main:app --reload
```
L'API sera disponible sur `http://localhost:8000`.

### 3. Scraping
```bash
cd scraping
# Assurez-vous d'avoir les dépendances python (pip install scrapy psycopg2-binary)
scrapy crawl medecins
```
*Note: Configurer les identifiants DB dans `scraping/pnas_scraper/settings.py`.*

### 4. Frontend
```bash
cd frontend
npm install
npm run dev
```
Ouvrir `http://localhost:3000`.

## Déploiement Gratuit

### Backend & DB (Render.com)
1. Créez un compte sur Render.
2. Créez un "New Blueprint Instance".
3. Connectez ce dépôt GitHub.
4. Render détectera `render.yaml` et déploiera l'API et la Base de données PostgreSQL automatiquement.

### Frontend (Vercel)
1. Créez un compte Vercel.
2. "Add New Project" -> Import Git Repository.
3. Configurez le `Root Directory` sur `frontend`.
4. Ajoutez la variable d'environnement `NEXT_PUBLIC_API_URL` pointant vers l'URL de votre API Render.
5. Deploy.

---
**Note sur la Monétisation** : Le tri des médecins se fait via la colonne `priorite_pub` (3=Sponsor, 2=Premium, 1=Récent, 0=Standard).
