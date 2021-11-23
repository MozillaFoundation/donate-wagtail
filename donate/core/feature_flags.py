from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, ObjectList
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting(icon='tick')
class FeatureFlags(BaseSetting):

    enable_paypal = models.BooleanField(
        default=False,
        verbose_name='Enable the PayPal button on the donate form',
    )

    enable_recaptcha = models.BooleanField(
        default=True,
        verbose_name='Enable recaptcha across the site',
    )

    use_checkbox_recaptcha = models.BooleanField(
        default=True,
        verbose_name='Use a checkbox recaptcha on the CC donate form',
    )

    content_panels = [
        FieldPanel('enable_paypal'),
        FieldPanel('enable_recaptcha'),
        FieldPanel('use_checkbox_recaptcha'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Feature Flags"),
    ])
