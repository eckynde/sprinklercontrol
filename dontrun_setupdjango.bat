cd server
py manage.py makemigrations
py manage.py migrate
py manage.py initialize

set DJANGO_SUPERUSER_PASSWORD=password
py manage.py createsuperuser --noinput --username admin
