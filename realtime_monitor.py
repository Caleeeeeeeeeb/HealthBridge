"""
Database change monitor
Watches for database file changes and triggers expiry checks
"""
import time
import os
import sys
from pathlib import Path
from datetime import datetime

def monitor_database_changes():
    """
    Monitor database file for changes and trigger expiry checks
    More efficient than time-based scheduling
    """
    # Get script directory (portable)
    script_dir = Path(__file__).parent.resolve()
    db_path = script_dir / "db.sqlite3"
    last_modified = 0
    
    print("🔍 Starting real-time database monitoring...")
    print(f"📁 Monitoring: {db_path}")
    print("Will check for expiring medicines whenever database changes")
    
    while True:
        try:
            # Check if database file exists
            if not db_path.exists():
                print(f"⚠️  Database not found at {db_path}")
                time.sleep(30)
                continue
            
            # Check if database file was modified
            current_modified = os.path.getmtime(db_path)
            
            if current_modified > last_modified:
                last_modified = current_modified
                print(f"📊 Database changed at {datetime.now().strftime('%H:%M:%S')} - checking expiry...")
                
                # Run expiry check (portable - uses current directory)
                os.chdir(script_dir)
                os.system('python manage.py check_expiry')
                
            time.sleep(30)  # Check every 30 seconds
            
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    monitor_database_changes()