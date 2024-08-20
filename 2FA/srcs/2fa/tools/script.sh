#!/bin/bash

cd /2fa

python manage.py makemigrations
sleep 5
python manage.py migrate
python manage.py runserver 0.0.0.0:8003