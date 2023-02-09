#!/usr/bin/env bash

# migrations
python manage.py createsuperuser --username management --email gokcekarda@gmail.com --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input

#gunicorn mysite.wsgi -w 16 -b 0.0.0.0:80 --reload --access-logfile - --log-level debug -t 120
gunicorn mysite.wsgi -w 35 -b 0.0.0.0:80 --reload --log-level info -t 120