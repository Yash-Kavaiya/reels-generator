@echo off
REM Quick launcher for YouTube Reels Automation

echo ========================================
echo YouTube Reels Automation - Gujarati Quotes
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Select an option:
echo 1. Run setup test
echo 2. Create a single reel
echo 3. Run main program (interactive)
echo 4. Run scheduler (automation)
echo 5. Install dependencies
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    python test_setup.py
) else if "%choice%"=="2" (
    python -c "from main import create_reel; create_reel()"
) else if "%choice%"=="3" (
    python main.py
) else if "%choice%"=="4" (
    python scheduler.py
) else if "%choice%"=="5" (
    pip install -r requirements.txt
) else (
    echo Invalid choice
)

echo.
pause
