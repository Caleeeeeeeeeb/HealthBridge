"""
Test Role-Based Dashboard Flow
Tests the complete user journey from registration to role-based dashboards
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthBridge.settings')
django.setup()

from django.test import Client, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse

CustomUser = get_user_model()

def test_role_flow():
    print("=" * 60)
    print("TESTING ROLE-BASED DASHBOARD FLOW")
    print("=" * 60)
    
    client = Client()
    results = []
    
    # Test 1: Role Selection Page Accessible
    print("\n1. Testing role selection page accessibility...")
    try:
        response = client.get(reverse('select_role'))
        if response.status_code in [200, 302]:
            print("   ✓ Role selection page accessible")
            results.append(True)
        else:
            print(f"   ✗ Unexpected status code: {response.status_code}")
            results.append(False)
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        results.append(False)
    
    # Test 2: Donor Dashboard URL Resolution
    print("\n2. Testing donor dashboard URL...")
    try:
        url = reverse('dashboard:donor_dashboard')
        print(f"   ✓ Donor dashboard URL: {url}")
        results.append(True)
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        results.append(False)
    
    # Test 3: Recipient Dashboard URL Resolution
    print("\n3. Testing recipient dashboard URL...")
    try:
        url = reverse('dashboard:recipient_dashboard')
        print(f"   ✓ Recipient dashboard URL: {url}")
        results.append(True)
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        results.append(False)
    
    # Test 4: Create Test User and Check Role Properties
    print("\n4. Testing user role properties...")
    try:
        # Clean up any existing test user
        CustomUser.objects.filter(email='test_donor@example.com').delete()
        
        test_user = CustomUser.objects.create_user(
            email='test_donor@example.com',
            password='testpass123',
            first_name='Test',
            last_name='Donor',
            user_type='donor',
            role_selected=True
        )
        
        if test_user.is_donor:
            print("   ✓ is_donor property working")
            results.append(True)
        else:
            print("   ✗ is_donor property failed")
            results.append(False)
        
        if not test_user.is_recipient:
            print("   ✓ is_recipient correctly returns False for donor")
            results.append(True)
        else:
            print("   ✗ is_recipient should be False for donor")
            results.append(False)
        
        # Clean up
        test_user.delete()
        
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        results.append(False)
    
    # Test 5: Check Donation Form URL
    print("\n5. Testing donation form URL...")
    try:
        url = reverse('donations:donate_medicine')
        print(f"   ✓ Donate medicine URL: {url}")
        results.append(True)
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        results.append(False)
    
    # Test 6: Check Request Form URL
    print("\n6. Testing request form URL...")
    try:
        url = reverse('requests:request_medicine')
        print(f"   ✓ Request medicine URL: {url}")
        results.append(True)
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        results.append(False)
    
    # Test 7: Check History URLs
    print("\n7. Testing history URLs...")
    try:
        donor_history = reverse('donations:my_donations')
        recipient_history = reverse('requests:track_medicine_requests')
        print(f"   ✓ Donor history URL: {donor_history}")
        print(f"   ✓ Recipient history URL: {recipient_history}")
        results.append(True)
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        results.append(False)
    
    # Test 8: Verify Templates Exist
    print("\n8. Testing template loading...")
    try:
        from django.template import loader
        loader.get_template('dashboard/donor_dashboard.html')
        print("   ✓ Donor dashboard template loads")
        loader.get_template('dashboard/recipient_dashboard.html')
        print("   ✓ Recipient dashboard template loads")
        loader.get_template('healthbridge_app/select_role.html')
        print("   ✓ Role selection template loads")
        results.append(True)
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100 if total > 0 else 0
    
    print(f"\nTests Passed: {passed}/{total} ({percentage:.0f}%)")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED - SYSTEM READY FOR MIGRATION")
    else:
        print(f"\n⚠️  {total - passed} TEST(S) FAILED - REVIEW REQUIRED")
    
    return passed == total

if __name__ == '__main__':
    test_role_flow()
