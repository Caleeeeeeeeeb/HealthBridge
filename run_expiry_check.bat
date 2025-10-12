@echo off
REM HealthBridge Expiry Monitoring Automation Script
REM This script runs the expiry check automatically

echo Starting HealthBridge Expiry Check at %date% %time%

REM Change to the HealthBridge directory
cd /d "C:\Users\Julius Cesar Gamallo\Documents\HealthBridge"

REM Run the expiry check command
py manage.py check_expiry

echo Expiry check completed at %date% %time%

REM Optional: Log the results (uncomment next line if you want logs)
REM echo %date% %time% - Expiry check completed >> expiry_check.log