from django.core.management.base import BaseCommand

from wagtail.core.models import Page
from wagtail.images.models import Image


class Command(BaseCommand):
    help = 'Delete all Page and Image objects from the database along with associated media files.'

    def handle(self, *args, **options):
        Page.objects.all().delete()
        self.stdout.write('Deleted all pages')
        num_deleted, __ = Image.objects.all().delete()
        self.stdout.write(f'Deleted {num_deleted} images')
