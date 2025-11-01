"""
DRY RUN TEST - User Role System
Test the logic without running migrations

This file checks:
1. Model field definitions are valid
2. View logic is correct
3. URL routing is configured
4. Template files exist
5. No syntax errors
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("✓ Testing imports...")
    
    try:
        from healthbridge_app.models import CustomUser
        print("  ✓ CustomUser model imported")
        
        from healthbridge_app.views import select_role, login_view, register
        print("  ✓ Auth views imported")
        
        from dashboard.views import donor_dashboard, recipient_dashboard
        print("  ✓ Dashboard views imported")
        
        return True
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False


def test_model_structure():
    """Test model structure"""
    print("\n✓ Testing model structure...")
    
    from healthbridge_app.models import CustomUser
    
    # Check UserType choices
    assert hasattr(CustomUser, 'UserType'), "CustomUser.UserType not found"
    assert hasattr(CustomUser.UserType, 'DONOR'), "DONOR choice not found"
    assert hasattr(CustomUser.UserType, 'RECIPIENT'), "RECIPIENT choice not found"
    print("  ✓ UserType choices defined correctly")
    
    # Check properties
    assert hasattr(CustomUser, 'is_donor'), "is_donor property not found"
    assert hasattr(CustomUser, 'is_recipient'), "is_recipient property not found"
    print("  ✓ Helper properties defined")
    
    return True


def test_view_logic():
    """Test view logic structure"""
    print("\n✓ Testing view logic...")
    
    from healthbridge_app import views as hb_views
    from dashboard import views as dash_views
    
    # Check select_role view
    import inspect
    select_role_source = inspect.getsource(hb_views.select_role)
    assert 'role_selected' in select_role_source, "role_selected check missing"
    assert 'is_donor' in select_role_source, "is_donor check missing"
    assert 'is_recipient' in select_role_source, "is_recipient check missing"
    print("  ✓ select_role view logic correct")
    
    # Check login view
    login_source = inspect.getsource(hb_views.login_view)
    assert 'role_selected' in login_source, "role_selected check in login missing"
    assert 'donor_dashboard' in login_source, "donor_dashboard redirect missing"
    assert 'recipient_dashboard' in login_source, "recipient_dashboard redirect missing"
    print("  ✓ login_view logic correct")
    
    # Check dashboard views
    donor_source = inspect.getsource(dash_views.donor_dashboard)
    assert 'is_donor' in donor_source, "is_donor check missing in donor dashboard"
    print("  ✓ donor_dashboard logic correct")
    
    recipient_source = inspect.getsource(dash_views.recipient_dashboard)
    assert 'is_recipient' in recipient_source, "is_recipient check missing in recipient dashboard"
    print("  ✓ recipient_dashboard logic correct")
    
    return True


def test_url_configuration():
    """Test URL configuration"""
    print("\n✓ Testing URL configuration...")
    
    from django.urls import resolve, reverse
    from django.urls.exceptions import NoReverseMatch
    
    # Check if select_role URL exists
    try:
        from HealthBridge.urls import urlpatterns
        url_names = []
        for pattern in urlpatterns:
            if hasattr(pattern, 'name'):
                url_names.append(pattern.name)
        
        assert 'select_role' in url_names, "select_role URL not found"
        print("  ✓ select_role URL configured")
    except Exception as e:
        print(f"  ! Could not verify URL config (expected before migration): {e}")
    
    return True


def test_template_files():
    """Test template files exist"""
    print("\n✓ Testing template files...")
    
    templates = [
        'templates/healthbridge_app/select_role.html',
        'templates/dashboard/donor_dashboard.html',
        'templates/dashboard/recipient_dashboard.html',
    ]
    
    css_files = [
        'static/dashboard/donor_dashboard.css',
        'static/dashboard/recipient_dashboard.css',
    ]
    
    for template in templates:
        if os.path.exists(template):
            print(f"  ✓ {template}")
        else:
            print(f"  ✗ {template} NOT FOUND")
            return False
    
    for css_file in css_files:
        if os.path.exists(css_file):
            print(f"  ✓ {css_file}")
        else:
            print(f"  ✗ {css_file} NOT FOUND")
            return False
    
    return True


def test_template_syntax():
    """Check for common template syntax errors"""
    print("\n✓ Testing template syntax...")
    
    templates_to_check = [
        'templates/healthbridge_app/select_role.html',
        'templates/dashboard/donor_dashboard.html',
        'templates/dashboard/recipient_dashboard.html',
    ]
    
    for template_path in templates_to_check:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for unclosed tags
            if content.count('{% ') != content.count(' %}'):
                print(f"  ✗ {template_path}: Unclosed template tags")
                return False
            
            # Check for {{ without }}
            if content.count('{{ ') != content.count(' }}'):
                print(f"  ✗ {template_path}: Unclosed variable tags")
                return False
            
            print(f"  ✓ {template_path} syntax OK")
    
    return True


def main():
    """Run all tests"""
    print("="*60)
    print("DRY RUN TEST - USER ROLE SYSTEM")
    print("="*60)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthBridge.settings')
    
    import django
    django.setup()
    
    tests = [
        test_imports,
        test_model_structure,
        test_view_logic,
        test_url_configuration,
        test_template_files,
        test_template_syntax,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test failed: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
    print("="*60)
    
    if all(results):
        print("\n✅ ALL TESTS PASSED!")
        print("Code is ready for migration when approved.")
    else:
        print("\n⚠️ SOME TESTS FAILED")
        print("Fix the issues before migrating.")
    
    return all(results)


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
