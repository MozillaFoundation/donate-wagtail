from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic.base import RedirectView
from django.shortcuts import render
from donate.payments import constants
from django.views.decorators.http import require_GET


class EnvVariablesView(View):
    """
    A view that permits a GET to expose whitelisted environment
    variables in JSON.
    """

    def get(self, request):
        return JsonResponse(settings.FRONTEND)


class WaysToGiveView(View):
    """
    A view for "ways to give" page
    """

    def get(self, request):
        return render(request, 'pages/core/ways_to_give_page.html', {
            'currencies': constants.CURRENCIES,
            'ways_to_give_link':
                request.scheme + "://" + request.get_host() + "/" + request.LANGUAGE_CODE
                + "/?utm_content=Ways_to_Give",
        })


class ThunderbirdRedirectView(RedirectView):
    """
    A view that redirects requests to give.thunderbird.net, preserving query params
    """

    url = 'https://give.thunderbird.net/'
    permanent = False
    query_string = True


@require_GET
def apple_pay_domain_association_view(request):
    """
    Returns string needed for Apple Pay domain association/verification
    """
    apple_pay_key = settings.APPLE_PAY_DOMAIN_ASSOCIATION_KEY
    key_not_found_message = "Key not found. Please check environment variables."

    if apple_pay_key:
        response_contents = apple_pay_key
        status_code = 200
    else:
        response_contents = key_not_found_message
        status_code = 501

    return HttpResponse(response_contents, status=status_code, content_type="text/plain; charset=utf-8")