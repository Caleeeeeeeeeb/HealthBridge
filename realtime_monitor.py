"""
Database change monitor
Watches for database file changes and triggers expiry checks
"""
import time
import os
from pathlib import Path
from datetime import datetime

def monitor_database_changes():
    """
    Monitor database file for changes and trigger expiry checks
    More efficient than time-based scheduling
    """
    db_path = Path("C:/Users/Julius Cesar Gamallo/Documents/HealthBridge/db.sqlite3")
    last_modified = 0
    
    print("🔍 Starting real-time database monitoring...")
    print("Will check for expiring medicines whenever database changes")
    
    while True:
        try:
            # Check if database file was modified
            current_modified = os.path.getmtime(db_path)
            
            if current_modified > last_modified:
                last_modified = current_modified
                print(f"📊 Database changed at {datetime.now().strftime('%H:%M:%S')} - checking expiry...")
                
                # Run expiry check
                os.system('cd "C:\\Users\\Julius Cesar Gamallo\\Documents\\HealthBridge" && py manage.py check_expiry')
                
            time.sleep(30)  # Check every 30 seconds
            
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    monitor_database_changes()