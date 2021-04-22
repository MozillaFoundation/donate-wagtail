import logging
from urllib import parse
from sentry_sdk.integrations.django import ignore_logger
import requests

from django.conf import settings
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.http import is_safe_url
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django.views.generic import FormView, TemplateView

from braintree import ErrorCodes
from dateutil.relativedelta import relativedelta
from wagtail.core.models import Page
from wagtail_ab_testing.models import AbTest
from wagtail_ab_testing.utils import request_is_trackable

from donate.core.utils import queue_ga_event
from . import constants, gateway
from .exceptions import InvalidAddress
from .forms import (
    BraintreeCardPaymentForm, BraintreePaypalPaymentForm, BraintreePaypalUpsellForm,
    NewsletterSignupForm, StartCardPaymentForm, UpsellForm
)
from .tasks import queue, send_newsletter_subscription_to_basket, send_transaction_to_basket
from .utils import (
    get_currency_info, get_merchant_account_id_for_card, get_merchant_account_id_for_paypal, get_plan_id,
    get_suggested_monthly_upgrade, freeze_transaction_details_for_session
)

ignore_logger(__name__)
logger = logging.getLogger(__name__)
sentry_logger = logging.getLogger(f'{__name__}_sentry')


class BraintreePaymentMixin:
    success_url = reverse_lazy('payments:newsletter_signup')

    def get_custom_fields(self, form):
        return {
            'project': self.request.session.get('project', 'mozillafoundation'),
            'campaign_id': self.request.session.get('campaign_id', ''),
            'landing_url': form.cleaned_data.get('landing_url', ''),
            'locale': self.request.LANGUAGE_CODE,
            'fraud_site_id': settings.FRAUD_SITE_ID,
        }

    def get_transaction_details_for_session(self, result, form, **kwargs):
        raise NotImplementedError()

    def process_braintree_error_result(result, form):
        raise NotImplementedError()

    def save_campaign_parameters_to_session(self, form):
        # These are stored in the session so that they can be used to track upsell transactions as well
        self.request.session['landing_url'] = form.cleaned_data['landing_url']
        self.request.session['campaign_id'] = form.cleaned_data['campaign_id']
        self.request.session['project'] = form.cleaned_data['project']

    def prepare_session_data(self, details):
        data = {
            'locale': self.request.LANGUAGE_CODE,
            'landing_url': self.request.session.get('landing_url', ''),
            'project': self.request.session.get('project', ''),
            'campaign_id': self.request.session.get('campaign_id', ''),
        }
        data.update(details)
        return freeze_transaction_details_for_session(data)

    def set_session_data(self, result, form, **kwargs):
        # Store details of the transaction in a session variable
        details = self.get_transaction_details_for_session(result, form, **kwargs)
        details = self.prepare_session_data(details)
        self.request.session['completed_transaction_details'] = details
        return details

    def handle_successful_transaction(self, result, form, send_data_to_basket=True, **kwargs):
        details = self.set_session_data(result, form, **kwargs)
        if send_data_to_basket:
            queue.enqueue(send_transaction_to_basket, details)
        return HttpResponseRedirect(self.get_success_url())

    def queue_ga_transaction(self, id, currency, amount, name, category):
        queue_ga_event(self.request, [
            'ecommerce:addTransaction', {
                'id': id,
                'revenue': str(amount),
                'currency': currency.upper(),
                'affiliation': self.request.session.get('project', ''),
            }
        ])
        queue_ga_event(self.request, [
            'ecommerce:addItem', {
                'id': id,
                'name': name,
                'sku': name,
                'category': category,
                'price': str(amount),
                'quantity': '1',
            }
        ])
        queue_ga_event(self.request, ['ecommerce:send'])


