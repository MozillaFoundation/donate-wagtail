from copy import deepcopy
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.core.blocks import DecimalBlock, StreamBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from modelcluster.fields import ParentalKey
from wagtail_localize.fields import SynchronizedField

from donate.payments import constants
from donate.payments.forms import BraintreePaypalPaymentForm, CurrencyForm
from donate.payments.utils import get_default_currency

from .blocks import ContentBlock


class DonationPage(Page):

    PROJECT_MOZILLAFOUNDATION = 'mozillafoundation'
    PROJECT_THUNDERBIRD = 'thunderbird'
    PROJECT_CHOICES = (
        (PROJECT_MOZILLAFOUNDATION, 'Mozilla Foundation'),
        (PROJECT_THUNDERBIRD, 'Thunderbird'),
    )

    project = models.CharField(
        max_length=25,
        choices=PROJECT_CHOICES,
        default=PROJECT_MOZILLAFOUNDATION,
        help_text='The project that donations from this campaign should be associated with'
    )
    campaign_id = models.CharField(
        max_length=255,
        blank=True,
        help_text='Used for analytics and reporting'
    )

    settings_panels = Page.settings_panels + [
        FieldPanel('campaign_id'),
    ]

    override_translatable_fields = [
        SynchronizedField('slug'),
        SynchronizedField('campaign_id'),
    ]

    @cached_property
    def currencies(self):
        currencies = deepcopy(constants.CURRENCIES)
        # Re-order currency `single` and `monthly` amounts
        for currency in currencies:
            currencies[currency]['presets']['single'].sort()
            currencies[currency]['presets']['monthly'].sort()
        return currencies

    def get_initial_currency(self, request):
        # Query argument takes first preference
        if request.GET.get('currency') in constants.CURRENCIES:
            return request.GET['currency']

        # Otherwise use the language code determined by Django
        return get_default_currency(getattr(request, 'LANGUAGE_CODE', ''))

    def serve(self, request, *args, **kwargs):
        response = super().serve(request, *args, **kwargs)
        if request.GET.get('subscribed') == '1':
            # Set a cookie that expires at the end of the session
            response.set_cookie('subscribed', '1', httponly=True)
        return response

    def get_initial_frequency(self, request):
        frequency = request.GET.get('frequency', '')
        return frequency if frequency in dict(constants.FREQUENCY_CHOICES) else constants.FREQUENCY_SINGLE

    def get_initial_currency_info(self, request, initial_currency, initial_frequency):
        initial_currency_info = self.currencies[initial_currency]

        # Check if presets have been specified in a query arg
        custom_presets = request.GET.get('presets', '').split(',')
        try:
            min_amount = initial_currency_info.get('minAmount', 0)
            custom_presets = [
                amount for amount in
                [
                    Decimal(value).quantize(Decimal('0.01'))
                    if float(value) >= min_amount else None
                    for value in custom_presets
                ]
                if amount
            ]
        except (InvalidOperation, ValueError):
            return initial_currency_info

        if not custom_presets:
            return initial_currency_info

        if len(custom_presets) < 4:
            return initial_currency_info

        sorting = request.GET.get('sort', False)

        if sorting == 'reverse':
            custom_presets.sort(reverse=True)

        initial_currency_info['presets'][initial_frequency] = custom_presets[:4]
        return initial_currency_info

    def default_initial_amount(self, initial_currency_info, initial_frequency):
        """
        The default donation amount is the second lowest amount in the list of amounts.
        """
        return sorted(initial_currency_info['presets'][initial_frequency])[1]

    def get_initial_amount(self, request, initial_currency_info, initial_frequency):
        """
        When called with ?amount=..., that value will be preselected if:

        1. it's a real number, and
        2. that number can be found in the current list of possibles values.

        If not, the default initial amount is used
        """
        amount = request.GET.get('amount', False)

        if amount is False or 'e' in amount:
            return self.default_initial_amount(initial_currency_info, initial_frequency)

        try:
            value = Decimal(amount).quantize(Decimal('0.01'))
        except InvalidOperation:
            return self.default_initial_amount(initial_currency_info, initial_frequency)

        if value in initial_currency_info['presets'][initial_frequency]:
            return value

        return self.default_initial_amount(initial_currency_info, initial_frequency)

    def get_initial_values(self, request):
        frequency = self.get_initial_frequency(request)
        currency = self.get_initial_currency(request)
        currency_info = self.get_initial_currency_info(request, currency, frequency)
        amount = self.get_initial_amount(request, currency_info, frequency)

        return {
            "frequency": frequency,
            "currency": currency,
            "currency_info": currency_info,
            "amount": amount,
        }

    def get_context(self, request):
        ctx = super().get_context(request)
        values = self.get_initial_values(request)
        ctx.update({
            'currencies': self.currencies,
            'initial_currency_info': values['currency_info'],
            'initial_frequency': values['frequency'],
            'initial_amount': values['amount'],
            'braintree_params': settings.BRAINTREE_PARAMS,
            'braintree_form': BraintreePaypalPaymentForm(
                initial={
                    'landing_url': request.build_absolute_uri(),
                    'project': self.project,
                    'campaign_id': self.campaign_id,
                }
            ),
            'currency_form': CurrencyForm(initial={'currency': values['currency']}),
            'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY if settings.RECAPTCHA_ENABLED else None,
        })
        return ctx

    class Meta:
        abstract = True


class LandingPage(DonationPage):
    template = 'pages/core/landing_page.html'

    # Only allow creating landing pages at the root level
    parent_page_types = ['wagtailcore.Page']

    subpage_types = [
        'core.CampaignPage',
        'core.ContentPage',
        'core.ContributorSupportPage',
    ]

    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        models.PROTECT,
        related_name='+',
    )
    intro = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('project'),
        ImageChooserPanel('featured_image'),
        FieldPanel('intro'),
    ]


class CampaignPage(DonationPage):
    template = 'pages/core/campaign_page.html'
    parent_page_types = ['core.LandingPage', 'core.CampaignPage']
    subpage_types = ['core.CampaignPage']

    submit_to_pontoon_on_publish = False

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        models.PROTECT,
        related_name='+',
    )
    lead_text = models.CharField(max_length=800)
    intro = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('project'),
        ImageChooserPanel('hero_image'),
        FieldPanel('lead_text'),
        FieldPanel('intro'),
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


class ContentPage(Page):
    template = 'pages/core/content_page.html'
    parent_page_types = ['core.LandingPage']
    subpage_types = ['core.ContentPage']

    call_to_action_text = models.CharField(max_length=255, blank=True)
    call_to_action_url = models.URLField(blank=True)

    body = StreamField(ContentBlock)

    content_panels = Page.content_panels + [
        FieldPanel('call_to_action_text'),
        FieldPanel('call_to_action_url'),
        StreamFieldPanel('body'),
    ]

    override_translatable_fields = [
        SynchronizedField('slug'),
    ]


class ContributorSupportPage(Page):
    template = 'pages/core/contributor_support_page.html'
    parent_page_types = ['core.LandingPage']

    override_translatable_fields = [
        SynchronizedField('slug'),
    ]

    # This page does not have subpages

    def get_context(self, request):
        ctx = super().get_context(request)
        ctx.update({
            'orgid': settings.SALESFORCE_ORGID,
            'record_type_id': settings.SALESFORCE_CASE_RECORD_TYPE_ID,
        })
        return ctx
