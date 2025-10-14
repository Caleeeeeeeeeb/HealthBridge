@echo off
REM HealthBridge Expiry Monitoring Automation Script
echo Starting HealthBridge Expiry Check at %date% %time%

REM Change to the script directory (portable)
pushd "%~dp0"

REM Auto-detect virtual environment folder (env, venv, .venv)
set "ACTIVATE="
if exist "%~dp0env\Scripts\activate.bat" set "ACTIVATE=%~dp0env\Scripts\activate.bat"
if "%ACTIVATE%"=="" if exist "%~dp0venv\Scripts\activate.bat" set "ACTIVATE=%~dp0venv\Scripts\activate.bat"
if "%ACTIVATE%"=="" if exist "%~dp0.venv\Scripts\activate.bat" set "ACTIVATE=%~dp0.venv\Scripts\activate.bat"

if "%ACTIVATE%"=="" (
    echo No virtual environment found. Using system Python...
) else (
    echo Activating virtual environment: %ACTIVATE%
    call "%ACTIVATE%"
)

REM Run the expiry check command
python manage.py check_expiry

echo Expiry check completed at %date% %time%

REM Optional: Log the results (uncomment next line if you want logs)
REM echo %date% %time% - Expiry check completed >> expiry_check.log

popd
pause