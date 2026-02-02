# AVMS — Django version (scaffold)

This workspace contains a scaffolded Django project (`avms_project`) and an app (`visitors`) implementing the Visitor model and a REST API powered by Django REST Framework.

Quick start (Windows):

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Configure database

Edit `avms_project/settings.py` DATABASES section or set env vars. Example (MySQL):

4. Run migrations and start server

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Notes:
- If `mysqlclient` is hard to build on Windows, install `mysql-connector-python` and update `ENGINE` in `settings.py` to `mysql.connector.django` (see docs).
- The API endpoints are available at `/api/visitors/` for CRUD operations.
