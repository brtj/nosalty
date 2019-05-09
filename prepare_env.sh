#!/bin/bash

appPATH="$(pwd)"
pythonENV="$appPATH/venv/"
djangoPATH="$appPATH/django-server/nosalty/"

echo 'Creating virtualenv'
python3 -m venv venv
source $pythonENV/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

cd $djangoPATH
python manage.py makemigrations
python manage.py migrate --run-syncdb

