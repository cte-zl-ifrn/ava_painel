from pathlib import Path
from sc4py.env import env, env_as_bool, env_as_int, env_as_list
import logging.config
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from datetime import datetime
from django.core.exceptions import DisallowedHost


PAINEL_VERSION = "1.0.49"


BASE_DIR = Path(__file__).resolve().parent

DEBUG = env_as_bool("DJANGO_DEBUG", False)


# Get loglevel from env
LOGLEVEL = env("DJANGO_LOGLEVEL", "DEBUG").upper()


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s"
            },
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "console"},
        },
        "loggers": {
            "parso": {"level": "WARNING", "handlers": ["console"]},
            "": {"level": LOGLEVEL, "handlers": ["console"]},
        },
    }
)


# Apps
MY_APPS = env_as_list(
    "MY_APPS",
    [
        "painel",
        "health",
        "middleware",
    ],
)

MY_APPS += ["suapfake"] if env_as_bool("SUAPFAKE", True) else []

THIRD_APPS = env_as_list(
    "THIRD_APPS",
    [
        # 'markdownx',
        "django_extensions",
        "import_export",
        "simple_history",
        "safedelete",
        "django_sass",
        "djrichtextfield",
        "django_json_widget",
        # "django_admin_json_editor",
        # "corsheaders",
        # "adminlte3",
        # "adminlte3_admin",
    ],
)
DJANGO_APPS = env_as_list(
    "DJANGO_APPS",
    [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "a4",
    ],
)
INSTALLED_APPS = MY_APPS + THIRD_APPS + DJANGO_APPS

# Middleware
MIDDLEWARE = [
    "painel.middleware.GoToHTTPSMiddleware",  # <-
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

# Routing
WSGI_APPLICATION = env("DJANGO_WSGI_APPLICATION", "wsgi.application")
ALLOWED_HOSTS = env_as_list("DJANGO_ALLOWED_HOSTS", "*" if DEBUG else "")
USE_X_FORWARDED_HOST = env_as_bool("DJANGO_USE_X_FORWARDED_HOST", True)
SECURE_PROXY_SSL_HEADER = env_as_list("DJANGO_SECURE_PROXY_SSL_HEADER", "")
ROOT_URL_PATH = env("DJANGO_ROOT_URL_PATH", "painel/")
ROOT_URLCONF = env("DJANGO_ROOT_URLCONF", "urls")
STATIC_URL = env("DJANGO_STATIC_URL", f"{ROOT_URL_PATH}static/")
STATIC_ROOT = env("DJANGO_STATIC_ROOT", "/var/static")
MEDIA_URL = env("DJANGO_MEDIA_URL", f"{ROOT_URL_PATH}media/")
MEDIA_ROOT = env("DJANGO_MEDIA_ROOT", "/var/media")
MARKDOWNX_URLS_PATH = env("MARKDOWNX_URLS_PATH", "/markdownx/markdownify/")
MARKDOWNX_UPLOAD_URLS_PATH = env("MARKDOWNX_UPLOAD_URLS_PATH", "/markdownx/upload/")

# Template engine
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "painel.context_processors.gtag",
                "painel.context_processors.popup",
                "painel.context_processors.layout_settings",
                "painel.context_processors.top_menu",
                "painel.context_processors.user",
                "adminlte3_admin.context_processors.sidebar_menu",
                "painel.context_processors.messages",
                "painel.context_processors.notifications",
            ]
        },
    },
]

if DEBUG:
    TEMPLATES[0]["APP_DIRS"] = False
    TEMPLATES[0]["OPTIONS"]["loaders"] = [
        "django.template.loaders.app_directories.Loader"
    ]

TABBED_ADMIN_USE_JQUERY_UI = True
GTAG_ID = env("GTAG_ID", None)


# Database
DATABASES = {
    "default": {
        "ENGINE": env("POSTGRES_ENGINE", "django.db.backends.postgresql"),
        "HOST": env("POSTGRES_HOST", "db"),
        "PORT": env("POSTGRES_PORT", "5432"),
        "NAME": env("POSTGRES_DATABASE", "postgres"),
        "USER": env("POSTGRES_USER", "ava_user"),
        "PASSWORD": env("POSTGRES_PASSWORD", "ava_pass"),
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Localization
LANGUAGE_CODE = env("DJANGO_USE_I18N", "pt-br")
TIME_ZONE = env("DJANGO_USE_I18N", "America/Fortaleza")
USE_I18N = env_as_bool("DJANGO_USE_I18N", True)
USE_L10N = env_as_bool("DJANGO_USE_L10N", True)
USE_TZ = env_as_bool("DJANGO_USE_TZ", True)


# Development
if DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + env_as_list(
        "DEV_APPS", "debug_toolbar" if DEBUG else ""
    )
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: request.get_host()
        in ["localhost", "127.0.0.1", "localhost:8000", "127.0.0.1:8000"],
    }
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]


