# Django Bus Reservation System

A Django application for searching bus schedules, registering and signing in, booking seats, viewing bookings, and cancelling bookings.

## Requirements

- Python 3.10+
- Django 5.2.x (see `requirements.txt`)

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Set a strong secret key in your environment (recommended):

   **Windows PowerShell**
   ```powershell
   $env:DJANGO_SECRET_KEY = "replace-with-a-long-random-secret"
   $env:DJANGO_DEBUG = "True"
   ```

   **macOS/Linux**
   ```bash
   export DJANGO_SECRET_KEY="replace-with-a-long-random-secret"
   export DJANGO_DEBUG="True"
   ```

4. Apply database migrations and create an admin account:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

6. Open http://127.0.0.1:8000/

## Important notes

- The project uses SQLite by default. The database file is created locally and is not included in Git.
- Add bus schedules through the Django admin at `/admin/`.
- The app's booking history uses the built-in Django authentication user ID.
- Back up any existing database before applying migrations to an existing installation.
- Before production deployment, set a unique `DJANGO_SECRET_KEY`, set `DJANGO_DEBUG=False`, configure `DJANGO_ALLOWED_HOSTS`, use HTTPS, and review Django's deployment checklist.
- This repository has been code-reviewed and updated, but it still needs to be run against a real database and tested in the target environment before production use.
