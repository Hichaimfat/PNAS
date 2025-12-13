# Script pour lancer le projet (Backend + Frontend)

# Configuration des chemins (Safety check)
$PythonPath = "C:\Users\dr khelifa\AppData\Local\Programs\Python\Python311"
$NodePath = "C:\Program Files\nodejs"
$env:Path = "$PythonPath;$NodePath;$env:Path"

Write-Host "Lancement de PNAS..." -ForegroundColor Green

# Commande de lancement Backend (avec Path explicite dans le sous-processus)
$BackendCmd = "cd backend; `$env:Path = '$PythonPath;$NodePath;`$env:Path'; .\venv\Scripts\activate; uvicorn app.main:app --reload"
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", $BackendCmd

# Commande de lancement Frontend
$FrontendCmd = "cd frontend; `$env:Path = '$NodePath;`$env:Path'; npm run dev"
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", $FrontendCmd

Write-Host "Backend: http://localhost:8000"
Write-Host "Frontend: http://localhost:3000"
