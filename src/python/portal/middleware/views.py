import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.forms import ValidationError
from django.conf import settings
from portal.models import Campus, Diario, h2d, SyncError
from .models import Solicitacao
from django.db import transaction


def raise_error(request, error):
    solicitacao = Solicitacao.objects.create(
        status=Solicitacao.Status.FALHA,
        campus=error.campus if 'campus' in dir(error) else None,
        status_code=error.code,
        
        requisicao_header=h2d(request),
        requisicao_invalida=request.body,
        
        resposta_header=h2d(error.retorno) if error.retorno else None,
        resposta_invalida=error.retorno.text if error.retorno else None
    )
    
    error_json = {"error": error.message, "code": error.code, "solicitacao_id": solicitacao.id}
    return JsonResponse(error_json, status=error.code)


@csrf_exempt
@transaction.atomic
def moodle_suap(request):
    try:
        if not hasattr(settings, 'SUAP_EAD_KEY'):
            raise SyncError("Você se esqueceu de configurar a settings 'SUAP_EAD_KEY'.", 428)
        
        if 'HTTP_AUTHENTICATION' not in request.META:
            raise SyncError("Envie o token de autenticação no header.", 431)

        if f"Token {settings.SUAP_EAD_KEY}" != request.META['HTTP_AUTHENTICATION']:
            raise SyncError("Você enviou um token de auteticação diferente do que tem na settings 'SUAP_EAD_KEY'.", 403)

        if request.method == 'POST':
            diario = Diario.sync(request.body, h2d(request))
            return JsonResponse(diario)
        else:
            return _baixar_notas(request)
    except SyncError as e:
        return raise_error(request, e)
    except Exception as e:
        return JsonResponse({"error": str(e), "code": 500})
        

def _baixar_notas(request):
    return raise_error(request, SyncError("Não implementado.", 501))
