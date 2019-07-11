from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.core.blocks import DecimalBlock, StreamBlock
from wagtail.core.fields import RichTextField, StreamField
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


class AmountBlock(StreamBlock):
    amount = DecimalBlock(min_value=0, max_digits=7, decimal_places=2)

    class Meta:
        icon = 'cogs'
        max_num = 6


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

    single_options = StreamField(AmountBlock())
    monthly_options = StreamField(AmountBlock())

    panels = [
        FieldPanel('currency'),
        StreamFieldPanel('single_options'),
        StreamFieldPanel('monthly_options'),
    ]

    class Meta:
        unique_together = (('campaign', 'currency'),)
