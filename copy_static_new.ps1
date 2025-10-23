# PowerShell script to copy static files

Write-Host "Copying static files..." -ForegroundColor Yellow

$source = "healthbridge_app\static\healthbridge_app"

if (Test-Path "$source\autocomplete.js") {
    Copy-Item "$source\autocomplete.js" "donations\static\donations\autocomplete.js" -Force
    Write-Host "Copied autocomplete.js" -ForegroundColor Green
}

if (Test-Path "$source\autocomplete.css") {
    Copy-Item "$source\autocomplete.css" "donations\static\donations\autocomplete.css" -Force
    Write-Host "Copied autocomplete.css" -ForegroundColor Green
}

if (Test-Path "$source\style.css") {
    Copy-Item "$source\style.css" "landing\static\landing\style.css" -Force
    Write-Host "Copied style.css" -ForegroundColor Green
}

if (Test-Path "$source\style1.css") {
    Copy-Item "$source\style1.css" "landing\static\landing\style1.css" -Force
    Write-Host "Copied style1.css" -ForegroundColor Green
}

if (Test-Path "$source\script.js") {
    Copy-Item "$source\script.js" "landing\static\landing\script.js" -Force
    Write-Host "Copied script.js" -ForegroundColor Green
}

Write-Host "Static files migration complete!" -ForegroundColor Green