class CardPaymentView(BraintreePaymentMixin, FormView):
    form_class = BraintreeCardPaymentForm
    template_name = 'payment/card.html'

    def dispatch(self, request, *args, **kwargs):
        if kwargs['frequency'] not in constants.FREQUENCIES:
            raise Http404()
        self.payment_frequency = kwargs['frequency']

        # Ensure that the donation amount, currency and source page are legit
        start_form = StartCardPaymentForm(request.GET)
        if not start_form.is_valid():
            return HttpResponseRedirect('/')

        self.amount = start_form.cleaned_data['amount']
        self.currency = start_form.cleaned_data['currency']
        self.source_page = Page.objects.get(pk=start_form.cleaned_data['source_page_id']).specific
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            'amount': self.amount,
            'landing_url': self.request.META.get('HTTP_REFERER', ''),
            'project': self.source_page.project,
            'campaign_id': self.source_page.campaign_id,
        }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'currency_info': get_currency_info(self.currency),
            'braintree_params': settings.BRAINTREE_PARAMS,
            'payment_frequency': self.payment_frequency,
            'gateway_address_errors': getattr(self, 'gateway_address_errors', None),
            'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY if settings.RECAPTCHA_ENABLED else None,
        })
        return ctx

    def get_address_info(self, form_data):
        address_info = {
            'street_address': form_data['address_line_1'],
            'locality': form_data['city'],
            'postal_code': form_data['post_code'],
            'country_code_alpha2': form_data['country'],
        }

        if address_info.get('region'):
            address_info['region'] = form_data['region']

        return address_info

    def filter_user_card_errors(self, result):
        client_errors = {
            ErrorCodes.CreditCard.CreditCardTypeIsNotAccepted: _('The type of card you used is not accepted.'),
            ErrorCodes.CreditCard.CvvIsInvalid: _('The CVV code you entered was invalid.'),
            ErrorCodes.CreditCard.CvvVerificationFailed: _('The CVV code you entered was invalid.'),
            ErrorCodes.CreditCard.ExpirationDateIsInvalid: _('The expiration date you entered was invalid.'),
            ErrorCodes.CreditCard.NumberIsInvalid: _('The credit card number you entered was invalid.'),
        }
        return [
            client_errors[error.code] for error in result.errors.deep_errors
            if error.code in client_errors.keys()
        ]

    def check_for_address_errors(self, result):
        errors = {
            ErrorCodes.Address.PostalCodeInvalidCharacters: _('The post code you provided is not valid.'),
            ErrorCodes.Address.PostalCodeIsTooLong: _('The post code you provided is not valid.'),
        }
        for error in result.errors.deep_errors:
            if error.code in errors:
                # The view is expected to catch this exception and report the error
                # back to the view so that the use can try to correct them.
                raise InvalidAddress(errors=[errors[error.code]])

    def process_braintree_error_result(self, result, form):
        """
        Parse an error result object from Braintree, and look for errors
        that we can report back to the user. If we find any, add these to the
        form.
        """
        default_error_message = _('Sorry there was an error processing your payment. '
                                  'Please try again later or use a different payment method.')

        if result.errors.deep_errors:
            # Validation errors exist - check if they are meaningful to the user
            try:
                self.check_for_address_errors(result)
            except InvalidAddress as e:
                self.gateway_address_errors = e.errors
                return self.form_invalid(form)

            errors_to_report = self.filter_user_card_errors(result)
            if errors_to_report:
                for error_msg in errors_to_report:
                    form.add_error(None, error_msg)
            else:
                form.add_error(None, default_error_message)
        else:
            # Processor decline or some other exception
            form.add_error(None, default_error_message)

        queue_ga_event(self.request, ['send', 'event', {
                'eventCategory': 'User Flow',
                'eventAction': 'Card Error',
                'eventLabel': result.message,
            }
        ])
        return self.form_invalid(form)

    def form_valid(self, form, send_data_to_basket=True):
        self.save_campaign_parameters_to_session(form)
        if self.payment_frequency == constants.FREQUENCY_SINGLE:
            return self.process_single_transaction(form, send_data_to_basket=send_data_to_basket)
        else:
            return self.process_monthly_transaction(form)

    def create_customer(self, form):
        result = gateway.customer.create({
            'first_name': form.cleaned_data['first_name'],
            'last_name': form.cleaned_data['last_name'],
            'email': form.cleaned_data['email'],
            'payment_method_nonce': form.cleaned_data['braintree_nonce'],
            'custom_fields': self.get_custom_fields(form),
            'credit_card': {
                'billing_address': self.get_address_info(form.cleaned_data)
            },
            'device_data': form.cleaned_data['device_data'],
        })

        if not result.is_success:
            logger.error(
                'Failed to create Braintree customer: {}'.format(result.message),
                extra={'result': result}
            )

        return result

    def process_single_transaction(self, form, send_data_to_basket=True):
        # Create a customer and payment method for this customer
        # We vault this customer so that upsell doesn't require further authorization
        result = self.create_customer(form)
        if result.is_success:
            payment_method = result.customer.payment_methods[0]
        else:
            return self.process_braintree_error_result(result, form)

        result = gateway.transaction.sale({
            'amount': form.cleaned_data['amount'],
            'merchant_account_id': get_merchant_account_id_for_card(self.currency),
            'payment_method_token': payment_method.token,
            'options': {
                'submit_for_settlement': True
            },
            'device_data': form.cleaned_data['device_data'],
        })

        if result.is_success:
            self.queue_ga_transaction(
                id=result.transaction.id,
                currency=self.currency,
                amount=form.cleaned_data['amount'],
                name='Card Donation',
                category='one-time'
            )
            queue_ga_event(self.request, ['send', 'event', {
                    'eventCategory': 'Donation',
                    'eventAction': 'Card',
                    'eventLabel': 'Single',
                }
            ])
            return self.handle_successful_transaction(
                result,
                form,
                payment_method_token=payment_method.token,
                transaction_id=result.transaction.id,
                settlement_amount=result.transaction.disbursement_details.settlement_amount,
                last_4=result.transaction.credit_card_details.last_4,
                send_data_to_basket=send_data_to_basket,
            )
        else:
            logger.error(
                'Failed Braintree transaction: {}'.format(result.message),
                extra={'result': result}
            )
            return self.process_braintree_error_result(result, form)

    def process_monthly_transaction(self, form):
        # Create a customer and payment method for this customer
        result = self.create_customer(form)

        if result.is_success:
            payment_method = result.customer.payment_methods[0]
        else:
            return self.process_braintree_error_result(result, form)

        # Create a subscription against the payment method
        result = gateway.subscription.create({
            'plan_id': get_plan_id(self.currency),
            'merchant_account_id': get_merchant_account_id_for_card(self.currency),
            'payment_method_token': payment_method.token,
            'price': form.cleaned_data['amount'],
            'first_billing_date': now().date(),
        })

        if result.is_success:
            self.queue_ga_transaction(
                id=result.subscription.id,
                currency=self.currency,
                amount=form.cleaned_data['amount'],
                name='Card Donation',
                category='monthly'
            )
            queue_ga_event(self.request, ['send', 'event', {
                    'eventCategory': 'Donation',
                    'eventAction': 'Card',
                    'eventLabel': 'Monthly',
                }
            ])
            # Bypass self.handle_successful_transaction, as this is not a transaction
            # but a subscription: we won't be posting anything to basket immediately,
            # instead relying on the webhook over in the 'process_webhook' task.
            # We still must set the correct session data
            self.set_session_data(
                result,
                form,
                payment_method=payment_method,
                transaction_id=result.subscription.id,
                last_4=payment_method.last_4,
            )
            return HttpResponseRedirect(self.get_success_url())
        else:
            logger.error(
                'Failed to create Braintree subscription: {}'.format(result.message),
                extra={'result': result}
            )
            return self.process_braintree_error_result(result, form)

    def get_card_type(self, result, **kwargs):
        try:
            transaction = result.transaction
            if transaction.payment_instrument_type == "credit_card":
                credit_card_details = transaction.credit_card_details
                return credit_card_details.card_type

        except AttributeError:
            # check if 'payment_method' was passed as a kwarg
            if 'payment_method' in kwargs:
                return kwargs['payment_method'].card_type

        return 'Unknown'

    def get_transaction_details_for_session(self, result, form, **kwargs):
        details = form.cleaned_data.copy()
        details.update({
            'transaction_id': kwargs['transaction_id'],
            'settlement_amount': kwargs.get('settlement_amount', None),
            'last_4': kwargs['last_4'],
            'payment_method': constants.METHOD_CARD,
            'card_type': self.get_card_type(result, **kwargs),
            'currency': self.currency,
            'payment_frequency': self.payment_frequency,
            'payment_method_token': kwargs.get('payment_method_token'),
        })
        return details

    def get_success_url(self):
        if self.payment_frequency == constants.FREQUENCY_SINGLE:
            return reverse('payments:card_upsell')
        else:
            return super().get_success_url()


