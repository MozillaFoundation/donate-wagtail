from django.core.management.base import BaseCommand

from wagtail_localize.models import Language, Locale


class Command(BaseCommand):
    help = 'Deletes all pages that are not in the default locale'

    def handle(self, *args, **options):
        default_locale = Locale.objects.default()

        # Delete all pages except for ones in the default locale
        for locale in Locale.objects.exclude(id=default_locale.id):
            locale.get_all_pages().delete()

        # Delete all languages that no longer have any pages
        Language.objects.exclude(id=default_locale.language_id).delete()
