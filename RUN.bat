@echo off
echo ========================================
echo AMC AI STUDIOS - SIMPLE LAUNCHER
echo ========================================
echo.

REM Simple launcher without virtual environment
REM Just installs dependencies and runs the app

echo Step 1: Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.10+ from python.org
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b 1
)

echo Step 2: Installing dependencies...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet python-dotenv pydantic flask flask-cors

echo Step 3: Starting application...
echo.
echo ========================================
echo Opening AMC AI Studios...
echo ========================================
echo.

python main.py

if %errorlevel% neq 0 (
    echo.
    echo Application closed with error
    pause
)