class PaypalPaymentView(BraintreePaymentMixin, FormView):
    form_class = BraintreePaypalPaymentForm
    generic_error_message = _('Something went wrong. We were unable to process your payment.')
    http_method_names = ['post']

    def form_valid(self, form, send_data_to_basket=True):
        self.save_campaign_parameters_to_session(form)
        self.payment_frequency = form.cleaned_data['frequency']
        self.currency = form.cleaned_data['currency']
        success_kwargs = {}

        if self.payment_frequency == constants.FREQUENCY_SINGLE:
            result = gateway.transaction.sale({
                'amount': form.cleaned_data['amount'],
                'merchant_account_id': get_merchant_account_id_for_paypal(
                    self.currency, form.cleaned_data['amount']
                ),
                'custom_fields': self.get_custom_fields(form),
                'payment_method_nonce': form.cleaned_data['braintree_nonce'],
                'options': {
                    'submit_for_settlement': True
                }
            })
            if result.is_success:
                self.queue_ga_transaction(
                    id=result.transaction.id,
                    currency=self.currency,
                    amount=form.cleaned_data['amount'],
                    name='PayPal Donation',
                    category='one-time'
                )
                queue_ga_event(self.request, ['send', 'event', {
                        'eventCategory': 'Donation',
                        'eventAction': 'PayPal',
                        'eventLabel': 'Single',
                    }
                ])
        else:
            # Create a customer and payment method for this customer
            result = gateway.customer.create({
                'payment_method_nonce': form.cleaned_data['braintree_nonce'],
                'custom_fields': self.get_custom_fields(form),
            })

            if result.is_success:
                payment_method = result.customer.payment_methods[0]
                success_kwargs['payment_method'] = payment_method
            else:
                return self.form_invalid(form, result=result)

            # Create a subcription against the payment method
            result = gateway.subscription.create({
                'plan_id': get_plan_id(self.currency),
                'merchant_account_id': get_merchant_account_id_for_paypal(
                    self.currency, form.cleaned_data['amount']
                ),
                'payment_method_token': payment_method.token,
                'price': form.cleaned_data['amount'],
                'first_billing_date': now().date(),
            })
            send_data_to_basket = False
            if result.is_success:
                self.queue_ga_transaction(
                    id=result.subscription.id,
                    currency=self.currency,
                    amount=form.cleaned_data['amount'],
                    name='PayPal Donation',
                    category='monthly'
                )
                queue_ga_event(self.request, ['send', 'event', {
                        'eventCategory': 'Donation',
                        'eventAction': 'PayPal',
                        'eventLabel': 'Monthly',
                    }
                ])

        if result.is_success:
            return self.handle_successful_transaction(
                result,
                form,
                send_data_to_basket=send_data_to_basket,
                **success_kwargs
            )

        return self.form_invalid(form, result=result)

    def form_invalid(self, form, result=None):
        if result:
            sentry_logger.error(
                'Failed Braintree transaction: {}'.format(result.message),
                extra={'result': result},
                exc_info=True
            )
        messages.error(self.request, self.generic_error_message)
        return self.redirect_to_source_url()

    def redirect_to_source_url(self):
        # Redirect back to the page that the form was submitted from.
        # The CSRF middleware will reject the request if no valid referrer is set, so
        # there in no possibility of this being empty. The is_safe_url
        # check is also redundant, but we do it just to be sure.
        referrer = self.request.META['HTTP_REFERER']
        if is_safe_url(referrer, allowed_hosts={self.request.get_host()}):
            return HttpResponseRedirect(referrer)

        # If for some reason the referrer was invalid, redirect back to the home page
        return HttpResponseRedirect('/')

    def get_transaction_details_for_session(self, result, form, **kwargs):
        if self.payment_frequency == constants.FREQUENCY_SINGLE:
            transaction_id = result.transaction.id
            settlement_amount = result.transaction.disbursement_details.settlement_amount
            email = result.transaction.paypal_details.payer_email
            first_name = result.transaction.paypal_details.payer_first_name
            last_name = result.transaction.paypal_details.payer_last_name
        else:
            transaction_id = result.subscription.id
            settlement_amount = None
            email = kwargs['payment_method'].email
            first_name = kwargs['payment_method'].payer_info['first_name']
            last_name = kwargs['payment_method'].payer_info['last_name']

        return {
            'amount': form.cleaned_data['amount'],
            'campaign_id': form.cleaned_data['campaign_id'],
            'project': form.cleaned_data['project'],
            'landing_url': form.cleaned_data['landing_url'],
            'settlement_amount': settlement_amount,
            'transaction_id': transaction_id,
            'payment_method': constants.METHOD_PAYPAL,
            'currency': self.currency,
            'payment_frequency': self.payment_frequency,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        }

    def get_success_url(self):
        if self.payment_frequency == constants.FREQUENCY_SINGLE:
            return reverse('payments:paypal_upsell')
        else:
            return super().get_success_url()


