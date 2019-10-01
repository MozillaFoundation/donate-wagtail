#!/usr/bin/env bash

# Django Migrations
python manage.py migrate --no-input
<<<<<<< HEAD
=======
PATH=$PATH:/app/bin/
echo $PATH
ls /app/bin
>>>>>>> debug time \o/
python manage.py compilemessages
