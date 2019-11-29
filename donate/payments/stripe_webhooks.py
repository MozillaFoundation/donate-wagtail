import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from .tasks import queue, process_stripe_webhook


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    http_method_names = ['post']

    def post(self, request):
        signature = request.META['HTTP_STRIPE_SIGNATURE']

        if not signature:
            return HttpResponseBadRequest(reason='HTTP_STRIPE_SIGNATURE must be provided')

        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest(reason='Payload is not valid JSON')

        queue.enqueue(process_stripe_webhook, payload, signature=signature)

        return HttpResponse()
