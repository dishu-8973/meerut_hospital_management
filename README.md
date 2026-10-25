# Meerut Hospital — Django + FastAPI

Complete Hospital Management starter: premium website (Django), patient login/registration,
appointment booking, admin panel, aur FastAPI REST API (same database).

## Quick start (Windows)

1. Python 3.11+ install karo (python.org).
2. Is folder mein **`setup.bat`** double-click karo
   (venv banata hai, packages install karta hai, migrations chalata hai, sample doctors add karta hai,
   aur admin account banane ko kehta hai).
3. **`run_django.bat`** chalao → http://127.0.0.1:8000/
4. Doosra terminal/window: **`run_api.bat`** chalao → http://127.0.0.1:8001/docs

### Manual commands (VS Code terminal)

```powershell
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt

python manage.py makemigrations hospital
python manage.py migrate
python manage.py seed_doctors        # optional: 6 sample doctors
python manage.py createsuperuser

python manage.py runserver                              # Terminal 1
python -m uvicorn fastapi_app:app --reload --port 8001  # Terminal 2
```

## Pages

| URL | Kaam |
|---|---|
| `/` | Home (hero, departments, doctors) |
| `/doctors/` | Doctors list + search/filter |
| `/register/`, `/login/` | Patient signup / login |
| `/dashboard/` | Patient ki appointments + cancel |
| `/appointments/book/` | Appointment booking (`?doctor=<id>` se doctor pre-select) |
| `/admin/` | Admin panel (doctors, appointments, status) |

## API (FastAPI, port 8001)

| Method | Endpoint | Auth |
|---|---|---|
| GET | `/api/doctors` | public |
| GET | `/api/appointments` | HTTP Basic (Django username/password) |
| POST | `/api/appointments` | HTTP Basic |
| POST | `/api/appointments/{id}/cancel` | HTTP Basic |

POST body example:

```json
{ "doctor_id": 1, "appointment_date": "2027-01-15T10:30:00+05:30", "reason": "General consultation" }
```

## Apni details badalna

`config/settings.py` ke neeche `HOSPITAL_INFO` mein hospital ka naam, phone, email, address aur timing
badlo — poori website mein automatically update ho jayega. Home page par departments ke text
`templates/home.html` mein hain.

## Apni purani HTML/CSS website use karna

Purani pages ko `templates/` mein copy karo, top par `{% extends "base.html" %}` lagao, content ko
`{% block content %}...{% endblock %}` mein daalo, aur CSS/JS/images `static/` folder mein rakh kar
`{% static 'path' %}` se link karo.

## PostgreSQL par switch

```powershell
$env:DB_ENGINE = "postgres"
$env:DB_NAME = "meerut_hospital"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "your-local-database-password"
$env:DB_HOST = "127.0.0.1"
$env:DB_PORT = "5432"
python manage.py migrate
python manage.py createsuperuser
```

SQLite ka purana data automatically PostgreSQL mein nahi jaata. Password code ya GitHub mein mat daalo.

## Production se pehle zaroor karo

- `DJANGO_SECRET_KEY` environment variable set karo, `DJANGO_DEBUG=0`, `DJANGO_ALLOWED_HOSTS` set karo.
- HTTPS lagao (API ka Basic auth sirf HTTPS par safe hai) aur rate limiting / stronger API auth (JWT) add karo.
- Doctor-wise schedule, email/SMS notifications, backups aur patient data privacy rules add karo.

## Folder structure

```
config/        settings, urls, asgi, wsgi
hospital/      models, forms, views, admin, seed_doctors command
templates/     base, home, doctors, dashboard, appointment_form, registration/
static/        css/style.css, js/main.js
fastapi_app.py REST API
```
