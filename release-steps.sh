#!/usr/bin/env bash

# Django Migrations
python manage.py migrate --no-input

PATH=$BUILD_DIR/gettext/bin:$PATH python manage.py compilemessages
