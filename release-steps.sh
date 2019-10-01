#!/usr/bin/env bash

# Django Migrations
python manage.py migrate --no-input

PATH=$HOME/gettext/bin:$PATH
LD_LIBRARY_PATH=$HOME/gettext/lib:$LD_LIBRARY_PATH

python manage.py compilemessages
