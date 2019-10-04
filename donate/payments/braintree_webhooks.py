from django import forms
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from .tasks import queue, process_webhook


class WebhookForm(forms.Form):
    bt_signature = forms.CharField()
    bt_payload = forms.CharField()


@method_decorator(csrf_exempt, name='dispatch')
class BraintreeWebhookView(FormView):
    form_class = WebhookForm
    http_method_names = ['post']

    def form_valid(self, form):
        queue.enqueue(process_webhook, form.cleaned_data)
        return HttpResponse()

    def form_invalid(self, form):
        return HttpResponseBadRequest()
