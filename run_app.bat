@echo off
echo ========================================
echo    Medicine Reminder Application
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
python -c "import kivy" >nul 2>&1
if errorlevel 1 (
    echo Installing Kivy and dependencies...
    pip install kivy kivymd pandas gtts
)

echo [2/3] Starting Medicine Reminder App...
echo.
python main.py

echo.
echo [3/3] Application closed.
pause