class TransactionRequiredMixin:

    """
    Mixin that redirects the user to the home page if they try to access a view
    without having completed a payment transaction.
    """
    def transaction_exists_in_session(self):
        return 'completed_transaction_details' in self.request.session

    def handle_no_transaction(self):
        return HttpResponseRedirect('/')

    def dispatch(self, request, *args, **kwargs):
        if not self.transaction_exists_in_session():
            return self.handle_no_transaction()
        return super().dispatch(request, *args, **kwargs)


class CardUpsellView(TransactionRequiredMixin, BraintreePaymentMixin, FormView):
    form_class = UpsellForm
    success_url = reverse_lazy('payments:newsletter_signup')
    template_name = 'payment/card_upsell.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.transaction_exists_in_session():
            return self.handle_no_transaction()
        # Avoid repeat submissions and make sure that the previous transaction was
        # a single card transaction.
        last_transaction = self.request.session['completed_transaction_details']
        if not(
            last_transaction['payment_frequency'] == constants.FREQUENCY_SINGLE
            and last_transaction['payment_method'] == constants.METHOD_CARD
        ):
            return HttpResponseRedirect(self.get_success_url())

        self.suggested_upgrade = get_suggested_monthly_upgrade(
            last_transaction['currency'], last_transaction['amount']
        )
        self.currency = last_transaction['currency']
        if self.suggested_upgrade is None:
            return HttpResponseRedirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            'amount': self.suggested_upgrade,
            'currency': self.currency,
        }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['currency'] = self.currency
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['currency_info'] = get_currency_info(self.currency)
        return ctx

    def form_valid(self, form):
        payment_method_token = self.request.session['completed_transaction_details']['payment_method_token']
        currency = form.cleaned_data['currency']

        # Create a subcription against the payment method
        start_date = now().date() + relativedelta(months=1)     # Start one month from today
        result = gateway.subscription.create({
            'plan_id': get_plan_id(currency),
            'merchant_account_id': get_merchant_account_id_for_card(currency),
            'payment_method_token': payment_method_token,
            'first_billing_date': start_date,
            'price': form.cleaned_data['amount'],
        })

        if result.is_success:
            self.queue_ga_transaction(
                id=result.subscription.id,
                currency=currency,
                amount=form.cleaned_data['amount'],
                name='Card Donation',
                category='monthly'
            )
            queue_ga_event(self.request, ['send', 'event', {
                    'eventCategory': 'User Flow',
                    'eventAction': 'Monthly Upgrade Click',
                    'eventLabel': 'Yes',
                }
            ])
            return self.handle_successful_transaction(result, form, currency=currency, send_data_to_basket=False)
        else:
            logger.error(
                'Failed to create Braintree subscription: {}'.format(result.message),
                extra={'result': result}
            )
            return self.process_braintree_error_result(result, form)

    def get_transaction_details_for_session(self, result, form, **kwargs):
        # Start with the details from the single payment, which contain`
        # name, email etc., and then update with new information.
        details = self.request.session['completed_transaction_details']
        details.update(form.cleaned_data)
        details.update({
            'transaction_id': result.subscription.id,
            'payment_method': constants.METHOD_CARD,
            'currency': kwargs['currency'],
            'payment_frequency': constants.FREQUENCY_MONTHLY,
        })
        return details

    def process_braintree_error_result(self, result, form):
        default_error_message = _('Sorry there was an error processing your payment. '
                                  'Please try again later.')
        form.add_error(None, default_error_message)
        return self.form_invalid(form)


