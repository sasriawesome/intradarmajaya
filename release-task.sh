#!/usr/bin/env bash
python manage.py migrate
python manage.py migrate lectures zero
python manage.py migrate students zero
python manage.py migrate teachers zero
python manage.py migrate academic zero
python manage.py collectstatic --noinput