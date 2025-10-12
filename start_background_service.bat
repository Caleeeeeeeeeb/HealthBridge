@echo off
REM HealthBridge Background Service Script
REM Keeps Django server running in background for real-time monitoring

echo Starting HealthBridge Background Service...
echo This will keep the real-time monitoring active

REM Change to the HealthBridge directory
cd /d "C:\Users\Julius Cesar Gamallo\Documents\HealthBridge"

REM Activate virtual environment and start server
echo Activating virtual environment...
call env\Scripts\activate.bat

echo Starting Django server for real-time monitoring...
echo Press Ctrl+C to stop the service

REM Start Django server (this keeps running)
python manage.py runserver 127.0.0.1:8000

echo Background service stopped
pause