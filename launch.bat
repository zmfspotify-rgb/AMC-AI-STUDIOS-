@echo off
echo ========================================
echo AMC AI STUDIOS - Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Checking dependencies...
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

REM Launch the application
echo.
echo Starting AMC AI Studios...
echo.
python main.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo Application exited with error code %errorlevel%
    pause
)

deactivate
