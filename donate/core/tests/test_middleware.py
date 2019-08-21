from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.utils import translation

from ..middleware import LocaleMiddleware


class LocaleMiddlewareTestCase(TestCase):

    def test_process_request_sets_iso_3166_language_code(self):
        request = RequestFactory().get('/en-GB/')
        LocaleMiddleware().process_request(request)
        self.assertEqual(request.LANGUAGE_CODE, 'en-gb')

    def test_process_response_redirects_to_iso_3166_language_code(self):
        request = RequestFactory().get('/')
        response = HttpResponse(status=404)
        translation.activate('en-gb')
        new_response = LocaleMiddleware().process_response(request, response)
        self.assertEqual(new_response.status_code, 302)
        self.assertEqual(new_response['Location'], '/en-GB/')
