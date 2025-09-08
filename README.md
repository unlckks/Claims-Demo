```markdown
# 🏥 Claims Management System

A lightweight **insurance claims management system** built with **Django**, **HTMX**, and **Alpine.js**.  
It provides an interactive UI to search, filter, view details, add notes, and flag/unflag claims for review.

---

## ✨ Features
- 🔍 **Search & Filter** by patient, insurer, status, or claim ID  
- 📄 **Detail View (HTMX)** – load claim details without full page reload  
- 🚩 **Flagging** – manually flag claims for review, with audit trail  
- 📝 **Notes** – add custom annotations with author & timestamp  
- ⚡ **HTMX partial updates** for list rows, detail panels, and notes  
- 🔒 **Authentication** – secure access using Django’s auth system  

---

## 🛠 Tech Stack
- **Backend**: Django 4.x (Python 3.10+)  
- **Database**: SQLite (default, file-based, no setup required)  
- **Frontend**: HTML / CSS + HTMX + Alpine.js  
- **Templates**: Django Templates  

---

## 📂 Project Structure
```

erisa\_Project/
├─ manage.py
├─ db.sqlite3               # SQLite DB (auto-created after migrations)
├─ data/                    # Sample data
│   ├─ claim\_list\_data.json
│   └─ claim\_detail\_data.json
├─ erisa\_Project/           # Project settings package
│   ├─ settings.py
│   ├─ urls.py
│   └─ ...
├─ claims/                  # Claims app
│   ├─ models.py
│   ├─ views.py
│   ├─ urls.py
│   ├─ templates/claims/
│   │   ├─ list.html
│   │   ├─ \_detail.html
│   │   ├─ \_notes.html
│   │   └─ base.html
│   └─ management/commands/
│       └─ load\_claims.py

````

---

## 🚀 Setup & Run

### 1. Clone & Install
```bash
git clone https://github.com/yourusername/claims-app
cd claims-app
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
````

### 2. Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Admin User

```bash
python manage.py createsuperuser
```

### 4. Load Sample Data

Ensure `data/` contains:

* `claim_list_data.json`
* `claim_detail_data.json`

Then run:

```bash
python manage.py load_claims --list data/claim_list_data.json --detail data/claim_detail_data.json --mode overwrite
```

### 5. Start Server

```bash
python manage.py runserver
```

Access:

* Claims app → [http://127.0.0.1:8000/claims/](http://127.0.0.1:8000/claims/)
* Admin dashboard → [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 📦 Data Format

### claim\_list\_data.json

```json
[
  {
    "id": 30001,
    "patient_name": "Virginia Rhodes",
    "billed_amount": 639787.37,
    "paid_amount": 16001.57,
    "status": "Denied",
    "insurer_name": "United Healthcare",
    "discharge_date": "2022-12-18"
  }
]
```

### claim\_detail\_data.json

```json
[
  {
    "id": 1,
    "claim_id": 30001,
    "cpt_codes": "99204,82947,99406",
    "denial_reason": "Policy terminated before service date"
  }
]
```

---

## 🖥 Usage

* Left panel: claim list with filters and search
* Right panel: details load dynamically via HTMX
* Quick actions: flag/unflag claims, add notes, generate report placeholder
* Notes: stored with user + timestamp

---