# # REST Framework
# REST_FRAMEWORK = {
#     'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
#     'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.BrowsableAPIRenderer','rest_framework.renderers.JSONRenderer',],
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
#     'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.SessionAuthentication',),
#     'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',],
# }


# # Email
# EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", 'django.core.mail.backends.smtp.EmailBackend')
# EMAIL_HOST = env("DJANGO_EMAIL_HOST", 'localhost')
# EMAIL_PORT = env_as_int("DJANGO_EMAIL_PORT", 25)
# EMAIL_HOST_USER = env("DJANGO_EMAIL_HOST_USER", '')
# EMAIL_HOST_PASSWORD = env("DJANGO_EMAIL_HOST_PASSWORD", '')
# EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX", '[SUAP-TI] ')
# EMAIL_USE_LOCALTIME = env_as_bool("DJANGO_EMAIL_USE_LOCALTIME", False)
# EMAIL_USE_TLS = env_as_bool("DJANGO_EMAIL_USE_TLS", False)
# EMAIL_USE_SSL = env_as_bool("DJANGO_EMAIL_USE_SSL", False)
# EMAIL_SSL_CERTFILE = env("DJANGO_EMAIL_SSL_CERTFILE", None)
# EMAIL_SSL_KEYFILE = env("DJANGO_EMAIL_SSL_KEYFILE", None)
# EMAIL_TIMEOUT = env_as_int("DJANGO_EMAIL_TIMEOUT", None)


# # Session
# SESSION_KEY = env("DJANGO_SESSION_KEY", 'painel_ava')
# SESSION_COOKIE_NAME = env("DJANGO_SESSION_COOKIE_NAME", '%s_sessionid' % SESSION_KEY)
# SESSION_COOKIE_AGE = env_as_int('DJANGO_SESSION_COOKIE_AGE', 1209600)
# SESSION_COOKIE_DOMAIN = env('DJANGO_SESSION_COOKIE_DOMAIN', None)
# SESSION_COOKIE_HTTPONLY = env_as_bool('DJANGO_SESSION_COOKIE_HTTPONLY', False)
# SESSION_COOKIE_PATH = env("DJANGO_SESSION_COOKIE_PATH", "/")
# SESSION_COOKIE_SAMESITE = env("DJANGO_SESSION_COOKIE_SAMESITE", 'Lax')
# SESSION_COOKIE_SECURE = env_as_bool('DJANGO_SESSION_COOKIE_SECURE', False)
# SESSION_EXPIRE_AT_BROWSER_CLOSE = env_as_bool('DJANGO_SESSION_EXPIRE_AT_BROWSER_CLOSE', False)
# SESSION_FILE_PATH = env('DJANGO_SESSION_FILE_PATH', None)
# SESSION_SAVE_EVERY_REQUEST = env_as_bool('DJANGO_SESSION_SAVE_EVERY_REQUEST', False)
# SESSION_SERIALIZER = env("DJANGO_SESSION_SERIALIZER", 'django.contrib.sessions.serializers.JSONSerializer')
# # SESSION_ENGINE = env("DJANGO_SESSION_ENGINE", 'redis_sessions.session')
# # SESSION_REDIS = {
# #     'host': env("DJANGO_SESSION_REDIS_HOST", 'redis'),
# #     'port': env_as_int("DJANGO_SESSION_REDIS_PORT", 6379),
# #     'db': env_as_int("DJANGO_SESSION_REDIS_DB", 0),
# #     'password': env("DJANGO_SESSION_REDIS_PASSWORD", 'redis_password'),
# #     'prefix': env("DJANGO_SESSION_REDIS_PREFIX", '%s_session' % session_slug),
# #     'socket_timeout': env("DJANGO_SESSION_REDIS_SOCKET_TIMEOUT", 0.1),
# #     'retry_on_timeout': env("DJANGO_SESSION_REDIS_RETRY_ON_TIMEOUT", False),
# # }


# Auth and Security... some another points impact on security, take care!
SECRET_KEY = env("DJANGO_SECRET_KEY", "changeme")
AUTH_PASSWORD_VALIDATORS = []
LOGIN_URL = env("DJANGO_LOGIN_URL", "login/")
LOGIN_REDIRECT_URL = env("DJANGO_LOGIN_REDIRECT_URL", "/")
LOGOUT_REDIRECT_URL = env("DJANGO_LOGOUT_REDIRECT_URL", LOGIN_REDIRECT_URL)
AUTH_USER_MODEL = env("DJANGO_AUTH_USER_MODEL", "a4.Usuario")
GO_TO_HTTPS = env_as_bool("GO_TO_HTTPS", False)

