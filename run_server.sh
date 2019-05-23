#!/usr/bin/env bash

appPATH="$(pwd)"
pythonENV="$appPATH/venv/"
source $pythonENV/bin/activate

cd django-server/nosalty
python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py runserver