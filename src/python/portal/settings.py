from pathlib import Path
from sc4py.env import env, env_as_bool, env_as_int, env_as_list
import logging.config


BASE_DIR = Path(__file__).resolve().parent


DEBUG = env_as_bool("DJANGO_DEBUG", False)


# Get loglevel from env
LOGLEVEL = env('DJANGO_LOGLEVEL', 'DEBUG').upper()


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        'parso': {
            'level': 'WARNING',
            'handlers': ['console',],
        },
        '': {
            'level': LOGLEVEL,
            'handlers': ['console',],
        },
    },
})


# Apps
MY_APPS = env_as_list('MY_APPS', [
    'portal',
    'health',
    'middleware',
])
THIRD_APPS = env_as_list('THIRD_APPS', [
    'markdownx',
    'django_extensions',
    # 'adminlte3',
    # 'adminlte3_admin',
])
DJANGO_APPS = env_as_list('DJANGO_APPS', [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'a4',
])
INSTALLED_APPS = MY_APPS + THIRD_APPS + DJANGO_APPS

# Middleware
MIDDLEWARE = [
    'portal.middleware.GoToHTTPSMiddleware', # <-
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Routing
WSGI_APPLICATION = env('DJANGO_WSGI_APPLICATION', 'wsgi.application')
ALLOWED_HOSTS = env_as_list('DJANGO_ALLOWED_HOSTS', '*' if DEBUG else '')
USE_X_FORWARDED_HOST = env_as_bool('DJANGO_USE_X_FORWARDED_HOST', False)
SECURE_PROXY_SSL_HEADER = env_as_list('DJANGO_SECURE_PROXY_SSL_HEADER', '')
ROOT_URLCONF = env('DJANGO_ROOT_URLCONF', 'urls')
STATIC_URL = env('DJANGO_STATIC_URL', '/static/')
STATIC_ROOT = env('DJANGO_STATIC_ROOT', "/var/static")
MEDIA_URL = env('DJANGO_MEDIA_URL', '/media/')
MEDIA_ROOT = env('DJANGO_MEDIA_ROOT', '/var/media')
MARKDOWNX_URLS_PATH = env('MARKDOWNX_URLS_PATH', '/markdownx/markdownify/')
MARKDOWNX_UPLOAD_URLS_PATH = env('MARKDOWNX_UPLOAD_URLS_PATH', '/markdownx/upload/')


# Template engine
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'portal.context_processors.gtag',

                'portal.context_processors.layout_settings',
                'portal.context_processors.top_menu',
                'portal.context_processors.user',
                'adminlte3_admin.context_processors.sidebar_menu',
                'portal.context_processors.messages',
                'portal.context_processors.notifications',                
            ]
        },
    },
]
TABBED_ADMIN_USE_JQUERY_UI = True
GTAG_ID = env("GTAG_ID", None)


# Database
DATABASES = {
    'default': {
        'ENGINE': env('POSTGRES_ENGINE', 'django.db.backends.postgresql_psycopg2'),
        'HOST': env('POSTGRES_HOST', 'db'),
        'PORT': env('POSTGRES_PORT', '5432'),
        'NAME': env('POSTGRES_DATABASE', 'postgres'),
        'USER': env('POSTGRES_USER', 'ava_user'),
        'PASSWORD': env('POSTGRES_PASSWORD', 'ava_pass'),
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Localization
LANGUAGE_CODE = env('DJANGO_USE_I18N', 'pt-br')
TIME_ZONE = env('DJANGO_USE_I18N', 'America/Fortaleza')
USE_I18N = env_as_bool('DJANGO_USE_I18N', True)
USE_L10N = env_as_bool('DJANGO_USE_L10N', True)
USE_TZ = env_as_bool('DJANGO_USE_TZ', True)


# Development
if DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + env_as_list('DEV_APPS', 'debug_toolbar' if DEBUG else '')
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: request.get_host() in ['localhost', '127.0.0.1'],
    }
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']


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
# SESSION_KEY = env("DJANGO_SESSION_KEY", 'ead_portal')
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
SECRET_KEY = env("DJANGO_SECRET_KEY", 'changeme')
AUTH_PASSWORD_VALIDATORS = []
LOGIN_URL = env('DJANGO_LOGIN_URL', 'login/')
LOGIN_REDIRECT_URL = env('DJANGO_LOGIN_REDIRECT_URL', '/')
LOGOUT_REDIRECT_URL = env("DJANGO_LOGOUT_REDIRECT_URL", LOGIN_REDIRECT_URL)
AUTH_USER_MODEL = env('DJANGO_AUTH_USER_MODEL', 'a4.Usuario')
GO_TO_HTTPS = env_as_bool('GO_TO_HTTPS', False)

OAUTH = {
    'REDIRECT_URI': env('SUAP_REDIRECT_URI', 'http://localhost:8000/authenticate/'),
    'CLIENTE_ID': env('SUAP_CLIENTE_ID', 'change me on confs/enabled/app.env'),
    'CLIENT_SECRET': env('SUAP_CLIENT_SECRET', 'change me on confs/enabled/app.env'),
    'BASE_URL': env('SUAP_BASE_URL', 'https://suap.ifrn.edu.br'),
    'VERIFY_SSL': env('SUAP_VERIFY_SSL', False),
}

AUTHENTICATION_BACKENDS = (
    # 'a4.backends.SuapOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SUAP_EAD_KEY = env('SUAP_EAD_KEY', 'changeme')
