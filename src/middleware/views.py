import json
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.http import HttpRequest, JsonResponse
from painel.models import Diario, Campus
from painel.managers import SyncError
from painel.services import get_json_api
from django.shortcuts import get_object_or_404
from base.decorators import exception_as_json, valid_token, check_is_post, check_is_get


@csrf_exempt
@transaction.atomic
@exception_as_json
@check_is_post
@valid_token
def sync_up_enrolments(request: HttpRequest):
    try:
        message_string = request.body.decode("utf-8")
    except Exception as e1:
        return SyncError(f"Erro ao decodificar o body em utf-8 ({e1}).", 405)

    try:
        json.dumps(message_string)
    except Exception as e1:
        return SyncError(f"Erro ao converter para JSON ({e1}).", 407)

    solicitacao = Diario.objects.sync(message_string)
    return JsonResponse(solicitacao.respondido, safe=False)


@csrf_exempt
@exception_as_json
@check_is_get
@valid_token
def sync_down_grades(request: HttpRequest):
    campus = get_object_or_404(Campus, sigla=request.GET.get("campus_sigla"))
    diario_id = int(request.GET.get("diario_id"))
    notas = get_json_api(campus.ambiente, "sync_down_grades", diario_id=diario_id)
    return JsonResponse(notas, safe=False)
