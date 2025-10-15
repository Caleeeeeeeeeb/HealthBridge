# HealthBridge - Quick Start Guide

## 🚀 Setup (First Time)

```bash
# 1. Clone the repo
git clone https://github.com/Caleeeeeeeeeb/HealthBridge.git
cd HealthBridge

# 2. Run setup
setup.bat

# 3. Edit .env file with the project set up notepad file
```



```bash
# 4. Setup database
env\Scripts\activate
python manage.py migrate

# 5. Run the server
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

---

## 🔄 Background Monitor (Optional)

Automatically checks for expiring medicines every 2 minutes.

**Start:** `start_monitor.bat`  
**Stop:** `.\stop_monitor.ps1`  
**Check status:** `check_status.bat`

---

## 📝 Daily Use

```bash
cd HealthBridge
env\Scripts\activate
python manage.py runserver
```

That's it!
