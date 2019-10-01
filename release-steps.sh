#!/usr/bin/env bash

# Django Migrations
python manage.py migrate --no-input

PATH=$HOME/gettext/bin:$PATH

echo $PATH
ls -la

python manage.py compilemessages
