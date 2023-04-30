from django.conf import settings
from django.http import HttpResponse
from django.db import connection


def health(request):
    debug = "FAIL (are active)" if settings.DEBUG else "OK"

    try:
        connection.connect()
        connection_result = "OK"
    except:
        connection_result = "FAIL"

    return HttpResponse(
        f"""
        <pre>
            Reverse proxy: OK.
            Django: OK.
            Database: {connection_result}.
            Redis: Not tested.
            SUAP: Not tested.
            LDAP: Not tested.
            Debug: {debug}.
        </pre>
        """
    )
