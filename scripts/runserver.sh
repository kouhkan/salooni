#!/bin/sh
cd /code
su  -c "python manage.py collectstatic --no-input && python manage.py makemigrations && python manage.py migrate && gunicorn --workers=3 myblog.wsgi -b 0.0.0.0:8080"