from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic.base import RedirectView

class EnvVariablesView(View):
    """
    A view that permits a GET to expose whitelisted environment
    variables in JSON.
    """

    def get(self, request):
        return JsonResponse(settings.FRONTEND)


class ThunderbirdRedirectView(RedirectView):
    """
    A view that redirects requests to give.thunderbird.net, preserving query params
    """

    url = 'https://give.thunderbird.net/'
    permanent = False # True
    query_string = True
