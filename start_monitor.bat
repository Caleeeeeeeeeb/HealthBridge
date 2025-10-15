@echo off
REM ============================================================
REM HealthBridge Supabase Monitor - Silent Background Service
REM Runs without popup windows
REM ============================================================

REM Get the script directory (portable)
cd /d "%~dp0"

echo Starting HealthBridge Monitor (silent mode)...

REM Check if virtual environment exists
if not exist env\Scripts\pythonw.exe (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM Start monitor in background using pythonw (no console window)
start "" env\Scripts\pythonw.exe realtime_monitor.py

echo.
echo Monitor started successfully!
echo Running in background without popup windows.
echo.
echo To stop: run stop_monitor.ps1
echo To check status: Task Manager ^> Details ^> pythonw.exe
echo.
timeout /t 3

