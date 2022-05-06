from tabnanny import verbose
from django.apps import AppConfig


class SuapFakeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'suapfake'
    verbose_name = 'SUAP Fake'
    icon = ''
