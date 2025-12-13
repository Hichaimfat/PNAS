# Script d'installation automatique pour PNAS

$ErrorActionPreference = "Stop"

# Configuration des chemins (Adapté à l'installation faite par l'assistant)
$PythonPath = "C:\Users\dr khelifa\AppData\Local\Programs\Python\Python311"
$NodePath = "C:\Program Files\nodejs"

# Ajouter au PATH de la session actuelle
$env:Path = "$PythonPath;$NodePath;$env:Path"

Write-Host ">>> Démarrage de l'installation..." -ForegroundColor Green

# 1. Vérification des outils
Write-Host "1. Vérification des outils..."
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "CRITIQUE: Python n'est pas trouvé. Vérifiez C:\Users\dr khelifa\AppData\Local\Programs\Python\Python311"
    exit 1
}
if (!(Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Error "CRITIQUE: Node.js/npm n'est pas trouvé. Vérifiez C:\Program Files\nodejs"
    exit 1
}

Write-Host "   - Python : $(Get-Command python | Select-Object -ExpandProperty Source)"
Write-Host "   - Node   : $(Get-Command node | Select-Object -ExpandProperty Source)"

# 2. Setup Backend
Write-Host "`n2. Installation du Backend (Python)..." -ForegroundColor Cyan
Set-Location "backend" 

if (!(Test-Path "venv")) {
    Write-Host "   - Création de l'environnement virtuel..."
    python -m venv venv
}

Write-Host "   - Installation des dépendances..."
# Utilisation de python -m pip pour plus de robustesse
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m pip install alembic # Ensure alembic is installed

Write-Host "   - Application des migrations de base de données..."
try {
    .\venv\Scripts\python.exe -m alembic upgrade head
    Write-Host "   - Migrations appliquées avec succès." -ForegroundColor Green
}
catch {
    Write-Warning "   - Erreur lors des migrations. Assurez-vous que PostgreSQL est lancé et 'pnas_db' créé."
    Write-Warning "   - Erreur: $_"
}

Set-Location ..

# 3. Setup Frontend
Write-Host "`n3. Installation du Frontend (Node.js)..." -ForegroundColor Cyan
Set-Location "frontend"
if (Test-Path "package.json") {
    Write-Host "   - Installation des modules Node..."
    npm install
}
else {
    Write-Error "Dossier frontend incomplet (package.json manquant)."
}
Set-Location ..

Write-Host "`n>>> Installation terminée avec succès !" -ForegroundColor Green
Write-Host "Pour lancer le projet, utilisez 'run_app.ps1'."
Write-Host "Appuyez sur Entrée pour quitter..."
Read-Host
