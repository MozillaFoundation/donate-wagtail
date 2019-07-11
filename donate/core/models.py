from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel


class LandingPage(Page):
    template = 'pages/core/landing_page.html'

    # Only allow creating landing pages at the root level
    parent_page_types = ['wagtailcore.Page']

    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        models.PROTECT,
        related_name='+',
    )
    intro = RichTextField()

    content_panels = Page.content_panels + [
        ImageChooserPanel('featured_image'),
        FieldPanel('intro'),
    ]
