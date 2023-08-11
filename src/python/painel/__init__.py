from django.http import HttpRequest


def request2dict(request: HttpRequest):
    {k: v for k, v in request.headers.items()}
