"""
Supabase Database Monitor for HealthBridge
Monitors Supabase PostgreSQL database and triggers expiry checks
Uses periodic polling since Supabase is a remote database
Runs silently in background without popup windows
"""
import time
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import django
from django.db import connection

def setup_django():
    """Initialize Django to access database"""
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthBridge.settings')
    django.setup()

def check_database_connection():
    """Verify connection to Supabase"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            if 'PostgreSQL' in version:
                return True, "Supabase (PostgreSQL)"
        return False, "Unknown database"
    except Exception as e:
        return False, str(e)

def monitor_database_changes():
    """
    Monitor Supabase database and trigger expiry checks periodically
    Uses smart polling instead of file monitoring
    """
    script_dir = Path(__file__).parent.resolve()
    
    print("🔍 Starting Supabase real-time monitoring...")
    print(f"📁 Working directory: {script_dir}")
    
    # Setup Django and verify connection
    try:
        setup_django()
        connected, db_info = check_database_connection()
        
        if connected:
            print(f"✅ Connected to {db_info}")
        else:
            print(f"❌ Database connection failed: {db_info}")
            return
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return
    
    print("🔄 Monitoring for expiring medicines every 2 minutes...")
    print("Press Ctrl+C to stop\n")
    
    check_interval = 120  # Check every 2 minutes
    
    while True:
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"📊 [{timestamp}] Running expiry check...")
            
            # Run expiry check command silently (no popup window)
            os.chdir(script_dir)
            result = subprocess.run(
                [sys.executable, 'manage.py', 'check_expiry'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            
            # Print output for logging purposes
            if result.stdout:
                print(result.stdout.strip())
            
            if result.returncode == 0:
                print(f"✅ Check completed successfully")
            else:
                print(f"⚠️  Check completed with warnings (exit code: {result.returncode})")
                if result.stderr:
                    print(f"Error: {result.stderr.strip()}")
            
            print(f"⏰ Next check in {check_interval} seconds...\n")
            time.sleep(check_interval)
            
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
            break
        except Exception as e:
            print(f"❌ Error during check: {e}")
            print("Retrying in 60 seconds...")
            time.sleep(60)

if __name__ == "__main__":
    monitor_database_changes()