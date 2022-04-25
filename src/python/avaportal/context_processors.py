from django.conf import settings


def gtag(request):
    if getattr(settings, 'GTAG_ID', None) is not None:
        return {'gtag_id': settings.GTAG_ID}
    return {}
