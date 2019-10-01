#!/usr/bin/env bash

# Django Migrations
python manage.py migrate --no-input
python manage.py compilemessages
