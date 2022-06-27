from django.utils.translation import gettext as _
import json
import urllib
import requests
from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from .models import Usuario


def register(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        raise ValidationError('Você já tem um registro')


def login(request: HttpRequest) -> HttpResponse:
    OAUTH = settings.OAUTH
    next = urllib.parse.quote_plus(request.GET['next'] if 'next' in request.GET else '/',safe="")
    redirect_uri = f"{OAUTH['REDIRECT_URI']}?next={next}"
    redirect_uri = OAUTH['REDIRECT_URI']
    suap_url = f"{OAUTH['BASE_URL']}/o/authorize/?response_type=code&client_id={OAUTH['CLIENTE_ID']}&redirect_uri={redirect_uri}"
    return redirect(suap_url)


def authenticate(request: HttpRequest) -> HttpResponse:
    from portal.models import Campus, Polo
    OAUTH = settings.OAUTH
    
    assert 'code' in request.GET, _("O código de autenticação não foi informado.")
    
    access_token_request_data = dict(
        grant_type='authorization_code',
        code=request.GET.get('code'),
        redirect_uri=OAUTH['REDIRECT_URI'],
        client_id=OAUTH['CLIENTE_ID'],
        client_secret=OAUTH['CLIENT_SECRET']
    )
    request_data = json.loads(requests.post(f"{OAUTH['BASE_URL']}/o/token/", data=access_token_request_data, verify=OAUTH['VERIFY_SSL']).text)
    headers = {'Authorization': 'Bearer {}'.format(request_data.get('access_token')), 'x-api-key': OAUTH['CLIENT_SECRET']}
    response_data = json.loads(requests.get(f"{OAUTH['BASE_URL']}/api/eu/", data={'scope': request_data.get('scope')}, headers=headers, verify=OAUTH['VERIFY_SSL']).text )
    
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
            email_secundario=response_data.get('email_secundario'),
            campus=Campus.objects.filter(sigla=response_data.get('campus')).first(),
            polo=Polo.objects.filter(suap_id=response_data.get('polo')).first(),
            tipo=Usuario.Tipo.get_by_length(len(username)),
            # status=response_data.get('status'),
            is_superuser=is_superuser,
            is_staff=is_superuser,
        )
    auth.login(request, user)
    return redirect('/')


def logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return render(request, "a4/logout.html")