SUAP_BASE_URL = env("SUAP_BASE_URL", "https://suap.ifrn.edu.br")
OAUTH = {
    "REDIRECT_URI": env("SUAP_REDIRECT_URI", "http://ava/painel/authenticate/"),
    "CLIENTE_ID": env("SUAP_CLIENTE_ID", "change me on confs/enabled/app.env"),
    "CLIENT_SECRET": env("SUAP_CLIENT_SECRET", "change me on confs/enabled/app.env"),
    "BASE_URL": SUAP_BASE_URL,
    "VERIFY_SSL": env("SUAP_VERIFY_SSL", False),
}
AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

SUAP_EAD_KEY = env("SUAP_EAD_KEY", "changeme")
SUAP_PAINEL_FAKEUSER = env("SUAP_PAINEL_FAKEUSER", None)
MOODLE_SYNC_URL = env("MOODLE_SYNC_URL", "http://ava/api/moodle_suap/")
MOODLE_SYNC_TOKEN = env("MOODLE_SYNC_TOKEN", "changeme")

CORS_ORIGIN_ALLOW_ALL = env_as_bool("DJANGO_CORS_ORIGIN_ALLOW_ALL", False)
CORS_ALLOWED_ORIGINS = env_as_list("DJANGO_CORS_ALLOWED_ORIGINS", [SUAP_BASE_URL])
CSRF_TRUSTED_ORIGINS = env_as_list("DJANGO_CSRF_TRUSTED_ORIGINS", [])

LAST_STARTUP = int(datetime.timestamp(datetime.now()) * 1000)

DJRICHTEXTFIELD_CONFIG = {
    # https://github.com/jaap3/django-richtextfield
    #
    # TinyMCE
    # "js": ["//cdn.tiny.cloud/1/no-api-key/tinymce/5/tinymce.min.js"],
    # "init_template": "djrichtextfield/init/tinymce.js",
    # "settings": {
    #     "menubar": True,
    #     "plugins": "link image",
    #     # "toolbar": "bold italic | link image | removeformat",
    #     "width": "100%",
    # },
    #
    # CKEditor
    "js": ["//cdn.ckeditor.com/4.14.0/standard/ckeditor.js"],
    "init_template": "djrichtextfield/init/ckeditor.js",
    "settings": {
        # "toolbar": [
        #     {"items": ["Format", "-", "Bold", "Italic", "-", "RemoveFormat"]},
        #     {"items": ["Link", "Unlink", "Image", "Table"]},
        #     {"items": ["Source"]},
        # ],
        "format_tags": "p;h1;h2;h3",
        "width": "100%",
    },
}

# Observabilidade
if env("SENTRY_DNS", None):
    sentry_sdk.init(
        dsn=env("SENTRY_DNS"),
        integrations=[DjangoIntegration(), RedisIntegration()],
        default_integrations=env_as_bool("SENTRY_DEFAULT_INTEGRATIONS", True),
        # Informe em porcentual, ou seja, 50 significa que 100% de erros serão reportados.
        sample_rate=env_as_int("SENTRY_SAMPLE_RATE", 100) / 100.0,
        # before_send=,
        # before_breadcrumb=,
        # Informe em porcentual, ou seja, 50 significa que 100% de erros serão reportados.
        traces_sample_rate=env_as_int("SENTRY_TRACES_SAMPLE_RATE", 100) / 100.0,
        # traces_sampler=
        # If you wish to associate users to errors (assuming you are using django.contrib.auth) you may enable sending PII data.
        send_default_pii=env_as_bool("SENTRY_SEND_DEFAULT_PII", True),
        debug=env_as_bool("SENTRY_DEBUG", False),
        environment=env("SENTRY_ENVIRONMENT", "local"),
        max_breadcrumbs=env_as_int("SENTRY_MAX_BREADCRUMBS", 100),
        with_locals=env_as_bool("SENTRY_WITH_LOCALS", True),
        ignore_errors=[DisallowedHost]
        # release=env('SENTRY_RELEASE', '1.0.0'),
        # attach_stacktrace=env('SENTRY_ATTACH_STACKTRACE', 'off'),
        # server_name=env('SENTRY_SERVER_NAME', 'off'),
        # in_app_include=env_as_list('SENTRY_IN_APP_INCLUDE', []),
        # in_app_exclude=env_as_list('SENTRY_IN_APP_EXCLUDE', []),
        # request_bodies=env_as_list('SENTRY_REQUEST_BODIES', []),
        # ca_certs=
        # request_bodies=
        # send_client_reports=
        # transport=,
        # shutdown_timeout=env_as_int('SENTRY_SHUTDOWN_TIMEOUT', 2),
    )
