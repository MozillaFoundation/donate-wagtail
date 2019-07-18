from decimal import Decimal, InvalidOperation
import logging
import urllib

from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.template.defaultfilters import floatformat
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import FormView, TemplateView

from braintree import ErrorCodes

from . import constants, gateway
from .exceptions import InvalidAddress
from .forms import BraintreePaymentForm, PersonalDetailsForm
from .utils import freeze_personal_details_for_session

logger = logging.getLogger(__name__)


class BraintreePaymentMixin:
    """
    Mixin for processing Braintree payments.

    Requires the view to set a ``personal_details`` instance
    variable that holds user billing details and amount.
    """
    form_class = BraintreePaymentForm
    personal_details = None

    def get_personal_details_url(self):
        """
        Subclasses must implement this to provide a URL that the user can
        be redirected back to in the event that the payment gateway
        reports an address validation error.
        """
        raise NotImplementedError()

    def report_invalid_address(self, errors):
        """
        Redirect the user back to the payment details view, and add session
        context about the address validation error reported by the gateway.
        """
        self.request.session['gateway_address_errors'] = errors
        return HttpResponseRedirect(self.get_personal_details_url())

    def dispatch(self, *args, **kwargs):
        self.personal_details = self.request.session.get('personal_details')
        # If we don't have personal_details in the session, the user
        # hasn't completed the previous step, so send them to it.
        if not self.personal_details:
            return HttpResponseRedirect(self.get_personal_details_url())
        return super().dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        # Clear any existing address errors from the session
        self.request.session['gateway_address_errors'] = None
        return super().post(*args, **kwargs)

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
                return self.report_invalid_address(e.errors)

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

    def get_custom_fields(self, form):
        return {}

    def get_address_info(self, personal_details):
        address_info = {
            'street_address': personal_details['address_line_1'],
            'locality': personal_details['town'],
            'postal_code': personal_details['post_code'],
            'country_code_alpha2': personal_details['country'],
        }

        if personal_details.get('region'):
            address_info['region'] = personal_details['region']

        return address_info

    def get_merchant_account_id(self):
        return settings.BRAINTREE_MERCHANT_ID

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
                # The view is expected to catch this exception and pass the errors
                # back to the personal details view so that the use can try to correct them.
                raise InvalidAddress(errors=[errors[error.code]])

    def get_transaction_details_for_session(self, result, form):
        raise NotImplementedError()

    def success(self, result, form):
        # Move personal details and transaction ID to a new session variable
        details = self.get_transaction_details_for_session(result, form)
        self.request.session['completed_transaction_details'] = freeze_personal_details_for_session(details)
        del self.request.session['personal_details']
        return HttpResponseRedirect(self.get_success_url())

    def get_braintree_params(self):
        return {
            'use_sandbox': settings.BRAINTREE_USE_SANDBOX
        }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'braintree_tokenization_key': settings.BRAINTREE_TOKENIZATION_KEY,
            'payment_amount': self.personal_details['amount'],
            'braintree_params': self.get_braintree_params(),
        })
        return ctx


class PersonalDetailsView(FormView):
    form_class = PersonalDetailsForm
    template_name = 'payment/personal_details.html'

    def dispatch(self, request, *args, **kwargs):
        if not (kwargs['frequency'] in constants.FREQUENCIES and kwargs['method'] in constants.METHODS):
            raise Http404()
        self.payment_method = kwargs['method']
        self.payment_frequency = kwargs['frequency']
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Ensure that the donation amount is a valid currency decimal
        try:
            Decimal(self.request.GET.get('amount', '50'))
        except InvalidOperation:
            # This will redirect to the campaign/landing page later
            return HttpResponseRedirect('/')

        return super().get(request, *args, **kwargs)

    def get_initial(self):
        # If we have personal details in the session, then repopulate them into the form
        # excepting values that should be fetched from GET params
        initial = self.request.session.get('personal_details', {})
        initial.pop('amount', None)

        amount = self.request.GET.get('amount', 50)
        try:
            initial['amount'] = Decimal(amount)
        except InvalidOperation:
            pass

        return initial

    def form_valid(self, form):
        form_data = form.cleaned_data.copy()
        form_data['amount'] = str(form_data['amount'])
        self.request.session['personal_details'] = form_data
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(f'payments:{self.payment_method}_{self.payment_frequency}')


