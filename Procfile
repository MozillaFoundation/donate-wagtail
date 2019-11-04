release: ./release-steps.sh
web: cd donate && gunicorn donate.wsgi:application
worker: python manage.py rqworker default wagtail_localize_pontoon.sync
