from django import forms
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from .tasks import queue, process_stripe_webhook


class StripeWebhookForm(forms.Form):
    data = forms.TextInput()


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(FormView):
    form_class = StripeWebhookForm
    http_method_names = ['post']

    def form_valid(self, form):
        signature = self.request.META['HTTP_STRIPE_SIGNATURE']
        queue.enqueue(process_stripe_webhook, form.cleaned_data, signature=signature)
        return HttpResponse()

    def form_invalid(self, form):
        return HttpResponseBadRequest()