class PaypalUpsellView(TransactionRequiredMixin, BraintreePaymentMixin, FormView):
    form_class = BraintreePaypalUpsellForm
    success_url = reverse_lazy('payments:newsletter_signup')
    template_name = 'payment/paypal_upsell.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.transaction_exists_in_session():
            return self.handle_no_transaction()
        # Avoid repeat submissions and make sure that the previous transaction was
        # a single card transaction.
        last_transaction = self.request.session['completed_transaction_details']
        if not(
            last_transaction['payment_frequency'] == constants.FREQUENCY_SINGLE
            and last_transaction['payment_method'] == constants.METHOD_PAYPAL
        ):
            return HttpResponseRedirect(self.get_success_url())

        self.suggested_upgrade = get_suggested_monthly_upgrade(
            last_transaction['currency'], last_transaction['amount']
        )
        self.currency = self.request.session['completed_transaction_details']['currency']
        if self.suggested_upgrade is None:
            return HttpResponseRedirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            'currency': self.currency,
            'amount': self.suggested_upgrade
        }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['currency'] = self.currency
        return kwargs

    def form_valid(self, form, send_data_to_basket=True):
        self.currency = form.cleaned_data['currency']

        # Create a customer and payment method for this customer
        result = gateway.customer.create({
            'payment_method_nonce': form.cleaned_data['braintree_nonce'],
            'custom_fields': self.get_custom_fields(form),
        })

        if result.is_success:
            payment_method = result.customer.payment_methods[0]
        else:
            logger.error(
                'Failed to create Braintree customer: {}'.format(result.message),
                extra={'result': result}
            )
            return self.process_braintree_error_result(result, form)

        # Create a subscription against the payment method
        start_date = now().date() + relativedelta(months=1)     # Start one month from today
        result = gateway.subscription.create({
            'plan_id': get_plan_id(self.currency),
            'merchant_account_id': get_merchant_account_id_for_paypal(
                self.currency, form.cleaned_data['amount']
            ),
            'payment_method_token': payment_method.token,
            'first_billing_date': start_date,
            'price': form.cleaned_data['amount'],
        })

        if result.is_success:
            self.queue_ga_transaction(
                id=result.subscription.id,
                currency=self.currency,
                amount=form.cleaned_data['amount'],
                name='PayPal Donation',
                category='monthly'
            )
            queue_ga_event(self.request, ['send', 'event', {
                    'eventCategory': 'User Flow',
                    'eventAction': 'Monthly Upgrade Click',
                    'eventLabel': 'Yes',
                }
            ])
            return self.handle_successful_transaction(result, form, send_data_to_basket=False)
        else:
            logger.error(
                'Failed Braintree transaction: {}'.format(result.message),
                extra={'result': result}
            )
            return self.process_braintree_error_result(result, form)

    def get_transaction_details_for_session(self, result, form, **kwargs):
        # Start with the details from the single payment, which contain`
        # name, email etc., and then update with new information.
        details = self.request.session['completed_transaction_details']
        details.update(form.cleaned_data)
        details.update({
            'transaction_id': result.subscription.id,
            'payment_method': constants.METHOD_PAYPAL,
            'currency': self.currency,
            'payment_frequency': constants.FREQUENCY_MONTHLY,
        })
        return details

    def process_braintree_error_result(self, result, form):
        default_error_message = _('Sorry there was an error processing your payment. '
                                  'Please try again later.')
        form.add_error(None, default_error_message)
        return self.form_invalid(form, result=result)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'braintree_params': settings.BRAINTREE_PARAMS,
            'currency_info': get_currency_info(self.currency),
        })
        return ctx

    def form_invalid(self, form, result=None):
        if result:
            sentry_logger.error(
                'Failed Braintree transaction: {}'.format(result.message),
                extra={'result': result},
                exc_info=True
            )

        return super(PaypalUpsellView, self).form_invalid(form)


