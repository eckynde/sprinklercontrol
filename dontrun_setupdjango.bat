cd server
py manage.py makemigrations
py manage.py migrate
py manage.py initialize

set DJANGO_SUPERUSER_PASSWORD=book
py manage.py createsuperuser --noinput
py manage.py runserver