class SinglePaymentView(BraintreePaymentMixin, FormView):
    method = None

    def get_template_names(self):
        if self.method == constants.METHOD_CARD:
            return ['payment/card_details.html']
        else:
            return ['payment/paypal.html']

    def get_personal_details_url(self):
        params = {}
        if hasattr(self, 'personal_details'):
            params['amount'] = self.personal_details['amount']
        params = urllib.parse.urlencode(params)
        return reverse(
            'payments:personal_details',
            kwargs={'method': self.method, 'frequency': constants.FREQUENCY_SINGLE}
        ) + '?' + params

    def form_valid(self, form):
        if self.personal_details is None:
            raise ValueError('personal_details instance variable has not been set.')

        result = gateway.transaction.sale({
            'amount': floatformat(self.personal_details['amount'], 2),
            'billing': self.get_address_info(self.personal_details),
            'customer': {
                'first_name': self.personal_details['first_name'],
                'last_name': self.personal_details['last_name'],
                'email': self.personal_details['email'],
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

    def get_transaction_details_for_session(self, result, form):
        details = self.personal_details.copy()
        details.update({
            'transaction_id': result.transaction.id,
            'payment_method': self.method,
        })
        return details

    def get_braintree_params(self):
        params = super().get_braintree_params()
        if self.method == constants.METHOD_PAYPAL:
            params['flow'] = 'checkout'
        return params

    def get_success_url(self):
        return reverse('payments:completed')


class MonthlyPaymentView(BraintreePaymentMixin, FormView):
    method = None

    def get_template_names(self):
        if self.method == constants.METHOD_CARD:
            return ['payment/card_details.html']
        else:
            return ['payment/paypal.html']

    def get_personal_details_url(self):
        params = {}
        if hasattr(self, 'personal_details'):
            params['amount'] = self.personal_details['amount']
        params = urllib.parse.urlencode(params)
        return reverse(
            'payments:personal_details',
            kwargs={'method': self.method, 'frequency': constants.FREQUENCY_MONTHLY}
        ) + '?' + params

    def form_valid(self, form):
        if self.personal_details is None:
            raise ValueError('personal_details instance variable has not been set.')

        # Create a customer and payment method for this customsr
        result = gateway.customer.create({
            'first_name': self.personal_details['first_name'],
            'last_name': self.personal_details['last_name'],
            'email': self.personal_details['email'],
            'payment_method_nonce': form.cleaned_data['braintree_nonce'],
            'custom_fields': self.get_custom_fields(form),
            'credit_card': {
                'billing_address': self.get_address_info(self.personal_details)
            }
        })

        if result.is_success:
            payment_method = result.customer.payment_methods[0]
        else:
            logger.error(
                'Failed to create Braintree customer: {}'.format(result.message),
                extra={'result': result}
            )
            self.process_braintree_error_result(result, form)
            return self.form_invalid(form)

        # Create a subcription against the payment method
        result = gateway.subscription.create({
            'plan_id': 'usd',   # TODO we need to map this to per-currency plans in Braintree
            'payment_method_token': payment_method.token,
            'price': floatformat(self.personal_details['amount'], 2),
        })

        if result.is_success:
            return self.success(result, form)
        else:
            logger.error(
                'Failed to create Braintree subscription: {}'.format(result.message),
                extra={'result': result}
            )
            return self.process_braintree_error_result(result, form)

    def get_transaction_details_for_session(self, result, form):
        details = self.personal_details.copy()
        details.update({
            'transaction_id': result.subscription.id,
            'payment_method': self.method,
        })
        return details

    def get_braintree_params(self):
        params = super().get_braintree_params()
        if self.method == constants.METHOD_PAYPAL:
            params['flow'] = 'vault'
        return params

    def get_success_url(self):
        return reverse('payments:completed')


class ThankYouView(TemplateView):
    template_name = 'payment/thank_you.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['completed_transaction_details'] = self.request.session['completed_transaction_details']
        return ctx
