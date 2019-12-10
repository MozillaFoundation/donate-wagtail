"""Management command running on CI: Send a message on Slack if an error is found while running compilemessages."""

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import requests


class Command(BaseCommand):
    help = 'Send a message to Slack if compilemessages returns an error.'

    def handle(self, *args, **options):
        try:
            call_command("compilemessages", verbosity=1)
        except CommandError as err:
            travis_logs_url = settings.TRAVIS_LOGS_URL
            slack_webhook = settings.SLACK_WEBHOOK_PONTOON

            slack_payload = {
                'attachments': [
                    {
                        'fallback': '<!here> An error occurred while compiling `.po` files for '
                                    'donate-wagtail\n'
                                    f'Error message: ```{err}```\n'
                                    f'URL: {travis_logs_url}',
                        'pretext':  '<!here> An error occurred while compiling `.po` files for '
                                    'donate-wagtail\n',
                        'title':    f'Travis logs\n',
                        'text':     f'Error message: ```{err}```\n',
                        'color':    '#8b0000',
                        'actions': [
                            {
                                'type': 'button',
                                'text': 'View logs',
                                'url': f'{travis_logs_url}'
                            }
                        ]
                    }
                ]
            }

            r = requests.post(f'{slack_webhook}',
                              json=slack_payload,
                              headers={'Content-Type': 'application/json'}
                              )

            # Raise if post request was a 4xx or 5xx
            r.raise_for_status()

            # Raise exception to make travis run fail
            raise err
