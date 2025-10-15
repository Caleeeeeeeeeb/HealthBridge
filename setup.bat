@echo off
REM ============================================================
REM HealthBridge - One-Click Setup Script
REM Portable installation for team members
REM ============================================================

echo.
echo ============================================================
echo    HealthBridge - Automated Setup
echo ============================================================
echo.

REM Get the script directory (portable - works from any location)
cd /d "%~dp0"

echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
python --version
echo.

echo [2/5] Creating virtual environment...
if exist env (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv env
    echo Virtual environment created!
)
echo.

echo [3/5] Activating virtual environment...
call env\Scripts\activate.bat
echo.

echo [4/5] Installing dependencies...
pip install --upgrade pip
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    pip install django python-dotenv dj-database-url psycopg2-binary pillow
)
echo.

echo [5/5] Checking .env configuration...
if exist .env (
    echo .env file found!
    echo Please verify your DATABASE_URL and email settings.
) else (
    echo WARNING: .env file not found!
    echo Creating template .env file...
    (
        echo # HealthBridge Configuration
        echo # Replace with your actual credentials
        echo.
        echo # Database ^(Supabase PostgreSQL^)
        echo DATABASE_URL=postgresql://your-connection-string-here
        echo.
        echo # Email Settings
        echo EMAIL_HOST=smtp.gmail.com
        echo EMAIL_PORT=587
        echo EMAIL_HOST_USER=your-email@gmail.com
        echo EMAIL_HOST_PASSWORD=your-app-password
    ) > .env
    echo.
    echo IMPORTANT: Edit .env file with your actual credentials!
    echo See QUICK_START.md for team credentials.
)
echo.

echo ============================================================
echo    Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Edit .env file with your database and email credentials
echo   2. Run: env\Scripts\activate
echo   3. Run: python manage.py migrate
echo   4. Run: python manage.py runserver
echo.
echo For automated background monitoring:
echo   - Run: start_monitor.bat
echo.
echo Full instructions: See QUICK_START.md
echo.
pause
