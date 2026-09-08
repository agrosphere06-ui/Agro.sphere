@echo off
title Push Agro-Sphere to GitHub
cd /d "%~dp0"
echo ================================================================
echo   Pushing Agro-Sphere to https://github.com/agrosphere06-ui/Agro.sphere.git
echo ================================================================
echo.
echo Select an authentication option to push:
echo.
echo [1] Quick Browser Login (GitHub Device Flow - Recommended)
echo [2] Enter GitHub Personal Access Token (PAT)
echo.
set /p CHOICE="Choose 1 or 2 (Default: 1): "

if "%CHOICE%"=="2" (
    echo.
    echo If you don't have a token, generate one in 10 seconds at:
    echo https://github.com/settings/tokens/new?scopes=repo^&description=AgroSphere
    echo.
    set /p GITHUB_TOKEN="Enter your GitHub Token (starts with ghp_): "
    echo.
    echo Pushing codebase to agrosphere06-ui/Agro.sphere...
    "C:\Users\Divesh\.gemini\antigravity\scratch\mingit\cmd\git.exe" push https://%GITHUB_TOKEN%@github.com/agrosphere06-ui/Agro.sphere.git main
) else (
    echo.
    echo Launching GitHub Web Authentication...
    "C:\Users\Divesh\.gemini\antigravity\scratch\gh.exe" auth login --web --git-protocol https
    "C:\Users\Divesh\.gemini\antigravity\scratch\gh.exe" auth setup-git
    echo.
    echo Pushing codebase to agrosphere06-ui/Agro.sphere...
    "C:\Users\Divesh\.gemini\antigravity\scratch\mingit\cmd\git.exe" push -u origin main
)

echo.
if %ERRORLEVEL% EQU 0 (
    echo ================================================================
    echo   SUCCESS! All project files are live on GitHub!
    echo   https://github.com/agrosphere06-ui/Agro.sphere
    echo ================================================================
) else (
    echo ================================================================
    echo   Push encountered an error. Please verify your permissions.
    echo ================================================================
)
pause
