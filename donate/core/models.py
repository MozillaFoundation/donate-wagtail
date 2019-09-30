from copy import deepcopy
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
from wagtail_localize.models import TranslatablePageMixin, TranslatablePageRoutingMixin, Locale

from donate.payments import constants
from donate.payments.forms import BraintreePaypalPaymentForm, CurrencyForm
from donate.payments.utils import get_default_currency

from .blocks import ContentBlock


class DonationPage(TranslatablePageMixin, Page):

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

    @cached_property
    def currencies(self):
        return deepcopy(constants.CURRENCIES)

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

    def get_context(self, request):
        ctx = super().get_context(request)
        initial_currency = self.get_initial_currency(request)
        ctx.update({
            'currencies': self.currencies,
            'initial_currency_info': self.currencies[initial_currency],
            'braintree_params': settings.BRAINTREE_PARAMS,
            'braintree_form': BraintreePaypalPaymentForm(
                initial={
                    'source_page_id': self.pk,
                    'landing_url': request.build_absolute_uri(),
                    'project': self.project,
                    'campaign_id': self.campaign_id,
                }
            ),
            'currency_form': CurrencyForm(initial={'currency': initial_currency}),
            'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY if settings.RECAPTCHA_ENABLED else None,
        })
        return ctx

    @classmethod
    def can_create_at(cls, parent):
        if not super().can_create_at(parent):
            return False

        # Prevent pages being created in translated sections
        if issubclass(parent.specific_class, TranslatablePageMixin):
            if parent.specific.locale_id != Locale.objects.default_id():
                return False

        return True

    class Meta:
        unique_together = [
            ('translation_key', 'locale'),
        ]
        abstract = True


class LandingPage(TranslatablePageRoutingMixin, DonationPage):
    template = 'pages/core/landing_page.html'

    # Only allow creating landing pages at the root level
    parent_page_types = ['wagtailcore.Page']
    subpage_types = ['core.CampaignPage', 'core.ContentPage']

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

    translatable_fields = [
        'title',
        'seo_title',
        'search_description',
        'intro',
    ]

    def save(self, *args, **kwargs):
        # This slug isn't used anywhere but it does need to be unique for each language
        language_code = self.locale.language.code.lower()
        if language_code == 'en-us':
            # Needs to be something nice as translators will see it
            self.slug = 'mozilla-donate'
        else:
            self.slug = 'mozilla-donate-' + language_code

        super().save(*args, **kwargs)


class CampaignPage(DonationPage):
    template = 'pages/core/campaign_page.html'
    parent_page_types = ['core.LandingPage']

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

    translatable_fields = [
        'title',
        'slug',
        'seo_title',
        'search_description',
        'lead_text',
        'intro',
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


class ContentPage(TranslatablePageMixin, Page):
    template = 'pages/core/content_page.html'
    parent_page_types = ['LandingPage']
    subpage_types = ['ContentPage']

    call_to_action_text = models.CharField(max_length=255, blank=True)
    call_to_action_url = models.URLField(blank=True)

    body = StreamField(ContentBlock)

    content_panels = Page.content_panels + [
        FieldPanel('call_to_action_text'),
        FieldPanel('call_to_action_url'),
        StreamFieldPanel('body'),
    ]

    translatable_fields = [
        'title',
        'seo_title',
        'search_description',
        'call_to_action_text',
        'body',
    ]
