#!/usr/bin/env bash

# Django Migrations
python manage.py migrate --no-input

echo $PATH
ls -la

python manage.py compilemessages
