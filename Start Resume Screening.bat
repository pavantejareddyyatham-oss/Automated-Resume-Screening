@echo off
setlocal
cd /d "%~dp0"

set "PYTHON=%~dp0.venv\Scripts\python.exe"
set "URL=http://127.0.0.1:5000"

if not exist "%PYTHON%" (
    echo Python environment not found at .venv
    echo Run this once first:  .venv\Scripts\python.exe -m pip install -r requirements.txt
    pause
    exit /b 1
)

powershell -NoProfile -Command "try { (Invoke-WebRequest -UseBasicParsing -TimeoutSec 1 '%URL%/health').StatusCode } catch { 0 }" | findstr /r "200" >nul
if %ERRORLEVEL%==0 (
    start "" "%URL%"
    exit /b 0
)

start "Automated Resume Screening" "%PYTHON%" "%~dp0app.py"
timeout /t 2 /nobreak >nul
start "" "%URL%"
endlocal
