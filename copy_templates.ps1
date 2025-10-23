# PowerShell script to copy templates to modular structure
# Run this from the HealthBridge root directory

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "HealthBridge Template Migration" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

$source = "healthbridge_app\templates\healthbridge_app"

# Landing templates
Write-Host "Copying Landing templates..." -ForegroundColor Yellow
Copy-Item "$source\home.html" "landing\templates\landing\home.html" -Force
Write-Host "✓ home.html copied" -ForegroundColor Green

# Login templates
Write-Host "`nCopying Login templates..." -ForegroundColor Yellow
Copy-Item "$source\login.html" "login\templates\login\login.html" -Force
Copy-Item "$source\password_reset.html" "login\templates\login\password_reset.html" -Force
Copy-Item "$source\password_reset_done.html" "login\templates\login\password_reset_done.html" -ForegroundColor Green
Copy-Item "$source\password_reset_confirm.html" "login\templates\login\password_reset_confirm.html" -Force
Copy-Item "$source\password_reset_complete.html" "login\templates\login\password_reset_complete.html" -Force
Copy-Item "$source\password_reset_email.html" "login\templates\login\password_reset_email.html" -Force
Write-Host "✓ All login templates copied" -ForegroundColor Green

# Registration templates
Write-Host "`nCopying Registration templates..." -ForegroundColor Yellow
Copy-Item "$source\register.html" "registration\templates\registration\register.html" -Force
Write-Host "✓ register.html copied" -ForegroundColor Green

# Dashboard templates
Write-Host "`nCopying Dashboard templates..." -ForegroundColor Yellow
Copy-Item "$source\dashboard.html" "dashboard\templates\dashboard\dashboard.html" -Force
Copy-Item "$source\recipient.html" "dashboard\templates\dashboard\recipient.html" -Force
Write-Host "✓ dashboard.html and recipient.html copied" -ForegroundColor Green

# Donations templates
Write-Host "`nCopying Donations templates..." -ForegroundColor Yellow
Copy-Item "$source\donate_medicine.html" "donations\templates\donations\donate_medicine.html" -Force
Copy-Item "$source\track_requests_list.html" "donations\templates\donations\track_requests_list.html" -Force
Copy-Item "$source\track_request_detail.html" "donations\templates\donations\track_request_detail.html" -Force
Copy-Item "$source\confirm_delete_donation.html" "donations\templates\donations\confirm_delete_donation.html" -Force
Copy-Item "$source\medicine_search.html" "donations\templates\donations\medicine_search.html" -Force
Write-Host "✓ All donations templates copied" -ForegroundColor Green

# Requests templates
Write-Host "`nCopying Requests templates..." -ForegroundColor Yellow
Copy-Item "$source\request_medicine.html" "requests\templates\requests\request_medicine.html" -Force
Copy-Item "$source\track_medicine_requests.html" "requests\templates\requests\track_medicine_requests.html" -Force
Copy-Item "$source\confirm_delete_request.html" "requests\templates\requests\confirm_delete_request.html" -Force

# Check if medicine_request_detail.html exists
if (Test-Path "$source\medicine_request_detail.html") {
    Copy-Item "$source\medicine_request_detail.html" "requests\templates\requests\medicine_request_detail.html" -Force
}
Write-Host "✓ All requests templates copied" -ForegroundColor Green

Write-Host "`n==================================" -ForegroundColor Cyan
Write-Host "Template Migration Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "`nNote: base.html and base_auth.html remain in healthbridge_app (shared)" -ForegroundColor Yellow
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Update template references ({% extends %}, {% include %})" -ForegroundColor White
Write-Host "2. Update {% static %} tags to use new module names" -ForegroundColor White
Write-Host "3. Update {% url %} tags to use namespaces (e.g., 'landing:home')" -ForegroundColor White
Write-Host "4. Run migrations: python manage.py makemigrations" -ForegroundColor White
Write-Host "5. Test each module" -ForegroundColor White
