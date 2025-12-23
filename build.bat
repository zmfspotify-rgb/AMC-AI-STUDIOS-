@echo off
echo ========================================
echo AMC AI STUDIOS - Build Executable
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

REM Build executable
echo.
echo Building Windows executable...
pyinstaller AMC_AI_Studios.spec

echo.
echo Build complete! Executable is in dist\AMC_AI_Studios\
echo.
pause
