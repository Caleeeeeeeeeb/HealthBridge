import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthBridge.settings')
django.setup()

from django.urls import reverse

print('=' * 50)
print('COMPREHENSIVE URL TEST')
print('=' * 50)

urls_to_test = {
    'Authentication & Navigation': [
        'select_role',
        'landing:home',
    ],
    'Dashboard URLs': [
        'dashboard:dashboard',
        'dashboard:donor_dashboard',
        'dashboard:recipient_dashboard',
    ],
    'Donation URLs': [
        'donations:donate_medicine',
        'donations:my_donations',
    ],
    'Request URLs': [
        'requests:request_medicine',
        'requests:track_medicine_requests',
    ],
}

all_passed = True

for category, urls in urls_to_test.items():
    print(f'\n{category}:')
    for url_name in urls:
        try:
            resolved = reverse(url_name)
            print(f'  ✓ {url_name:40} -> {resolved}')
        except Exception as e:
            print(f'  ✗ {url_name:40} -> ERROR: {e}')
            all_passed = False

print('\n' + '=' * 50)
if all_passed:
    print('✅ ALL URLS RESOLVED SUCCESSFULLY!')
else:
    print('❌ SOME URLS FAILED!')
print('=' * 50)
