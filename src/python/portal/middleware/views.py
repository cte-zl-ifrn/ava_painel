import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.conf import settings
from portal.models import Campus, Ambiente
from .models import Solicitacao


def raise_error(request, error, code, campus=None, retorno=None):
    solicitacao = Solicitacao()

    solicitacao.status = Solicitacao.Status.FALHA
    solicitacao.campus = campus
    solicitacao.status_code = code

    solicitacao.requisicao_header = {k:v for k,v in request.headers.items()}
    solicitacao.requisicao_invalida = request.body
   
    solicitacao.resposta = error
    if retorno:
        solicitacao.resposta_header = {k:v for k,v in retorno.headers.items()}
        solicitacao.resposta_invalida = retorno.text
   
    solicitacao.save()
    
    error['identificador'] = solicitacao.id
    response = JsonResponse(error)
    response.status_code=code
    return response


@csrf_exempt
def moodle_suap(request):
    if not hasattr(settings, 'SUAP_EAD_KEY'):
        response = JsonResponse({"error": "Você se esqueceu de configurar a settings 'SUAP_EAD_KEY'."})
        response.status_code=500
        return response        
    
    if 'HTTP_AUTHENTICATION' not in request.META:
        response = JsonResponse({"error": "Envie o token de autenticação no header."})
        response.status_code=500
        return response        

    if f"Token {settings.SUAP_EAD_KEY}" != request.META['HTTP_AUTHENTICATION']:
        response = JsonResponse({"error": "Você enviou um token de auteticação diferente do que tem na settings 'SUAP_EAD_KEY'."})
        response.status_code=500
        return response        

    if request.method == 'POST':
        return _sincronizar_diario(request)
    else:
        return _baixar_notas(request)


def _sincronizar_diario(request):
    try:
        pkg = json.loads(request.body)
        filter = {"suap_id": pkg["campus"]["id"], "sigla": pkg["campus"]["sigla"]}
    except Exception as e:
        return raise_error(request, {"error": f"O JSON está inválido. {e}", "code": 406}, 406)
    
    campus = Campus.objects.filter(**filter).first()
    if campus is None:
        return raise_error(request, {"error": f"Não existe um campus com o id '{filter['suap_id']}' e a sigla '{filter['sigla']}'.", "code": 404}, 404)

    if not campus.active:
        return raise_error(request, {"error": f"O campus '{filter['sigla']}' existe, mas está inativo.", "code": 412 }, 412, campus)
    
    if not campus.ambiente.active:
        return raise_error(request, {"error": f"O campus '{filter['sigla']}' existe e está ativo, mas o ambiente {campus.ambiente.sigla} está inativo.", "code": 412 }, 412, campus)

    try:
        retorno = requests.post(
            f"{campus.ambiente.url}/auth/suap/sync_up.php", 
            data={"jsonstring": request.body}, 
            headers={"Authentication": f"Token {campus.ambiente.token}"}
        )
    except Exception as e:
        return raise_error(request, {"error": f"Erro na integração. {e}", "code": 400}, 400, campus)
    

    retorno_json = None
    if retorno.status_code != 200:
        try:
            retorno_json = json.loads(retorno.text)
        except:
            return raise_error(request, {"error": f"Erro na integração. Contacte um administrador.", "code": retorno.status_code}, retorno.status_code, campus, retorno)
        return raise_error(request, {"error": retorno_json, "code": retorno.status_code}, retorno.status_code, campus, retorno)
    
    
    solicitacao = Solicitacao()
    solicitacao.requisicao = pkg
    solicitacao.requisicao_header = {k:v for k,v in request.headers.items()}
    solicitacao.resposta = retorno_json
    solicitacao.resposta_header = {k:v for k,v in retorno.headers.items()}
    solicitacao.status = Solicitacao.Status.SUCESSO
    solicitacao.status_code = retorno.status_code
    solicitacao.campus = campus
    solicitacao.save()
 
    return HttpResponse(retorno.text)


def _baixar_notas(request):
    return raise_error(request, {"error": f"Não implementado.", "code": 501}, 501)
