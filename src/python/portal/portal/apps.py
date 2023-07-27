from tabnanny import verbose
from django.apps import AppConfig


class PortalConfig(AppConfig):
    name = "portal"
    verbose_name = "Painel"
    icon = "fa fa-edit"
