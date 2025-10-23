# PowerShell script to update templates to reference external CSS files

Write-Host "Updating templates to use external CSS files..." -ForegroundColor Cyan

# Function to remove style blocks and add CSS link
function Update-Template {
    param(
        [string]$TemplatePath,
        [string]$CSSPath
    )
    
    if (-not (Test-Path $TemplatePath)) {
        Write-Host "  Warning: Template not found: $TemplatePath" -ForegroundColor Yellow
        return
    }
    
    $content = Get-Content $TemplatePath -Raw
    
    # Remove style block
    $content = $content -replace '(?s)<style>.*?</style>', ''
    
    # Check if load static exists
    if ($content -notmatch '{%\s*load\s+static\s*%}') {
        if ($content -match '({%\s*extends\s+.*?%})') {
            $content = $content -replace '({%\s*extends\s+.*?%})', "`$1`n{% load static %}"
        }
        else {
            $content = "{% load static %}`n" + $content
        }
    }
    
    # Add CSS link
    $cssLink = "<link rel=`"stylesheet`" href=`"{% static '$CSSPath' %}`">"
    
    if ($content -match '{%\s*block\s+extra_css\s*%}') {
        $content = $content -replace '({%\s*endblock\s*%})', "$cssLink`n`$1"
    }
    elseif ($content -match '</head>') {
        $content = $content -replace '</head>', "  $cssLink`n</head>"
    }
    elseif ($content -match '<head>') {
        $content = $content -replace '<head>', "<head>`n  $cssLink"
    }
    
    # Clean up
    $content = $content -replace "`n{3,}", "`n`n"
    
    $content | Out-File -FilePath $TemplatePath -Encoding UTF8 -NoNewline
    Write-Host "  Updated: $TemplatePath" -ForegroundColor Green
}

# Update templates
Update-Template "registration\templates\registration\register.html" "registration/register.css"
Update-Template "donations\templates\donations\donate_medicine.html" "donations/donate_medicine.css"
Update-Template "donations\templates\donations\confirm_delete_donation.html" "donations/confirm_delete_donation.css"
Update-Template "donations\templates\donations\medicine_search.html" "donations/medicine_search.css"
Update-Template "donations\templates\donations\track_requests_list.html" "donations/track_requests_list.css"
Update-Template "donations\templates\donations\track_request_detail.html" "donations/track_request_detail.css"

Write-Host ""
Write-Host "All templates updated successfully!" -ForegroundColor Green
Write-Host "CSS files are now in static directories." -ForegroundColor Cyan