class NewsletterSignupView(TransactionRequiredMixin, FormView):
    form_class = NewsletterSignupForm
    success_url = reverse_lazy('payments:completed')
    template_name = 'payment/newsletter_signup.html'

    def get(self, request, *args, **kwargs):
        # Skip this view if the user is already subscribed
        if request.COOKIES.get('subscribed') == '1':
            return HttpResponseRedirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.session['completed_transaction_details'].get('email', '')
        return initial

    def form_valid(self, form, send_data_to_basket=True):
        data = form.cleaned_data.copy()

        if settings.POST_DONATE_NEWSLETTER_URL is not None:
            # This will send the email address to Mailchimp for Thunderbird only.
            newsletter_url = settings.POST_DONATE_NEWSLETTER_URL
            data = parse.urlencode({
                'EMAIL': data['email']
            }).encode()
            res = requests.post(newsletter_url, data=data)
            if not res.ok:
                sentry_logger.error(
                    'Thunderbird newsletter POST failed',
                    extra={'status': res.status_code},
                    exc_info=True
                )

        elif send_data_to_basket:
            data['source_url'] = self.request.build_absolute_uri()
            data['lang'] = self.request.LANGUAGE_CODE
            queue.enqueue(send_newsletter_subscription_to_basket, data)

            queue_ga_event(self.request, ['send', 'event', {
                    'eventCategory': 'Signup',
                    'eventAction': 'Submitted the Form',
                    'eventLabel': 'Email',
                }
            ])

        return super().form_valid(form)


class ThankYouView(TransactionRequiredMixin, TemplateView):
    template_name = 'payment/thank_you.html'

    def get(self, *args, **kwargs):
        # Check if the user is trackable
        if request_is_trackable(self.request):
            for test in AbTest.objects.filter(goal_event='visit-thank-you-page', status=AbTest.STATUS_RUNNING):
                # Is the user a participant in this test?
                if f'wagtail-ab-testing_{test.id}_version' not in self.request.session:
                    continue

                # Has the user already completed the test?
                if f'wagtail-ab-testing_{test.id}_completed' in self.request.session:
                    continue

                # Log a conversion
                test.log_conversion(self.request.session[f'wagtail-ab-testing_{test.id}_version'])
                self.request.session[f'wagtail-ab-testing_{test.id}_completed'] = 'yes'

        return super().get(*args, **kwargs)
