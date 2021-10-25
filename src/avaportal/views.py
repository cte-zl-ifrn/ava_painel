import json
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Campus, Solicitacao
import requests


# Create your views here.
def index(request):
    campus = Campus.objects.filter(homepage=True)
    return render(request, 'avaportal/index.html', {'campus': campus})


def raise_error(request, error, code):
    solicitacao = Solicitacao()
    solicitacao.requisicao_header = request.META
    solicitacao.requisicao_invalida = request.body.decode('utf-8')
    solicitacao.resposta = error
    solicitacao.status = Solicitacao.Status.FALHA
    solicitacao.status_code = code
    solicitacao.save()
    response = JsonResponse(error)
    response.status_code=code
    return response

@csrf_exempt
def sync_up(request):
    
    if not hasattr(settings, 'SUAP_EAD_KEY'):
        raise Exception("Você se esqueceu de configurar a settings 'SUAP_EAD_KEY'.")
    
    if 'HTTP_AUTHENTICATION' not in request.META:
        raise Exception("Envie o token de autenticação no header.")

    if f"Token {settings.SUAP_EAD_KEY}" != request.META['HTTP_AUTHENTICATION']:
        raise Exception("Você enviou um token de auteticação diferente do que tem na settings 'SUAP_EAD_KEY'.")

    if request.method != 'POST':
        return HttpResponse("Mandou via GET pq?")

    try:
        pkg = json.loads(request.body)
        filter = {"suap_id": pkg["campus"]["id"], "sigla": pkg["campus"]["sigla"]}
    except Exception as e:
        return raise_error(request, {"error": f"O JSON está inválido. {e}", "code": 406}, 406)
    
    campus = Campus.objects.filter(**filter).first()
    if campus is None:
        return raise_error(request, {"error": f"Não existe um campus com o id '{filter['suap_id']}' E a sigla '{filter['sigla']}'.", "code": 404}, 404)

    if not campus.active:
        return raise_error(request, {"error": f"O campus '{filter['sigla']}' existe, mas está inativo.", "code": 412 }, 412)

    try:
       url = f"{campus.url}/auth/suap/sync_up.php"
       r = requests.post(url, data=request.body, headers={"Content-Type":"application/json", "Authentication": f"Token {campus.token}"})
    except Exception as e:
        return raise_error(request, {"error": f"Erro na integração. {e}", "code": 400}, 400)

    if r.status_code != 200:
        return raise_error(request, {"error": f"Erro na integração. {r.text}", "code": r.status_code}, r.status_code)

    solicitacao = Solicitacao()
    solicitacao.requisicao = request.body.decode('utf-8')
    solicitacao.requisicao_header = request.META
    solicitacao.resposta = r.text
    solicitacao.resposta_header = r.headers
    solicitacao.status = Solicitacao.Status.SUCESSO
    solicitacao.status_code = r.status_code
    solicitacao.save()
 
    return HttpResponse(r.text)

