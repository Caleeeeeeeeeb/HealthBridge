import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthBridge.settings')
django.setup()

from django.urls import reverse, NoReverseMatch

print('=' * 60)
print('ULTRA-DETAILED NoReverseMatch PREVENTION TEST')
print('=' * 60)

# Extract all {% url %} tags from templates
template_files = [
    'templates/healthbridge_app/select_role.html',
    'templates/dashboard/donor_dashboard.html',
    'templates/dashboard/recipient_dashboard.html',
]

# Extract all redirect() calls from views
view_files = [
    'healthbridge_app/views.py',
    'dashboard/views.py',
]

print('\n1. SCANNING TEMPLATES FOR {% url %} TAGS...')
print('-' * 60)

url_pattern = re.compile(r"{%\s*url\s+['\"]([^'\"]+)['\"]")
template_urls = set()

for template_file in template_files:
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = url_pattern.findall(content)
            if matches:
                print(f'\n{template_file}:')
                for match in matches:
                    template_urls.add(match)
                    print(f'  Found: {match}')
    except FileNotFoundError:
        print(f'\n✗ {template_file}: FILE NOT FOUND!')

print('\n\n2. SCANNING VIEWS FOR redirect() CALLS...')
print('-' * 60)

redirect_pattern = re.compile(r"redirect\(['\"]([^'\"]+)['\"]\)")
view_urls = set()

for view_file in view_files:
    try:
        with open(view_file, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = redirect_pattern.findall(content)
            if matches:
                print(f'\n{view_file}:')
                for match in matches:
                    view_urls.add(match)
                    print(f'  Found: {match}')
    except FileNotFoundError:
        print(f'\n✗ {view_file}: FILE NOT FOUND!')

print('\n\n3. TESTING ALL FOUND URLs...')
print('-' * 60)

all_urls = template_urls.union(view_urls)
failed_urls = []

for url_name in sorted(all_urls):
    try:
        resolved = reverse(url_name)
        print(f'✓ {url_name:50} -> {resolved}')
    except NoReverseMatch as e:
        print(f'✗ {url_name:50} -> FAILED: {e}')
        failed_urls.append((url_name, str(e)))
    except Exception as e:
        print(f'✗ {url_name:50} -> ERROR: {e}')
        failed_urls.append((url_name, str(e)))

print('\n' + '=' * 60)
print('FINAL RESULT')
print('=' * 60)

if failed_urls:
    print(f'\n❌ FOUND {len(failed_urls)} POTENTIAL NoReverseMatch ERRORS:\n')
    for url_name, error in failed_urls:
        print(f'  ✗ {url_name}')
        print(f'    {error}\n')
else:
    print('\n✅ NO NoReverseMatch ERRORS FOUND!')
    print(f'✅ All {len(all_urls)} URLs tested and working correctly')

print('\n' + '=' * 60)
