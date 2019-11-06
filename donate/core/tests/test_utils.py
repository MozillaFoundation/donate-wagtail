from django.utils import translation
from django.utils.translation.trans_real import (
    to_language as django_to_language,
    parse_accept_lang_header as django_parse_accept_lang_header
)
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .. import language_code_to_iso_3166, parse_accept_lang_header, to_language
from ..utils import queue_ga_event


class UtilsTestCase(TestCase):

    def test_get_language_code_to_iso_3166(self):
        self.assertEqual(language_code_to_iso_3166('en-gb'), 'en-GB')
        self.assertEqual(language_code_to_iso_3166('en-us'), 'en-US')
        self.assertEqual(language_code_to_iso_3166('fr'), 'fr')

    def test_to_language(self):
        self.assertEqual(to_language('en_US'), 'en-US')

    def test_parse_accept_lang_header_returns_iso_3166_language(self):
        self.assertEqual(
            parse_accept_lang_header('en-GB,en;q=0.5'),
            (('en-GB', 1.0), ('en', 0.5)),
        )

    def test_queue_ga_event_new(self):
        request = RequestFactory().get('/')
        request.session = self.client.session
        queue_ga_event(request, ['send', 'event', 'foo'])
        self.assertEqual(request.session['ga_events'], [['send', 'event', 'foo']])

    def test_queue_ga_event_append(self):
        request = RequestFactory().get('/')
        request.session = self.client.session
        request.session['ga_events'] = [['send', 'event', 'foo']]
        queue_ga_event(request, ['send', 'event', 'bar'])
        self.assertEqual(request.session['ga_events'], [['send', 'event', 'foo'], ['send', 'event', 'bar']])
        self.assertTrue(request.session.modified)


class UtilsIntegrationTestCase(TestCase):

    """
    Test that our overrides to Django translation functions work.
    """
    def test_to_language(self):
        self.assertEqual(django_to_language('en_US'), 'en-US')

    def test_parse_accept_lang_header_returns_iso_3166_language(self):
        self.assertEqual(
            django_parse_accept_lang_header('en-GB,en;q=0.5'),
            (('en-GB', 1.0), ('en', 0.5)),
        )

    def test_reverse_produces_correct_url_prefix(self):
        translation.activate('en-GB')
        url = reverse('payments:completed')
        self.assertTrue(url.startswith('/en-GB/'))
        translation.deactivate()
