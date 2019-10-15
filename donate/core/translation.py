from django.utils.translation import gettext_lazy as _

"""
A series of strings that are used by Django core, that we want to be able
to provide translations for in the languages we support.

Declaring strings here will ensure that they are included in our translation
files, and used in preference to Django's.
"""

# Field.default_error_messages['required']
default_required_message = _('This field is required.')

# DecimalField.default_error_messages['invalid']
decimal_invalid = _('Enter a number.')

# EmailValidator.message
email_validator_message = _('Enter a valid email address.')
