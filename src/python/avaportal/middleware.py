import logging
from urllib.parse import urlsplit, urlunsplit
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.middleware.security import SecurityMiddleware


logger = logging.getLogger(__name__)


class GoToHTTPSMiddleware(MiddlewareMixin):
    """
    Force all requests to use HTTPs when behind a reverse proxy.

    .. note::
        ``settings.GO_TO_HTTPS`` needs to be True.
        The RP need to inform HTTP_X_FORWARDED_PROTO and HTTP_X_FORWARDED_HOST.
        If RP dont inform HTTP_X_FORWARDED_PROTO http will be assumed.
    """
    def process_request(self, request):
        meta = request.META

        if not getattr(settings, 'GO_TO_HTTPS', False):
            return None
        
        host = meta['HTTP_X_FORWARDED_HOST'] or request.get_host()
        url = "https://%s%s" % (host, request.get_full_path())

        if 'HTTP_X_FORWARDED_PROTO' in meta and meta['HTTP_X_FORWARDED_PROTO'] == 'http':
            return HttpResponseRedirect(url)

        if 'HTTP_X_FORWARDED_PROTO' not in meta:
            return HttpResponseRedirect(url)

