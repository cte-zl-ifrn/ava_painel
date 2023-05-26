from django.utils.translation import gettext as _
import json
import urllib
import requests
from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect, render, get_object_or_404
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from .models import Usuario


def register(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        raise ValidationError("Você já tem um registro")


def login(request: HttpRequest) -> HttpResponse:
    OAUTH = settings.OAUTH
    next = urllib.parse.quote_plus(
        request.GET["next"] if "next" in request.GET else "/", safe=""
    )
    redirect_uri = f"{OAUTH['REDIRECT_URI']}?next={next}"
    redirect_uri = OAUTH["REDIRECT_URI"]
    suap_url = f"{OAUTH['BASE_URL']}/o/authorize/?response_type=code&client_id={OAUTH['CLIENTE_ID']}&redirect_uri={redirect_uri}"
    return redirect(suap_url)


def authenticate(request: HttpRequest) -> HttpResponse:
    from portal.models import Campus, Polo

    OAUTH = settings.OAUTH

    if "code" not in request.GET:
        raise Exception(_("O código de autenticação não foi informado."))

    access_token_request_data = {
        "grant_type": "authorization_code",
        "code": request.GET.get("code"),
        "redirect_uri": OAUTH["REDIRECT_URI"],
        "client_id": OAUTH["CLIENTE_ID"],
        "client_secret": OAUTH["CLIENT_SECRET"],
    }

    request_data = json.loads(
        requests.post(
            f"{OAUTH['BASE_URL']}/o/token/",
            data=access_token_request_data,
            verify=OAUTH["VERIFY_SSL"],
        ).text
    )
    headers = {
        "Authorization": "Bearer {}".format(request_data.get("access_token")),
        "x-api-key": OAUTH["CLIENT_SECRET"],
    }
    # response_data = json.loads(requests.get(f"{OAUTH['BASE_URL']}/api/eu/", data={'scope': request_data.get('scope')}, headers=headers, verify=OAUTH['VERIFY_SSL']).text )
    response = requests.get(
        f"{OAUTH['BASE_URL']}/api/eu/?scope={request_data.get('scope')}",
        headers=headers,
        verify=OAUTH["VERIFY_SSL"],
    )
    response_data = json.loads(response.text)

    username = response_data["identificacao"]
    user = Usuario.objects.filter(username=username).first()
    defaults = {
        "nome_registro": response_data.get("nome_registro"),
        "nome_social": response_data.get("nome_social"),
        "nome_usual": response_data.get("nome_usual"),
        "nome": response_data.get("nome"),
        "first_name": response_data.get("primeiro_nome"),
        "last_name": response_data.get("ultimo_nome"),
        "email": response_data.get("email_preferencial"),
        "email_corporativo": response_data.get("email"),
        "email_google_classroom": response_data.get("email_google_classroom"),
        "email_academico": response_data.get("email_academico"),
        "email_secundario": response_data.get("email_secundario"),
        "campus": Campus.objects.filter(sigla=response_data.get("campus")).first(),
        "polo": Polo.objects.filter(suap_id=response_data.get("polo")).first(),
        "foto": response_data.get("foto"),
        "tipo_usuario": response_data.get("tipo_usuario"),
    }
    if user is None:
        is_superuser = Usuario.objects.count() == 0
        user = Usuario.objects.create(
            username=username,
            is_superuser=is_superuser,
            is_staff=is_superuser,
            **defaults,
        )
    else:
        Usuario.objects.filter(username=username).update(**defaults)
    auth.login(request, user)
    return redirect("portal:dashboard")


def logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return render(request, "a4/logout.html")


def personificar(request: HttpRequest, username: str):
    if not request.user.is_superuser:
        raise ValidationError("Só super usuários podem personificar")
    if "usuario_personificado" in request.session:
        raise ValidationError("Você já está personificando um usuário")

    u = get_object_or_404(Usuario, username=username)
    if u.is_superuser:
        raise ValidationError("Ninguém pode personificar um super usuário")

    request.session["usuario_personificado"] = username
    return redirect("portal:dashboard")


def despersonificar(request: HttpRequest) -> HttpResponse:
    if not request.user.is_superuser:
        raise ValidationError("Você não é um super usuário.")
    if "usuario_personificado" not in request.session:
        raise ValidationError("Você não está personificando um usuário.")
    del request.session["usuario_personificado"]
    return redirect("portal:dashboard")
