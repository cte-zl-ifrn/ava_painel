# -*- coding: utf-8 -*-
from sc4py.env import env, env_as_bool, env_as_list

SECRET_KEY = env("DJANGO_SECRET_KEY", "changeme")
LOGIN_URL = env("DJANGO_LOGIN_URL", "http://painel/painel/login/")
LOGIN_REDIRECT_URL = env("DJANGO_LOGIN_REDIRECT_URL", "http://painel/painel/")
LOGOUT_REDIRECT_URL = env("DJANGO_LOGOUT_REDIRECT_URL", "http://login/logout/")
AUTH_USER_MODEL = env("DJANGO_AUTH_USER_MODEL", "a4.Usuario")
GO_TO_HTTPS = env_as_bool("GO_TO_HTTPS", False)
AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = []

OAUTH = {
    "BASE_URL": env("OAUTH_BASE_URL", "http://login"),
    "REDIRECT_URI": env("OAUTH_REDIRECT_URI", "http://painel/painel/authenticate/"),
    "CLIENT_ID": env("OAUTH_CLIENT_ID", "changeme"),
    "CLIENT_SECRET": env("OAUTH_CLIENT_SECRET", "changeme"),
    "VERIFY_SSL": env("OAUTH_VERIFY_SSL", False),
}
AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

SUAP_INTEGRADOR_KEY = env("SUAP_INTEGRADOR_KEY", "changeme")

CORS_ORIGIN_ALLOW_ALL = env_as_bool("DJANGO_CORS_ORIGIN_ALLOW_ALL", False)
CORS_ALLOWED_ORIGINS = env_as_list("DJANGO_CORS_ALLOWED_ORIGINS", [OAUTH["BASE_URL"]])
CSRF_TRUSTED_ORIGINS = env_as_list("DJANGO_CSRF_TRUSTED_ORIGINS", [])
