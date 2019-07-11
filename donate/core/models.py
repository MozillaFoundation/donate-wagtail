from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, InlinePanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from modelcluster.fields import ParentalKey

from . import constants


class LandingPage(Page):
    template = 'pages/core/landing_page.html'

    # Only allow creating landing pages at the root level
    parent_page_types = ['wagtailcore.Page']
    subpage_types = ['core.CampaignPage']

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


class CampaignPage(Page):
    template = 'pages/core/campaign_page.html'
    parent_page_types = ['core.LandingPage']

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        models.PROTECT,
        related_name='+',
    )
    lead_text = models.CharField(max_length=800)

    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image'),
        FieldPanel('lead_text'),
        InlinePanel('donation_amounts', label='Donation amount overrides'),
    ]


class CampaignPageDonationAmount(models.Model):
    campaign = ParentalKey(
        'core.CampaignPage',
        on_delete=models.CASCADE,
        related_name='donation_amounts',
    )
    currency = models.CharField(
        max_length=3,
        choices=constants.CURRENCY_CHOICES,
        blank=False,
        db_index=True,
    )

    # Define 4 fields each for single and monthly preset amounts
    preset_kwargs = {'max_digits': 7, 'decimal_places': 2}
    single_1 = models.DecimalField(**preset_kwargs)
    single_2 = models.DecimalField(**preset_kwargs)
    single_3 = models.DecimalField(**preset_kwargs)
    single_4 = models.DecimalField(**preset_kwargs)
    monthly_1 = models.DecimalField(**preset_kwargs)
    monthly_2 = models.DecimalField(**preset_kwargs)
    monthly_3 = models.DecimalField(**preset_kwargs)
    monthly_4 = models.DecimalField(**preset_kwargs)

    panels = [
        FieldPanel('currency'),
        FieldRowPanel([
            FieldPanel('single_1'),
            FieldPanel('single_2'),
        ]),
        FieldRowPanel([
            FieldPanel('single_3'),
            FieldPanel('single_4'),
        ]),
        FieldRowPanel([
            FieldPanel('monthly_1'),
            FieldPanel('monthly_2'),
        ]),
        FieldRowPanel([
            FieldPanel('monthly_3'),
            FieldPanel('monthly_4'),
        ]),
    ]

    class Meta:
        unique_together = (('campaign', 'currency'),)
