# HealthBridge - Quick Start Guide

## 🚀 Setup (First Time)

```bash
# 1. Clone the repo
git clone https://github.com/Caleeeeeeeeeb/HealthBridge.git
cd HealthBridge

# 2. Run setup
setup.bat

# 3. Edit .env file with these credentials:
```

**.env file:**
```
DATABASE_URL=postgresql://postgres.rovbuexxvufsylkahhgw:HealthBridge@aws-1-us-east-2.pooler.supabase.com:5432/postgres
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=healthbridge.expiryalerts123@gmail.com
EMAIL_HOST_PASSWORD=vxze zjtx nrip uhhr
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
