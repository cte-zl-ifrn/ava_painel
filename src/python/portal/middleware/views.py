import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.conf import settings
from sentry_sdk import capture_exception
from portal.models import Diario, SyncError
from middleware.models import Solicitacao
from portal import request2dict


def response_error(request: HttpRequest, error: Exception):
    event_id = capture_exception(error)
    try:
        message_string = request.body.decode("utf-8")
    except Exception:
        try:
            message_string = request.body
        except Exception as ie2:
            message_string = f"erro ao decodificar a requisição {ie2}"

    solicitacao = Solicitacao.objects.create(
        status=Solicitacao.Status.FALHA,
        campus=error.campus if "campus" in dir(error) else None,
        status_code=error.code,
        requisicao_header=request2dict(request),
        requisicao=message_string,
        resposta_header=request2dict(error.retorno) if error.retorno else None,
        resposta=error.retorno.text if error.retorno else None,
    )

    error_json = {
        "error": error.message,
        "code": error.code,
        "solicitacao_id": solicitacao.id,
        "event_id": event_id,
    }

    return JsonResponse(error_json, status=error.code)


@csrf_exempt
@transaction.atomic
def moodle_suap(request: HttpRequest):
    try:
        if not hasattr(settings, "SUAP_EAD_KEY"):
            raise SyncError(
                "Você se esqueceu de configurar a settings 'SUAP_EAD_KEY'.", 428
            )

        # if "HTTP_AUTHENTICATION" not in request.META:
        #     raise SyncError("Envie o token de autenticação no header.", 431)

        # if f"Token {settings.SUAP_EAD_KEY}" != request.META["HTTP_AUTHENTICATION"]:
        #     raise SyncError(
        #         "Você enviou um token de auteticação diferente do que tem na settings 'SUAP_EAD_KEY'.",
        #         403,
        #     )

        if request.method != "POST":
            raise SyncError("Não implementado.", 501)

        try:
            message_string = request.body.decode("utf-8")
        except Exception as e1:
            return SyncError(f"Erro ao decodificar o body em utf-8 ({e1}).", 405)

        try:
            json.dumps(message_string)
        except Exception as e1:
            return SyncError(f"Erro ao converter para JSON ({e1}).", 407)

        response = Diario.sync(message_string, request2dict(request))
        return JsonResponse(response)

    except SyncError as se:
        print(type(se), se)
        print(se)
        return response_error(request, se)
    except Exception as e2:
        print(type(e2), e2)
        return response_error(request, e2)
