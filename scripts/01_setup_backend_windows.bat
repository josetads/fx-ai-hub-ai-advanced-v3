@echo off
echo === FX AI Hub AI Advanced V3 - Setup Backend ===
cd /d "%~dp0\..\backend"
python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
echo Setup concluido.
pause
