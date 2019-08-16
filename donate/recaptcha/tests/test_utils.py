from unittest import mock

from django.test import TestCase

from requests.exceptions import RequestException

from ..utils import verify


class RecaptchaVerifyTestCase(TestCase):

    def test_verify_successful(self):
        with mock.patch('donate.recaptcha.utils.requests', autospec=True) as mock_requests:
            mock_requests.post.return_value.json.return_value = {
                'success': True
            }
            self.assertTrue(verify('a-token'))

    def test_verify_unsuccessful(self):
        with mock.patch('donate.recaptcha.utils.requests', autospec=True) as mock_requests:
            mock_requests.post.return_value.json.return_value = {
                'success': False
            }
            self.assertFalse(verify('a-token'))

    def test_verify_returns_true_if_request_failed(self):
        with mock.patch('donate.recaptcha.utils.requests', autospec=True) as mock_requests:
            mock_requests.post.side_effect = RequestException()
            self.assertTrue(verify('a-token'))
