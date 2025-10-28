# Quick Reference: Centralized Structure

## File Locations

### Templates
All in: `healthbridge_app/templates/[module]/`

| Module | Location | Files |
|--------|----------|-------|
| Dashboard | `healthbridge_app/templates/dashboard/` | dashboard.html, recipient.html |
| Donations | `healthbridge_app/templates/donations/` | donate_medicine.html, medicine_search.html, track_requests_list.html, track_request_detail.html, confirm_delete_donation.html |
| Landing | `healthbridge_app/templates/landing/` | home.html |
| Login | `healthbridge_app/templates/login/` | login.html, password_reset*.html |
| Profile | `healthbridge_app/templates/profile/` | profile.html, edit_profile.html, change_password*.html |
| Registration | `healthbridge_app/templates/registration/` | register.html |
| Requests | `healthbridge_app/templates/requests/` | request_medicine.html, track_medicine_requests.html, confirm_delete_request.html |

### Static Files
All in: `healthbridge_app/static/[module]/`

| Module | Location | Files |
|--------|----------|-------|
| Dashboard | `healthbridge_app/static/dashboard/` | dashboard.css, recipient.css, images |
| Donations | `healthbridge_app/static/donations/` | *.css, autocomplete.js |
| Landing | `healthbridge_app/static/landing/` | style.css, script.js |
| Login | `healthbridge_app/static/login/` | login.css |
| Profile | `healthbridge_app/static/profile/` | profile.css |
| Registration | `healthbridge_app/static/registration/` | register.css |
| Requests | `healthbridge_app/static/requests/` | *.css |

## Usage in Code

### In Views (No Change Needed!)
```python
# Views already use correct paths
return render(request, 'dashboard/dashboard.html')
return render(request, 'donations/donate_medicine.html')
return render(request, 'login/login.html')
```

### In Templates
```html
<!-- Load static files -->
{% load static %}
<link rel="stylesheet" href="{% static 'dashboard/dashboard.css' %}">
<script src="{% static 'donations/autocomplete.js' %}"></script>

<!-- Extend base templates -->
{% extends 'healthbridge_app/base.html' %}

<!-- Include partials -->
{% include 'healthbridge_app/navbar.html' %}
```

### In URLs (No Change Needed!)
```python
# urls.py files don't need changes
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]
```

## Quick Commands

```powershell
# Check Django configuration
python manage.py check

# Run development server
python manage.py runserver 127.0.0.1:8080

# Collect static files (for production)
python manage.py collectstatic

# List all templates Django can find
python manage.py shell
>>> from django.template.loader import get_template
>>> template = get_template('dashboard/dashboard.html')
>>> print(template.origin.name)
```

## Benefits

✅ **Single source of truth** - All files in healthbridge_app  
✅ **Module organization** - Clear folder structure by feature  
✅ **Easy navigation** - Find any template/static file quickly  
✅ **Deployment ready** - Simplified collectstatic process  
✅ **Backward compatible** - Original files still work as fallback  

## Key Points

1. **Django finds templates automatically** via `APP_DIRS = True`
2. **Views don't need changes** - paths like `'dashboard/dashboard.html'` work
3. **Static files work** - `{% static 'module/file.css' %}` resolves correctly
4. **Original module directories cleaned** - No more duplicate templates/static folders
5. **Single source of truth** - All files exclusively in `healthbridge_app/`

---

*Created: October 28, 2025*
*Updated: October 28, 2025 - Module directories cleaned*
