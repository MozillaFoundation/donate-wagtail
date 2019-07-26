from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.core.blocks import DecimalBlock, StreamBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from modelcluster.fields import ParentalKey

from donate.payments import constants
from donate.payments.forms import BraintreePaypalPaymentForm, CurrencyForm
from donate.payments.utils import get_default_currency


class DonationPage(Page):

    @cached_property
    def currencies(self):
        return constants.CURRENCIES.copy()

    def get_initial_currency(self, request):
        # Query argument takes first preference
        if request.GET.get('currency') in constants.CURRENCIES:
            return request.GET['currency']
        # Otherwise sniff based on browser language
        return get_default_currency(request.META['HTTP_ACCEPT_LANGUAGE'])

    def get_context(self, request):
        ctx = super().get_context(request)
        ctx.update({
            'currencies': self.currencies,
            'braintree_params': settings.BRAINTREE_PARAMS,
            'braintree_form': BraintreePaypalPaymentForm(),
            'currency_form': CurrencyForm(initial={'currency': self.get_initial_currency(request)}),
        })
        return ctx

    class Meta:
        abstract = True


class LandingPage(DonationPage):
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


class CampaignPage(DonationPage):
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

    @classmethod
    def amount_stream_to_list(cls, stream):
        return [Decimal(child.value) for child in stream]

    @classmethod
    def get_presets(cls, override):
        return {
            'single': cls.amount_stream_to_list(override.single_options),
            'monthly': cls.amount_stream_to_list(override.monthly_options),
        }

    @cached_property
    def currencies(self):
        currencies = super().currencies
        # Apply overrides for preset options
        for override in self.donation_amounts.all():
            currencies[override.currency]['presets'] = self.get_presets(override)
        return currencies


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
