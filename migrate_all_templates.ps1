# PowerShell script to copy ALL templates to modular structure and extract CSS

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  HealthBridge Template & CSS Migration Script" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

$sourceBase = "healthbridge_app\templates\healthbridge_app"

# Define all template mappings
$templateMappings = @(
    # Login module
    @{Source="$sourceBase\login.html"; Dest="login\templates\login\login.html"; CSS="login/login.css"},
    
    # Dashboard module
    @{Source="$sourceBase\dashboard.html"; Dest="dashboard\templates\dashboard\dashboard.html"; CSS="dashboard/dashboard.css"},
    @{Source="$sourceBase\recipient.html"; Dest="dashboard\templates\dashboard\recipient.html"; CSS="dashboard/recipient.css"},
    
    # Donations module (already done but let's verify)
    @{Source="$sourceBase\donate_medicine.html"; Dest="donations\templates\donations\donate_medicine.html"; CSS="donations/donate_medicine.css"},
    @{Source="$sourceBase\medicine_search.html"; Dest="donations\templates\donations\medicine_search.html"; CSS="donations/medicine_search.css"},
    @{Source="$sourceBase\track_requests_list.html"; Dest="donations\templates\donations\track_requests_list.html"; CSS="donations/track_requests_list.css"},
    @{Source="$sourceBase\track_request_detail.html"; Dest="donations\templates\donations\track_request_detail.html"; CSS="donations/track_request_detail.css"},
    @{Source="$sourceBase\confirm_delete_donation.html"; Dest="donations\templates\donations\confirm_delete_donation.html"; CSS="donations/confirm_delete_donation.css"},
    
    # Requests module
    @{Source="$sourceBase\request_medicine.html"; Dest="requests\templates\requests\request_medicine.html"; CSS="requests/request_medicine.css"},
    @{Source="$sourceBase\track_medicine_requests.html"; Dest="requests\templates\requests\track_medicine_requests.html"; CSS="requests/track_medicine_requests.css"},
    
    # Registration module (already done but verify)
    @{Source="$sourceBase\register.html"; Dest="registration\templates\registration\register.html"; CSS="registration/register.css"}
)

# Function to extract CSS from template
function Extract-CSS {
    param($FilePath)
    if (-not (Test-Path $FilePath)) {
        return $null
    }
    $content = Get-Content $FilePath -Raw
    if ($content -match '(?s)<style>(.*?)</style>') {
        return $matches[1].Trim()
    }
    return $null
}

# Function to update template (remove style block, add CSS link)
function Update-TemplateContent {
    param($Content, $CSSPath)
    
    # Remove style block
    $Content = $Content -replace '(?s)<style>.*?</style>', ''
    
    # Check if load static exists
    if ($Content -notmatch '{%\s*load\s+static\s*%}') {
        if ($Content -match '({%\s*extends\s+.*?%})') {
            $Content = $Content -replace '({%\s*extends\s+.*?%})', "`$1`n{% load static %}"
        }
        else {
            $Content = "{% load static %}`n" + $Content
        }
    }
    
    # Add CSS link
    $cssLink = "<link rel=`"stylesheet`" href=`"{% static '$CSSPath' %}`">"
    
    if ($Content -match '{%\s*block\s+extra_css\s*%}') {
        $Content = $Content -replace '({%\s*endblock\s*%})', "$cssLink`n`$1"
    }
    elseif ($Content -match '</head>') {
        $Content = $Content -replace '</head>', "  $cssLink`n</head>"
    }
    elseif ($Content -match '<head>') {
        $Content = $Content -replace '<head>', "<head>`n  $cssLink"
    }
    
    # Clean up extra blank lines
    $Content = $Content -replace "`n{3,}", "`n`n"
    
    return $Content
}

Write-Host "Step 1: Copying templates and extracting CSS..." -ForegroundColor Yellow
Write-Host ""

foreach ($mapping in $templateMappings) {
    $source = $mapping.Source
    $dest = $mapping.Dest
    $cssPath = $mapping.CSS
    
    if (-not (Test-Path $source)) {
        Write-Host "  [SKIP] Source not found: $source" -ForegroundColor Red
        continue
    }
    
    # Extract CSS first
    $css = Extract-CSS $source
    if ($css) {
        $cssFile = $cssPath -replace '/', '\'
        $cssFullPath = $cssFile -replace '^([^\\]+)\\', '$1\static\$1\'
        
        # Only create CSS file if it doesn't exist yet
        if (-not (Test-Path $cssFullPath)) {
            $css | Out-File -FilePath $cssFullPath -Encoding UTF8
            Write-Host "  [CSS] Created: $cssFullPath" -ForegroundColor Green
        }
    }
    
    # Read template content
    $content = Get-Content $source -Raw
    
    # Update template content
    $updatedContent = Update-TemplateContent $content $cssPath
    
    # Write to destination
    $updatedContent | Out-File -FilePath $dest -Encoding UTF8 -NoNewline
    
    Write-Host "  [TEMPLATE] Copied: $dest" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "  Migration Complete!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Summary:" -ForegroundColor Yellow
Write-Host "  - All templates copied to module directories" -ForegroundColor White
Write-Host "  - CSS extracted and moved to static directories" -ForegroundColor White
Write-Host "  - Templates updated to use external CSS files" -ForegroundColor White
Write-Host ""
Write-Host "Next: Run 'python manage.py runserver' to test!" -ForegroundColor Cyan
