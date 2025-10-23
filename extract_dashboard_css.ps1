# PowerShell script to extract CSS from dashboard templates and create CSS files

Write-Host "Extracting CSS from dashboard templates..." -ForegroundColor Cyan

# Function to extract CSS between <style> and </style>
function Extract-CSS {
    param($FilePath)
    $content = Get-Content $FilePath -Raw
    if ($content -match '(?s)<style>(.*?)</style>') {
        return $matches[1].Trim()
    }
    return $null
}

# Extract from dashboard.html
$dashboardHTML = "healthbridge_app\templates\healthbridge_app\dashboard.html"
$dashboardCSS = Extract-CSS $dashboardHTML
if ($dashboardCSS) {
    $dashboardCSS | Out-File -FilePath "dashboard\static\dashboard\dashboard.css" -Encoding UTF8
    Write-Host "✓ Created dashboard/static/dashboard/dashboard.css" -ForegroundColor Green
}

# Extract from recipient.html
$recipientHTML = "healthbridge_app\templates\healthbridge_app\recipient.html"
$recipientCSS = Extract-CSS $recipientHTML
if ($recipientCSS) {
    $recipientCSS | Out-File -FilePath "dashboard\static\dashboard\recipient.css" -Encoding UTF8
    Write-Host "✓ Created dashboard/static/dashboard/recipient.css" -ForegroundColor Green
}

Write-Host "`nCSS extraction complete!" -ForegroundColor Green
