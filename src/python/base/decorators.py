from django.http import HttpRequest, JsonResponse
from django.conf import settings
from sentry_sdk import capture_exception
from painel.managers import SyncError


def exception_as_json(func):
    def __response_error(request: HttpRequest, error: Exception):
        event_id = capture_exception(error)
        error_json = {
            "error": getattr(error, "message", None),
            "code": getattr(error, "code", 500),
            "event_id": event_id,
        }

        return JsonResponse(error_json, status=getattr(error, "code", 500))

    def inner(request: HttpRequest, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except SyncError as se:
            return __response_error(request, se)
        except Exception as e2:
            return __response_error(request, e2)

    return inner


def valid_token(func):
    def inner(request: HttpRequest, *args, **kwargs):
        if not hasattr(settings, "SUAP_EAD_KEY"):
            raise SyncError("Você se esqueceu de configurar a settings 'SUAP_EAD_KEY'.", 428)

        if "HTTP_AUTHENTICATION" not in request.META:
            raise SyncError("Envie o token de autenticação no header.", 431)

        if f"Token {settings.SUAP_EAD_KEY}" != request.META["HTTP_AUTHENTICATION"]:
            raise SyncError(
                "Você enviou um token de autenticação diferente do que tem na settings 'SUAP_EAD_KEY'.", 403  # noqa
            )
        return func(request, *args, **kwargs)

    return inner


def check_is_post(func):
    def inner(request: HttpRequest, *args, **kwargs):
        if request.method != "POST":
            raise SyncError("Não implementado.", 501)
        return func(request, *args, **kwargs)

    return inner


def check_is_get(func):
    def inner(request: HttpRequest, *args, **kwargs):
        if request.method != "GET":
            raise SyncError("Não implementado.", 501)
        return func(request, *args, **kwargs)

    return inner
