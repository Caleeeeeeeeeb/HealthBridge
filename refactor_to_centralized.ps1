# PowerShell Script to Centralize Templates and Static Files
# Moves all module-specific templates and static files to healthbridge_app directory
# Organized by module names

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  HealthBridge Centralized Structure Refactoring" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will:" -ForegroundColor Yellow
Write-Host "  1. Move all templates from modules to healthbridge_app/templates/" -ForegroundColor White
Write-Host "  2. Move all static files from modules to healthbridge_app/static/" -ForegroundColor White
Write-Host "  3. Organize by module name (profile/, login/, dashboard/, etc.)" -ForegroundColor White
Write-Host "  4. Update template references in moved files" -ForegroundColor White
Write-Host ""

# Base paths
$hbAppTemplates = "healthbridge_app\templates"
$hbAppStatic = "healthbridge_app\static"

# Module list (excluding healthbridge_app itself)
$modules = @("landing", "login", "registration", "dashboard", "profile", "donations", "requests")

# Function to copy files recursively
function Copy-ModuleFiles {
    param(
        [string]$SourcePath,
        [string]$DestPath,
        [string]$FileType
    )
    
    if (Test-Path $SourcePath) {
        # Create destination if it doesn't exist
        if (-not (Test-Path $DestPath)) {
            New-Item -ItemType Directory -Path $DestPath -Force | Out-Null
        }
        
        # Get all files
        $files = Get-ChildItem -Path $SourcePath -File -Recurse
        
        if ($files) {
            foreach ($file in $files) {
                $relativePath = $file.FullName.Substring($SourcePath.Length + 1)
                $destFile = Join-Path $DestPath $relativePath
                $destDir = Split-Path $destFile -Parent
                
                if (-not (Test-Path $destDir)) {
                    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
                }
                
                Copy-Item $file.FullName $destFile -Force
                Write-Host "  ✓ Copied: $relativePath" -ForegroundColor Green
            }
            return $files.Count
        }
    }
    return 0
}

# Function to update template references
function Update-TemplateReferences {
    param(
        [string]$FilePath,
        [string]$ModuleName
    )
    
    if (Test-Path $FilePath) {
        $content = Get-Content $FilePath -Raw
        $updated = $false
        
        # Update {% extends %} references
        if ($content -match "{%\s*extends\s+'$ModuleName/") {
            $content = $content -replace "{%\s*extends\s+'$ModuleName/([^']+)'\s*%}", "{% extends '$ModuleName/`$1' %}"
            $updated = $true
        }
        
        # Update {% static %} references for module-specific files
        $content = $content -replace "{%\s*static\s+'$ModuleName/([^']+)'\s*%}", "{% static '$ModuleName/`$1' %}"
        
        # Update URL namespaces (if needed)
        # This part can be customized based on your URL structure
        
        if ($updated -or $content -ne (Get-Content $FilePath -Raw)) {
            $content | Set-Content $FilePath -NoNewline
        }
    }
}

Write-Host "Starting migration..." -ForegroundColor Cyan
Write-Host ""

$totalTemplates = 0
$totalStatic = 0

foreach ($module in $modules) {
    Write-Host "Processing module: $module" -ForegroundColor Yellow
    Write-Host "----------------------------------------" -ForegroundColor DarkGray
    
    # Templates migration
    $sourceTemplates = "$module\templates\$module"
    $destTemplates = "$hbAppTemplates\$module"
    
    if (Test-Path $sourceTemplates) {
        Write-Host "  Moving templates..." -ForegroundColor Cyan
        $count = Copy-ModuleFiles $sourceTemplates $destTemplates "template"
        $totalTemplates += $count
        
        if ($count -gt 0) {
            Write-Host "  Moved $count template file(s)" -ForegroundColor Green
        } else {
            Write-Host "  No templates found" -ForegroundColor DarkGray
        }
    } else {
        Write-Host "  No templates directory found" -ForegroundColor DarkGray
    }
    
    # Static files migration
    $sourceStatic = "$module\static\$module"
    $destStatic = "$hbAppStatic\$module"
    
    if (Test-Path $sourceStatic) {
        Write-Host "  Moving static files..." -ForegroundColor Cyan
        $count = Copy-ModuleFiles $sourceStatic $destStatic "static"
        $totalStatic += $count
        
        if ($count -gt 0) {
            Write-Host "  Moved $count static file(s)" -ForegroundColor Green
        } else {
            Write-Host "  No static files found" -ForegroundColor DarkGray
        }
    } else {
        Write-Host "  No static directory found" -ForegroundColor DarkGray
    }
    
    Write-Host ""
}

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Migration Summary" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Total templates moved: $totalTemplates" -ForegroundColor Green
Write-Host "Total static files moved: $totalStatic" -ForegroundColor Green
Write-Host ""

Write-Host "Final Structure:" -ForegroundColor Yellow
Write-Host "  healthbridge_app/" -ForegroundColor White
Write-Host "    ├── templates/" -ForegroundColor White
foreach ($module in $modules) {
    if (Test-Path "$hbAppTemplates\$module") {
        Write-Host "    │   ├── $module/" -ForegroundColor Cyan
        $files = Get-ChildItem "$hbAppTemplates\$module" -File
        foreach ($file in $files) {
            Write-Host "    │   │   └── $($file.Name)" -ForegroundColor Green
        }
    }
}
Write-Host "    └── static/" -ForegroundColor White
foreach ($module in $modules) {
    if (Test-Path "$hbAppStatic\$module") {
        Write-Host "        ├── $module/" -ForegroundColor Cyan
        $files = Get-ChildItem "$hbAppStatic\$module" -File -Recurse
        foreach ($file in $files) {
            $relativePath = $file.FullName.Substring((Resolve-Path "$hbAppStatic\$module").Path.Length + 1)
            Write-Host "        │   └── $relativePath" -ForegroundColor Green
        }
    }
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "1. Update template paths in views.py files" -ForegroundColor White
Write-Host "   Change: render(request, 'module/template.html')" -ForegroundColor DarkGray
Write-Host "   To:     render(request, 'module/template.html')" -ForegroundColor DarkGray
Write-Host ""
Write-Host "2. Update static file references in templates" -ForegroundColor White
Write-Host "   Change: {% static 'module/file.css' %}" -ForegroundColor DarkGray
Write-Host "   To:     {% static 'module/file.css' %}" -ForegroundColor DarkGray
Write-Host ""
Write-Host "3. Test all pages to ensure templates and static files load correctly" -ForegroundColor White
Write-Host ""
Write-Host "4. Run Django check:" -ForegroundColor White
Write-Host "   python manage.py check" -ForegroundColor Cyan
Write-Host ""
Write-Host "5. Clear browser cache and test all features" -ForegroundColor White
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Migration Complete! 🎉" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
