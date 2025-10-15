@echo off
REM Quick status check for HealthBridge monitoring

echo.
echo ============================================================
echo    HealthBridge Status Check
echo ============================================================
echo.

echo Checking for background monitor...
tasklist /FI "IMAGENAME eq pythonw.exe" 2>NUL | find /I /N "pythonw.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Monitor is RUNNING
    echo.
    tasklist /FI "IMAGENAME eq pythonw.exe" /FO TABLE
) else (
    echo [X] Monitor is NOT running
    echo     Run: start_monitor.bat to start it
)

echo.
echo ============================================================
echo.

echo Checking for Django server...
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Python processes detected
    echo     If runserver is running, visit: http://127.0.0.1:8000
) else (
    echo [X] Django server is NOT running
    echo     Run: python manage.py runserver
)

echo.
echo ============================================================
echo.
pause
