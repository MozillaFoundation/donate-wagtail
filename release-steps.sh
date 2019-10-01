#!/usr/bin/env bash

# Django Migrations
python manage.py migrate --no-input

PATH=$BUILD_DIR/gettext/bin:$PATH

echo $PATH
ls -la

#python manage.py compilemessages
