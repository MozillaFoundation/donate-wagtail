from django.conf import settings
from factory import Faker, SubFactory
from wagtail_factories import ImageFactory, PageFactory
from wagtail.core.models import Page, Site

from donate.core.models import CampaignPage, LandingPage
from donate.utility.faker.helpers import reseed


if settings.HEROKU_APP_NAME:
    REVIEW_APP_NAME = settings.HEROKU_APP_NAME
    REVIEW_APP_HOSTNAME = f'{REVIEW_APP_NAME}.herokuapp.com'


class LandingPageFactory(PageFactory):
    class Meta:
        model = LandingPage

    title = Faker('text', max_nb_chars=140)
    campaign_id = Faker('text', max_nb_chars=140)
    project = 'mozillafoundation'
    intro = Faker('paragraph', nb_sentences=5, variable_nb_sentences=True)
    featured_image = SubFactory(ImageFactory)


class CampaignPageFactory(PageFactory):
    class Meta:
        model = CampaignPage

    title = Faker('text', max_nb_chars=140)
    lead_text = Faker('paragraph', nb_sentences=2, variable_nb_sentences=True)
    intro = Faker('paragraph', nb_sentences=5, variable_nb_sentences=True)
    hero_image = SubFactory(ImageFactory)


def generate(seed):
    reseed(seed)

    try:
        landing_page = LandingPage.objects.get()
        print('Landing page already exists')
    except LandingPage.DoesNotExist:
        print('Generating a landing page')
        site_root = Page.objects.first()
        landing_page = LandingPageFactory.create(
            parent=site_root,
            title='Donate today',
            slug='landing',
        )

    reseed(seed)

    try:
        CampaignPage.objects.get()
        print('Campaign page already exists')
    except CampaignPage.DoesNotExist:
        print('Generating a campaign page')
        CampaignPageFactory.create(
            parent=landing_page,
            title='It\'s Pi Day!',
            slug='campaign',
        )

    reseed(seed)

    try:
        default_site = Site.objects.get(is_default_site=True)
        if settings.HEROKU_APP_NAME:
            default_site.hostname = REVIEW_APP_HOSTNAME
        default_site.root_page = landing_page
        default_site.save()
        print('Updated the default Site')
    except Site.DoesNotExist:
        print('Generating a default Site')
        if settings.HEROKU_APP_NAME:
            hostname = REVIEW_APP_HOSTNAME
            port = 80
        else:
            hostname = 'localhost'
            port = 8000

        Site.objects.create(
            hostname=hostname,
            port=port,
            root_page=landing_page,
            site_name='Donate',
            is_default_site=True
        )
