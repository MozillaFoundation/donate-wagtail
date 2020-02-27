from decimal import Decimal
import json
from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, RequestFactory

from wagtail.core.models import Page

from ..factory.core_pages import CampaignPageFactory, LandingPageFactory
from ..models import CampaignPageDonationAmount, DonationPage


class DonationPageTestCase(TestCase):

    def test_get_initial_currency_uses_currency_arg(self):
        request = RequestFactory().get('/?currency=gbp')
        self.assertEqual(
            DonationPage().get_initial_currency(request),
            'gbp'
        )

    def test_get_initial_currency_uses_locale(self):
        request = RequestFactory().get('/')
        request.LANGUAGE_CODE = 'es-MX'
        self.assertEqual(
            DonationPage().get_initial_currency(request),
            'mxn'
        )

    def test_serve_sets_subscribed_cookie(self):
        request = RequestFactory().get('/?subscribed=1')
        site_root = Page.objects.first()
        page = LandingPageFactory.create(
            parent=site_root,
            title='Donate today',
            slug='landing',
        )
        response = page.serve(request)
        self.assertEqual(response.cookies['subscribed'].value, '1')

    def test_serve_doesnt_set_subscribed_cookie_if_invalid_query_arg(self):
        request = RequestFactory().get('/?subscribed=foo')
        site_root = Page.objects.first()
        page = LandingPageFactory.create(
            parent=site_root,
            title='Donate today',
            slug='landing',
        )
        response = page.serve(request)
        self.assertNotIn('subscribed', response.cookies)

    def test_get_context(self):
        request = RequestFactory().get('/')
        site_root = Page.objects.first()
        page = LandingPageFactory.create(
            parent=site_root,
            title='Donate today',
            slug='landing',
            project='mozillafoundation',
            campaign_id='pi_day',
        )
        ctx = page.get_context(request)

        self.assertEqual(ctx['currencies'], page.currencies)
        self.assertEqual(ctx['initial_currency_info'], page.currencies['usd'])
        self.assertEqual(ctx['braintree_params'], settings.BRAINTREE_PARAMS)
        self.assertEqual(ctx['braintree_form'].initial, {
            'landing_url': request.build_absolute_uri(),
            'project': page.project,
            'campaign_id': page.campaign_id,
        })


class CampaignPageTestCase(TestCase):

    def setUp(self):
        site_root = Page.objects.first()
        landing_page = LandingPageFactory.create(
            parent=site_root,
            title='Donate today',
            slug='landing',
        )
        self.campaign_page = CampaignPageFactory.create(
            parent=landing_page,
            title='It\'s Pi Day!',
            slug='campaign',
        )

    def test_get_currencies_applies_overrides(self):
        # Add an override
        CampaignPageDonationAmount.objects.create(
            campaign=self.campaign_page,
            currency='usd',
            single_options=json.dumps([
                {'type': 'amount', 'value': '5'},
                {'type': 'amount', 'value': '2'},
            ]),
            monthly_options=json.dumps([
                {'type': 'amount', 'value': '15'},
                {'type': 'amount', 'value': '12'},
            ])
        )
        currencies = self.campaign_page.currencies
        self.assertEqual(currencies['usd']['presets'], {
            'single': [5, 2],
            'monthly': [15, 12],
        })

    def test_initial_currency_context_includes_overrides(self):
        CampaignPageDonationAmount.objects.create(
            campaign=self.campaign_page,
            currency='usd',
            single_options=json.dumps([
                {'type': 'amount', 'value': '5'},
                {'type': 'amount', 'value': '2'},
            ]),
            monthly_options=json.dumps([
                {'type': 'amount', 'value': '15'},
                {'type': 'amount', 'value': '12'},
            ])
        )
        request = RequestFactory().get('/?currency=usd')
        ctx = self.campaign_page.get_context(request)
        self.assertEqual(
            ctx['initial_currency_info']['presets']['single'],
            [Decimal(5), Decimal(2)]
        )
        self.assertEqual(
            ctx['initial_currency_info']['presets']['monthly'],
            [Decimal(15), Decimal(12)]
        )

    def test_get_initial_frequency_uses_arg(self):
        request = RequestFactory().get('/?frequency=monthly')
        self.assertEqual(
            DonationPage().get_initial_frequency(request),
            'monthly'
        )

    def test_get_initial_frequency_ignores_invalid_value(self):
        request = RequestFactory().get('/?frequency=bogus')
        self.assertEqual(
            DonationPage().get_initial_frequency(request),
            'single'
        )

    def test_get_initial_currency_info_uses_arg_and_sorts(self):
        request = RequestFactory().get('/?presets=1,9,5,3')
        self.assertEqual(
            DonationPage().get_initial_currency_info(request, 'usd', 'single')['presets']['single'],
            [Decimal(9), Decimal(5), Decimal(3), Decimal(1)]
        )

    def test_get_initial_currency_info_skips_if_invalid_params_present(self):
        request = RequestFactory().get('/?presets=1,9,5,3,foo')
        self.assertEqual(
            DonationPage().get_initial_currency_info(request, 'usd', 'single')['presets']['single'],
            DonationPage().currencies['usd']['presets']['single']
        )

    def test_get_initial_currency_info_limits_to_four_shoices(self):
        request = RequestFactory().get('/?presets=1,9,5,3,7,3')
        self.assertEqual(
            DonationPage().get_initial_currency_info(request, 'usd', 'single')['presets']['single'],
            [Decimal(9), Decimal(7), Decimal(5), Decimal(3)]
        )


class MissingMigrationsTests(TestCase):

    def test_no_migrations_missing(self):
        """
        Ensure we didn't forget a migration
        """
        output = StringIO()
        call_command('makemigrations', interactive=False, dry_run=True, stdout=output)

        if output.getvalue() != "No changes detected\n":
            raise AssertionError("Missing migrations detected:\n" + output.getvalue())
