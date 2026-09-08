@echo off
title Agro-Sphere Public Web Server
echo ===================================================
echo   AGRO-SPHERE - LIVE CLOUD TUNNEL FOR JUDGES
echo ===================================================
echo.
echo Starting FastAPI backend on port 5000...
start /b py -3.13 server.py
timeout /t 3 >nul
echo.
echo Starting Cloudflare Public HTTPS Tunnel...
echo.
.\cloudflared.exe tunnel --url http://127.0.0.1:5000
pause
