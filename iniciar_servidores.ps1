# Iniciar Fotocopiadora SyP - Frontend & Backend Django
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  FOTOCOPIADORA SyP - Iniciando Servidores" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$backendDir = Join-Path $PSScriptRoot "backend"
$pythonExe = Join-Path $backendDir "venv\Scripts\python.exe"

# 1. Iniciar Backend Django en segundo plano (Puerto 8000)
Write-Host "[1/2] Iniciando Backend Django en http://127.0.0.1:8000 ..." -ForegroundColor Yellow
Start-Process -FilePath $pythonExe -ArgumentList "manage.py runserver 8000" -WorkingDirectory $backendDir -WindowStyle Minimized

# 2. Iniciar Frontend (Puerto 5500) y abrir navegador
Write-Host "[2/2] Iniciando Frontend en http://localhost:5500 ..." -ForegroundColor Yellow
Start-Process "http://localhost:5500/index.html"
Start-Process "http://127.0.0.1:8000/admin/"

powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "servidor.ps1")
