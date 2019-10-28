from django.conf import settings


def export_vars(request):
    data = {}
    data['THUNDERBIRD_INSTANCE'] = settings.THUNDERBIRD_INSTANCE
    return data
