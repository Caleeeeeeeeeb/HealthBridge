# 🏥 HealthBridge

## 📖 Project Description
HealthBridge is an online platform designed to connect users with nearby pharmacies and medical resources.  
It allows users to search for medicines, request supplies, and manage health-related transactions efficiently.  
The system provides a user-friendly interface for both customers and administrators to ensure smooth and accessible healthcare support.

---

## 🧰 Tech Stack Used
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Django Framework)  
- **Database:** Supabase  

---

## ⚙️ Setup & Run Instructions

1. **Clone the repository**
   git clone https://github.com/Caleeeeeeeeeb/HealthBridge
   cd HealthBridge
   
Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # for Windows

Install dependencies
pip install -r requirements.txt
Run migrations


python manage.py migrate
Start the server
python manage.py runserver

---

## 🚀 Running the Background Service

### Quick Start (Windows)

**Start the Django development server with monitoring:**
```powershell
.\start_background_service.bat
```

**Run expiry check manually:**
```powershell
.\run_expiry_check.bat
```

### What These Scripts Do

- **`start_background_service.bat`** - Starts the Django development server at `http://127.0.0.1:8000/` with auto-reload enabled for real-time monitoring
- **`run_expiry_check.bat`** - Runs the expiry notification system to check for medicines nearing expiration and sends email alerts

Both scripts automatically detect and activate your virtual environment (`env`, `venv`, or `.venv`) if present.

### Command-Line Options for Expiry Check

```powershell
python manage.py check_expiry --days 7          # Check items expiring in 7 days
python manage.py check_expiry --dry-run         # Preview without sending emails
python manage.py check_expiry --force           # Force send even if already notified
python manage.py check_expiry --critical-only   # Only check critical (<3 days)
```

---

## 👨‍💻 Team Members
Name	Role	CIT-U Email
Terence Ed N. Limpio 	      Project Manager	    terenceed.limpio@cit.edu
Keith Daniel P. Lim	        Business Analyst 	  keithdaniel.lim@cit.edu
Rhyz Nhicco C. Libetario	  Scrum Masater	       rhyznhicco.libetario@cit.edu

Junjie L. Geraldez	        Lead Developer	     junjie.geraldez@cit.edu
Benz Leo A. Gamallo	        Developer	           benzleo.gamallo@cit.edu
Rudyard Axel L. Gersamio    Developer	           rudyardaxle.gersamiol@cit.edu
