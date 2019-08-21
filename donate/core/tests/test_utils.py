from django.test import RequestFactory, TestCase
from django.utils import translation

from ..utils import ISO3166LocalePrefixPattern, get_language_from_request, language_code_to_iso_3166


class UtilsTestCase(TestCase):

    def test_get_language_code_to_iso_3166(self):
        self.assertEqual(language_code_to_iso_3166('en-gb'), 'en-GB')
        self.assertEqual(language_code_to_iso_3166('en-us'), 'en-US')
        self.assertEqual(language_code_to_iso_3166('fr'), 'fr')

    def test_ISO3166LocalePrefixPattern(self):
        translation.deactivate()
        pattern = ISO3166LocalePrefixPattern(prefix_default_language=True)
        # Pattern should not match lowercase URLs
        self.assertIsNone(pattern.match('en-us/'))
        # It should match this URL
        self.assertTrue(pattern.match('en-US/'))

    def test_get_language_from_request_returns_iso_3166_language(self):
        request = RequestFactory().get('/')
        request.META['HTTP_ACCEPT_LANGUAGE'] = 'en-GB,en;q=0.5'
        language = get_language_from_request(request)
        self.assertEqual(language, 'en-GB')

    def test_get_language_from_request_fallback_language(self):
        request = RequestFactory().get('/')
        request.META['HTTP_ACCEPT_LANGUAGE'] = 'en-FO,en;q=0.5'
        language = get_language_from_request(request)
        self.assertEqual(language, 'en-US')
