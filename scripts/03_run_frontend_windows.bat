@echo off
echo === FX AI Hub AI Advanced V3 - Rodando Frontend ===
cd /d "%~dp0\..\frontend"
npm install
npm run dev
pause
