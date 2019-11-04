release: ./release-steps.sh
web: cd donate && gunicorn donate.wsgi:application
worker: ./ssh_configuration.sh && python manage.py rqworker default wagtail_localize_pontoon.sync
