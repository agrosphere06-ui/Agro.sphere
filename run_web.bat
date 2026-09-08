@echo off
title Agro-Sphere Server Launcher
cd /d "%~dp0"
echo ========================================================
echo   Starting Agro-Sphere Web Server (FastAPI + Vite)
echo ========================================================
echo.
echo Opening Agro-Sphere in your default browser...
start "" "http://localhost:5000"
echo Starting backend server on http://localhost:5000 ...
npm run dev
pause
