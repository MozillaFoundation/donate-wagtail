import json

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

    def test_get_initial_currency_uses_header(self):
        request = RequestFactory().get('/', HTTP_ACCEPT_LANGUAGE='es-CL;q=0.9')
        self.assertEqual(
            DonationPage().get_initial_currency(request),
            'clp'
        )

    def test_serve_sets_subscribed_cookie(self):
        request = RequestFactory().get('/?subscribed=1')
        response = DonationPage().serve(request)
        self.assertEqual(response.cookies['subscribed'].value, '1')

    def test_serve_doesnt_set_subscribed_cookie_if_invalid_query_arg(self):
        request = RequestFactory().get('/?subscribed=foo')
        response = DonationPage().serve(request)
        self.assertNotIn('subscribed', response.cookies)


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
