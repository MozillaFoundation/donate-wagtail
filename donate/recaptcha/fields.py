from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .utils import verify


class ReCaptchaField(forms.CharField):
    widget = forms.HiddenInput

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.required = True
        self.recaptcha_secret = kwargs.get('secret', '')

    def validate(self, value):
        super().validate(value)
        if not verify(value, self.recaptcha_secret):
            raise ValidationError(_("Captcha was invalid. Please try again."))
