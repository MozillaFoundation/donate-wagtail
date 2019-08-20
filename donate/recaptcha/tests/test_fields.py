from unittest import mock

from django.core.exceptions import ValidationError
from django.test import TestCase

from ..fields import ReCaptchaField


class RecaptchaFieldTestCase(TestCase):

    def test_validation_error_if_token_not_valid(self):
        with mock.patch('donate.recaptcha.fields.verify', autospec=True) as mock_verify:
            mock_verify.return_value = False
            with self.assertRaises(ValidationError):
                ReCaptchaField().validate('foo')

    def test_validation_ok_if_token_valid(self):
        with mock.patch('donate.recaptcha.fields.verify', autospec=True) as mock_verify:
            mock_verify.return_value = True
            self.assertIsNone(ReCaptchaField().validate('foo'))
