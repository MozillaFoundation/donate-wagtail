from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, ObjectList
from wagtail.contrib.settings.models import BaseSetting, register_setting

@register_setting(icon='tick')
class FeatureFlags(BaseSetting):

    enable_upsell_view = models.BooleanField(
        default=False,
        verbose_name='Enable the upsell view',
        help_text='Checking this will allow the upsell view to be displayed after one-time donations',
    )

    content_panels = [
        FieldPanel('enable_upsell_view')
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Feature Flags"),
    ])
