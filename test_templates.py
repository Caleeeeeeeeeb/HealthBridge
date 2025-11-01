import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthBridge.settings')
django.setup()

from django.template.loader import get_template

print('=' * 50)
print('TEMPLATE RENDERING TEST')
print('=' * 50)

templates_to_test = [
    'healthbridge_app/select_role.html',
    'dashboard/donor_dashboard.html',
    'dashboard/recipient_dashboard.html',
]

all_passed = True

for template_path in templates_to_test:
    try:
        template = get_template(template_path)
        print(f'✓ {template_path:45} -> OK')
    except Exception as e:
        print(f'✗ {template_path:45} -> ERROR: {e}')
        all_passed = False

print('\n' + '=' * 50)
if all_passed:
    print('✅ ALL TEMPLATES FOUND!')
else:
    print('❌ SOME TEMPLATES MISSING!')
print('=' * 50)
