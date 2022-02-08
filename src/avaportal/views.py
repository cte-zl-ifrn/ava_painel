import json
import requests
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required
from .models import Usuario, Campus, Polo, Solicitacao


def login(request):
    OAUTH = settings.OAUTH
    return redirect(f"{OAUTH['AUTHORIZE_URL']}?response_type=code&client_id={OAUTH['CLIENTE_ID']}&redirect_uri={OAUTH['REDIRECT_URI']}")


def authenticate(request):
    OAUTH = settings.OAUTH
    assert 'code' in request.GET, _("O código de autenticação não foi informado.")
    
    access_token_request_data = dict(
        grant_type='authorization_code',
        code=request.GET.get('code'),
        redirect_uri=OAUTH['REDIRECT_URI'],
        client_id=OAUTH['CLIENTE_ID'],
        client_secret=OAUTH['CLIENT_SECRET']
    )
    request_data = json.loads(requests.post(OAUTH['ACCESS_TOKEN_URL'], data=access_token_request_data, verify=False).text)
    headers = {'Authorization': 'Bearer {}'.format(request_data.get('access_token')), 'x-api-key': OAUTH['CLIENT_SECRET']}
    http_method = requests.post if OAUTH['METHOD'] == 'POST' else requests.get
    http_method = requests.get
    response_data = json.loads( http_method(OAUTH['USER_DATA_URL'], data={'scope': request_data.get('scope')}, headers=headers).text )
    
    username = response_data['identificacao']
    user = Usuario.objects.filter(username=username).first()
    if user is None:
        is_superuser = Usuario.objects.count() == 0
        user = Usuario.objects.create(
            username=username,
            nome=response_data.get('nome'),
            email=response_data.get('email'),
            email_escolar=response_data.get('email_google_classroom'),
            email_academico=response_data.get('email_academico'),
            email_pessoal=response_data.get('email_secundario'),
            campus=Campus.objects.filter(sigla=response_data.get('campus')).first(),
            polo=Polo.objects.filter(suap_id=response_data.get('polo')).first(),
            tipo=Usuario.Tipo.get_by_length(len(username)),
            # status=response_data.get('status'),
            is_superuser=is_superuser,
            is_staff=is_superuser,
        )
    auth.login(request, user)
    return redirect('/')

# Create your views here.
def health(request):
    debug = "OK" if settings.DEBUG == False else "FAIL (are active)"
    try:
        Campus.objects.all().exists()
        connection = "OK"
    except:
        connection = "FAIL"
    return HttpResponse(f"""
    <pre>
    Reverse proxy: OK.
    Django: OK.
    Database: {connection}.
    Debug: {debug}.
    Status: ALL FINE.
    </pre>
    """)


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
        r = requests.post(
            f"{campus.url}/auth/suap/sync_up.php", 
            data={"jsonstring": request.body}, 
            headers={"Authentication": f"Token {campus.token}"}
        )
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
    solicitacao.campus = campus
    solicitacao.save()
 
    return HttpResponse(r.text)

