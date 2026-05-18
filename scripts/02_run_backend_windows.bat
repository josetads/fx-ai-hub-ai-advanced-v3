@echo off
echo === FX AI Hub AI Advanced V3 - Rodando Backend ===
cd /d "%~dp0\..\backend"
call .venv\Scripts\activate.bat
uvicorn app.main:app --reload
pause
