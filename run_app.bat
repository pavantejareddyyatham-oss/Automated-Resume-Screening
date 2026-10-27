@echo off
setlocal
cd /d "%~dp0"

echo Checking project environment...
if not exist "venv_new\Scripts\python.exe" (
    echo Virtual environment not found. Creating it now...
    py -3.10 -m venv venv_new
)

echo Installing required packages...
"%~dp0venv_new\Scripts\python.exe" -m pip install --upgrade pip
"%~dp0venv_new\Scripts\python.exe" -m pip install -r requirements.txt
echo.
echo Starting Resume Screening Application...
"%~dp0venv_new\Scripts\python.exe" app.py
pause