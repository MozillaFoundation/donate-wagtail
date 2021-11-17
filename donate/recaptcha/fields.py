from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .utils import verify


class ReCaptchaField(forms.CharField):
    widget = forms.HiddenInput

    def __init__(self):
        super().__init__()
        self.required = True

    def validate(self, value):
        if not verify(value):
            raise ValidationError(_("Captcha was invalid. Please try again."))
