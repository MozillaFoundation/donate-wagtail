"""
Management command that trigger a sync with Pontoon. Used on Heroku as a scheduled task.
"""
from django.core.management.base import BaseCommand

from donate.core.pontoon import CustomSyncManager


class Command(BaseCommand):
    help = 'Enqueue a `sync_pontoon` job.'

    def handle(self, *args, **options):
        print("Syncing with Pontoon...")
        CustomSyncManager().trigger()
        print("Done!")
