#!/usr/bin/env python
"""Test URL resolution for all critical routes"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthBridge.settings')
django.setup()

from django.urls import reverse

urls_to_test = [
    'landing:home',  # Changed from 'index'
    'registration:register',
    'login:login',
    'select_role',  # Changed - it's in root urlconf, no namespace
    'dashboard:donor_dashboard',
    'dashboard:recipient_dashboard',
    'donations:donate_medicine',
    'donations:medicine_search',
    'requests:request_medicine',
    'requests:track_medicine_requests',
    'profile:edit_profile',  # Changed from 'profile'
]

print('\n=== URL RESOLUTION TEST ===\n')
success = 0
failed = 0

for url_name in urls_to_test:
    try:
        path = reverse(url_name)
        print(f'✅ {url_name:40} -> {path}')
        success += 1
    except Exception as e:
        print(f'❌ {url_name:40} -> ERROR: {e}')
        failed += 1

print(f'\n📊 Results: {success} passed, {failed} failed')
print(f'{"✅ ALL URLS WORKING!" if failed == 0 else "⚠️ SOME URLS HAVE ISSUES"}')
