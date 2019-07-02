#!/usr/bin/env bash

cd donate

# Django Migrations
python manage.py migrate --no-input
