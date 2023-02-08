#!/usr/bin/env bash

# migrations
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input

gunicorn mysite.wsgi -w 16 -b 0.0.0.0:8000 --reload --log-level info -t 120
#gunicorn mysite.wsgi --workers 16