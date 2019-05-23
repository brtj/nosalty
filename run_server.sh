#!/usr/bin/env bash

appPATH="$(pwd)"
pythonENV="$appPATH/venv/"
source $pythonENV/bin/activate

cd django-server/nosalty
python manage.py runserver