#!/bin/sh

python manage.py migrate

exec gunicorn too_good_to_blame.wsgi:application --bind 0.0.0.0:8000
