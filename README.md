# The Gents' Corner — Django Barber Shop

Django barber shop website with database-backed services, barbers and bookings, responsive UI, Google Calendar integration and downloadable ICS events.

## Local setup

Create and activate a virtual environment, then install dependencies:

    python -m venv venv
    .\\venv\\Scripts\\Activate.ps1
    pip install -r requirements.txt

Copy `.env.example` to `.env` and set your Neon `DATABASE_URL`. Keep the real credentials in `.env`; never commit that file.

Then run:

    python manage.py check
    python manage.py migrate
    python manage.py seed_shop
    python manage.py createsuperuser
    python manage.py runserver

Open http://127.0.0.1:8000/ and http://127.0.0.1:8000/admin/.

## Neon PostgreSQL

When `DATABASE_URL` is present, Django uses Neon PostgreSQL automatically. Use an SSL connection string such as:

    postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require&channel_binding=require

For deployment, configure `DATABASE_URL` as a hosting-platform environment variable/secret. Do not put database credentials in source code.

## Database commands

    python manage.py migrate
    python manage.py seed_shop
    python manage.py check

## Security

- `.env` is ignored by Git.
- `.env.example` contains placeholders only.
- Production secrets belong in deployment environment variables.
