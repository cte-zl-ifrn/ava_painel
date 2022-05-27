from django.utils.translation import gettext as _
import json
import urllib
import requests
from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def login(request: HttpRequest) -> HttpResponse:
    OAUTH = settings.OAUTH
    next = urllib.parse.quote_plus(request.GET['next'] if 'next' in request.GET else '/',safe="")
    redirect_uri = f"{OAUTH['REDIRECT_URI']}?next={next}"
    redirect_uri = OAUTH['REDIRECT_URI']
    suap_url = f"{OAUTH['BASE_URL']}/o/authorize/?response_type=code&client_id={OAUTH['CLIENTE_ID']}&redirect_uri={redirect_uri}"
    return redirect(suap_url)


def authenticate(request: HttpRequest) -> HttpResponse:
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
    user = User.objects.filter(username=username).first()
    if user is None:
        is_superuser = User.objects.count() == 0
        user = User.objects.create(
            username=username,
            first_name="response_data.get('first_name')",
            last_name="response_data.get('last_name')",
            email=response_data.get('email'),
            is_superuser=is_superuser,
            is_staff=is_superuser,
        )
    auth.login(request, user)
    return redirect('/')
