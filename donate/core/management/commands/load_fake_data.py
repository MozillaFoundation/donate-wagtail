import factory
import random

from django.core.management.base import BaseCommand
from django.conf import settings

import donate.core.factory as core_factory
from donate.utility.faker.helpers import reseed

from wagtail_factories import ImageFactory


class Command(BaseCommand):
    help = 'Generate fake data for local development and testing purposes' \
           'and load it into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--seed',
            action='store',
            dest='seed',
            help='A seed value to pass to Faker before generating data',
        )

    def handle(self, *args, **options):

        faker = factory.faker.Faker._get_faker(locale='en-US')

        # Seed Faker with the provided seed value or a pseudorandom int between 0 and five million
        if options['seed']:
            seed = options['seed']
        elif settings.RANDOM_SEED is not None:
            seed = settings.RANDOM_SEED
        else:
            seed = random.randint(0, 5000000)

        self.stdout.write(f'Seeding random numbers with: {seed}')

        reseed(seed)

        self.stdout.write('Generating Images')
        for i in range(20):
            ImageFactory.create(
                file__width=1080,
                file__height=720,
                file__color=faker.safe_color_name()
            )

        factories = [
            core_factory,
        ]
        for app_factory in factories:
            app_factory.generate(seed)

        self.stdout.write(self.style.SUCCESS('Done!'))
