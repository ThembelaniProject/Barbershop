# The Gents' Corner — Django Barber Shop

Full-stack Django barber shop website with database-backed services, barbers and bookings, responsive UI, Google Calendar integration and downloadable Apple Calendar-compatible ICS events.

## Local setup

python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_shop
python manage.py runserver
