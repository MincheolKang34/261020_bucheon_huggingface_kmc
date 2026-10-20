@echo off
REM One-click launcher: creates venv, installs requirements, runs the app.
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH. Install Python 3.8+ first.
    pause
    exit /b 1
)

if not exist "venv\Scripts\python.exe" (
    echo [1/3] Creating virtual environment...
    python -m venv venv || goto :fail
)

echo [2/3] Installing requirements...
REM --no-compile avoids Windows long-path errors while writing .pyc files
"venv\Scripts\python.exe" -m pip install -q --no-compile -r requirements.txt || goto :fail

echo [3/3] Starting app... (open http://127.0.0.1:7860)
"venv\Scripts\python.exe" app.py
if errorlevel 1 goto :fail
exit /b 0

:fail
echo [ERROR] Something went wrong. See the messages above.
pause
exit /b 1
