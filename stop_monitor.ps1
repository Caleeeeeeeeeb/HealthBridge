# HealthBridge Monitor - Stop Script
# Stops the running monitor process

Write-Host "Stopping HealthBridge Monitor..." -ForegroundColor Yellow

# Find and stop pythonw.exe processes running realtime_monitor.py
$processes = Get-Process pythonw -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*realtime_monitor.py*"
}

if ($processes) {
    $processes | ForEach-Object {
        Stop-Process -Id $_.Id -Force
        Write-Host "✅ Stopped process ID: $($_.Id)" -ForegroundColor Green
    }
} else {
    Write-Host "No monitor processes found running." -ForegroundColor Yellow
}

# Also check for regular python.exe
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*realtime_monitor.py*"
}

if ($pythonProcesses) {
    $pythonProcesses | ForEach-Object {
        Stop-Process -Id $_.Id -Force
        Write-Host "✅ Stopped process ID: $($_.Id)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Monitor stopped." -ForegroundColor Cyan
