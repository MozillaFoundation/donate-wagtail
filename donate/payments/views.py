import logging

from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import FormView, TemplateView

from braintree import ErrorCodes

from . import constants, gateway
from .exceptions import InvalidAddress
from .forms import (
    BraintreeCardPaymentForm, BraintreePaypalPaymentForm, StartCardPaymentForm,
    NewsletterSignupForm
)
from .utils import get_currency_info, freeze_transaction_details_for_session

logger = logging.getLogger(__name__)


class BraintreePaymentMixin:
    success_url = reverse_lazy('payments:newsletter_signup')

    def get_custom_fields(self, form):
        return {}

    def get_merchant_account_id(self, currency):
        return settings.BRAINTREE_MERCHANT_ACCOUNTS[currency]

    def get_transaction_details_for_session(self, result, form):
        raise NotImplementedError()

    def process_braintree_error_result(result, form):
        raise NotImplementedError()

    def success(self, result, form):
        # Store details of the transaction in a session variable
        details = self.get_transaction_details_for_session(result, form)
        self.request.session['completed_transaction_details'] = freeze_transaction_details_for_session(details)
        return HttpResponseRedirect(self.get_success_url())


class CardPaymentView(BraintreePaymentMixin, FormView):
    form_class = BraintreeCardPaymentForm
    template_name = 'payment/card.html'

    def dispatch(self, request, *args, **kwargs):
        if kwargs['frequency'] not in constants.FREQUENCIES:
            raise Http404()
        self.payment_frequency = kwargs['frequency']

        # Ensure that the donation amount and currency are legit
        start_form = StartCardPaymentForm(request.GET)
        if not start_form.is_valid():
            return HttpResponseRedirect('/')

        self.amount = start_form.cleaned_data['amount']
        self.currency = start_form.cleaned_data['currency']
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            'amount': self.amount
        }

    def get_plan_id(self, currency):
        return settings.BRAINTREE_PLANS[currency]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'currency_info': get_currency_info(self.currency),
            'braintree_params': settings.BRAINTREE_PARAMS,
            'gateway_address_errors': getattr(self, 'gateway_address_errors', None),
        })
        return ctx

    def get_address_info(self, form_data):
        address_info = {
            'street_address': form_data['address_line_1'],
            'locality': form_data['town'],
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

        return self.form_invalid(form)

    def form_valid(self, form):
        if self.payment_frequency == constants.FREQUENCY_SINGLE:
            return self.process_single_transaction(form)
        else:
            return self.process_monthly_transaction(form)

    def process_single_transaction(self, form):
        result = gateway.transaction.sale({
            'amount': form.cleaned_data['amount'],
            'merchant_account_id': self.get_merchant_account_id(self.currency),
            'billing': self.get_address_info(form.cleaned_data),
            'customer': {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
            },
            # Custom fields need to be set up in Braintree before they will be accepted.
            'custom_fields': self.get_custom_fields(form),
            'payment_method_nonce': form.cleaned_data['braintree_nonce'],
            'options': {
                'submit_for_settlement': True
            }
        })

        if result.is_success:
            return self.success(result, form)
        else:
            logger.error(
                'Failed Braintree transaction: {}'.format(result.message),
                extra={'result': result}
            )
            return self.process_braintree_error_result(result, form)

    def process_monthly_transaction(self, form):
        # Create a customer and payment method for this customsr
        result = gateway.customer.create({
            'first_name': form.cleaned_data['first_name'],
            'last_name': form.cleaned_data['last_name'],
            'email': form.cleaned_data['email'],
            'payment_method_nonce': form.cleaned_data['braintree_nonce'],
            'custom_fields': self.get_custom_fields(form),
            'credit_card': {
                'billing_address': self.get_address_info(form.cleaned_data)
            }
        })

        if result.is_success:
            payment_method = result.customer.payment_methods[0]
        else:
            logger.error(
                'Failed to create Braintree customer: {}'.format(result.message),
                extra={'result': result}
            )
            return self.process_braintree_error_result(result, form)

        # Create a subcription against the payment method
        result = gateway.subscription.create({
            'plan_id': self.get_plan_id(self.currency),
            'merchant_account_id': self.get_merchant_account_id(self.currency),
            'payment_method_token': payment_method.token,
            'price': form.cleaned_data['amount'],
        })

        if result.is_success:
            return self.success(result, form)
        else:
            logger.error(
                'Failed to create Braintree subscription: {}'.format(result.message),
                extra={'result': result}
            )
            return self.process_braintree_error_result(result, form)

    def get_transaction_id(self, result):
        if self.payment_frequency == constants.FREQUENCY_SINGLE:
            return result.transaction.id
        else:
            return result.subscription.id

    def get_transaction_details_for_session(self, result, form):
        details = form.cleaned_data.copy()
        details.update({
            'transaction_id': self.get_transaction_id(result),
            'payment_method': constants.METHOD_CARD,
        })
        return details


class PaypalPaymentView(BraintreePaymentMixin, FormView):
    form_class = BraintreePaypalPaymentForm
    frequency = None
    template_name = 'payment/paypal.html'       # This is only rendered if we have an error

    def form_valid(self, form):
        self.frequency = form.cleaned_data['frequency']

        if self.frequency == constants.FREQUENCY_SINGLE:
            result = gateway.transaction.sale({
                'amount': form.cleaned_data['amount'],
                'custom_fields': self.get_custom_fields(form),
                'payment_method_nonce': form.cleaned_data['braintree_nonce'],
                'options': {
                    'submit_for_settlement': True
                }
            })
        else:
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

            # Create a subcription against the payment method
            result = gateway.subscription.create({
                'plan_id': 'usd',   # TODO we need to map this to per-currency plans in Braintree
                'payment_method_token': payment_method.token,
                'price': form.cleaned_data['amount'],
            })

        if result.is_success:
            return self.success(result, form)
        else:
            logger.error(
                'Failed Braintree transaction: {}'.format(result.message),
                extra={'result': result}
            )
            return self.process_braintree_error_result(result, form)

    def process_braintree_error_result(self, result, form):
        return self.get(self.request)

    def get_transaction_details_for_session(self, result, form):
        if self.frequency == constants.FREQUENCY_SINGLE:
            transaction_id = result.transaction.id
        else:
            transaction_id = result.subscription.id
        return {
            'amount': form.cleaned_data['amount'],
            'transaction_id': transaction_id,
            'payment_method': constants.METHOD_PAYPAL,
        }


class NewsletterSignupView(FormView):
    form_class = NewsletterSignupForm
    success_url = reverse_lazy('payments:completed')
    template_name = 'payment/newsletter_signup.html'


class ThankYouView(TemplateView):
    template_name = 'payment/thank_you.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['completed_transaction_details'] = self.request.session['completed_transaction_details']
        return ctx
