from django.http.response import HttpResponseRedirectBase
from django.conf import settings

hostnames = settings.TARGET_DOMAINS


class HttpResponseTemporaryRedirect(HttpResponseRedirectBase):
    status_code = 307


class TargetDomainRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_host = request.META['HTTP_HOST']
        protocol = 'https' if request.is_secure() else 'http'

        if request_host in hostnames:
            return self.get_response(request)

        # Redirect to the primary domain (hostnames[0])
        redirect_url = '{protocol}://{hostname}{path}'.format(
            protocol=protocol,
            hostname=hostnames[0],
            path=request.get_full_path()
        )

        return HttpResponseTemporaryRedirect(redirect_url)
