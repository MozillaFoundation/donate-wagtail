"""
Management command called during the Heroku Review App post-deployment phase.
Creates an admin user and prints the password to the build logs.
"""
from factory import Faker
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser for use on Heroku review apps'

    def handle(self, *args, **options):
        try:
            User.objects.get(username='admin')
            self.stdout.write('Superuser already exists')
        except User.DoesNotExist:
            password = Faker(
                'password',
                length=16,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True
            ).generate({})
            User.objects.create_superuser('admin', 'admin@example.com', password)
            self.stdout.write(f'Created superuser with username admin and password {password}')
