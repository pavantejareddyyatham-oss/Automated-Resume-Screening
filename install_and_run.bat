@echo off
setlocal
cd /d "%~dp0"

echo ==================================================
echo Resume Screening Application Setup and Run
echo ==================================================

echo.
if not exist "venv_new\Scripts\python.exe" (
    echo [1/2] Creating virtual environment...
    py -3.10 -m venv venv_new
)

echo [1/2] Installing required packages...
"%~dp0venv_new\Scripts\python.exe" -m pip install --upgrade pip
"%~dp0venv_new\Scripts\python.exe" -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install packages. Please check your Python and pip installation.
    goto :error
)

echo.
echo [2/2] Starting the application...
echo.
echo The application will start now. Please open your web browser and go to:
echo http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the application when you're done.
echo.
"%~dp0venv_new\Scripts\python.exe" app.py
goto :end

:error
echo.
echo There was an error during setup.
echo Please try running these commands manually:
echo 1. "%~dp0venv_new\Scripts\python.exe" -m pip install -r requirements.txt
echo 2. "%~dp0venv_new\Scripts\python.exe" app.py

:end
pause 