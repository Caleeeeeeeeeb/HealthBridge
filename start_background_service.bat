@echo off
REM HealthBridge Background Service Script
echo Starting HealthBridge Background Service...
echo This will keep the real-time monitoring active

REM Change to script directory
pushd "%~dp0"

REM Try to find and activate virtual environment
if exist "env\Scripts\Activate.ps1" (
    echo Activating virtual environment: env
    call "env\Scripts\activate"
    goto :runserver
)
if exist "env\Scripts\activate.bat" (
    echo Activating virtual environment: env
    call "env\Scripts\activate.bat"
    goto :runserver
)
if exist "venv\Scripts\Activate.ps1" (
    echo Activating virtual environment: venv
    call "venv\Scripts\activate"
    goto :runserver
)
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment: venv
    call "venv\Scripts\activate.bat"
    goto :runserver
)
if exist ".venv\Scripts\Activate.ps1" (
    echo Activating virtual environment: .venv
    call ".venv\Scripts\activate"
    goto :runserver
)
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment: .venv
    call ".venv\Scripts\activate.bat"
    goto :runserver
)

echo No virtual environment found. Using system Python...

:runserver
echo Starting Django server for real-time monitoring...
echo Press Ctrl+C to stop the service
python manage.py runserver 127.0.0.1:8000

echo Background service stopped
popd
pause