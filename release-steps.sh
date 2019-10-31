#!/usr/bin/env bash

# Django Migrations
python manage.py migrate --no-input

# Configuring ssh key to be able to push content that needs to be translated with Pontoon to a certain repo (`WAGTAILLOCALIZE_PONTOON_GIT_URL` env variable).
echo $SSH_KEY > /app/.ssh/id_rsa
