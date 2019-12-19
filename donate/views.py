from django.conf import settings
from django.http import JsonResponse
from django.views import View


class EnvVariablesView(View):
    """
    A view that permits a GET to expose whitelisted environment
    variables in JSON.
    """

    def get(self, request):
        return JsonResponse(settings.FRONTEND)
