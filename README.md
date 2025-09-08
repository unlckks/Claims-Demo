---

# 🏥 Claims Management System

A lightweight **claims review and management system** built with **Django**, **HTMX**, and **Alpine.js**.
It provides an interactive interface to search, filter, view details, add notes, and flag/unflag insurance claims.

---

## ✨ Features

* 🔍 **Search & Filter** claims by patient, insurer, status, or claim ID
* 📄 **Detail View** with CPT codes, denial reasons, billed/paid amounts
* 📝 **Notes** with author and timestamp, added directly from detail view
* 🚩 **Flagging** claims for review with audit tracking
* ⚡ **HTMX partial updates** (no full-page reloads)
* 🔒 **CSRF-protected requests** for security

---

## 📦 Requirements

* Python **3.10+**
* Django **4.x / 5.x**
* SQLite (default) or any Django-supported database

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/claims-app.git
cd claims-app
```

### 2. Create & activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create an admin user

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Now open: [http://127.0.0.1:8000/claims/](http://127.0.0.1:8000/claims/)

---

## 🗂️ Project Structure

```
apps/claims/
├── models.py          # Claim, ClaimDetail, Flag, Note models
├── views.py           # List, detail, row, add note, toggle flag
├── urls.py            # Routes for the claims app
└── templates/claims/
    ├── base.html          # Global styles + HTMX + Alpine setup
    ├── list.html          # Main layout (list + detail panel)
    ├── _list.html         # Table partial
    ├── _row.html          # Single row partial
    ├── _detail.html       # Claim detail view
    └── _notes_block.html  # Notes block partial
```


