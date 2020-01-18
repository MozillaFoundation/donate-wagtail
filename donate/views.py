from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic.base import RedirectView
from django.shortcuts import render
from donate.payments import constants


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
