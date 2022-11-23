from typing import Sequence, Union, Callable, Any
from django.utils.translation import gettext as _
from django.contrib.admin import ModelAdmin, register, site, display 
from django.contrib.auth.models import Group
from .models import Usuario, Grupo


site.unregister(Group)


@register(Grupo)
class GrupoAdmin(ModelAdmin):
    pass


@register(Usuario)
class UsuarioAdmin(ModelAdmin):
    list_display = ('username', 'nome_apresentacao', 'email', 'email_secundario', 'tipo', 'auth')
    list_filter = ('tipo', 'polo__nome', 'campus__sigla')
    fieldsets = [
        (_('Autorização e autenticação'),
         {"fields": [('nome_civil', 'nome_social'), ('username', 'tipo'), ('is_active', 'is_superuser')],
          "description": _("Controla a identidade do usuário nos sistemas, qual seu papel e quais suas autorizações.")}),
        (_('Aluno'), 
         {"fields": [('campus', 'polo')], 
          "description": _("Estes campos só têm relevância para usuários do tipo aluno.")}),
        (_('Emails'),
         {"fields": [('email_secundario', 'email'), ('email_escolar', 'email_academico')],
          "description": _("Conjunto de e-mails do usuário")}),
        (_('Dates'),
         {"fields": [('date_joined', 'first_login', 'last_login')],
          "description": _("Eventos relevantes relativos a este usuário")}),
    ]
    readonly_fields: Sequence[str] = ['nome_civil', 'nome_social', 'date_joined', 'first_login', 'last_login']
    # autocomplete_fields: Sequence[str] = ['groups']

    @display
    def auth(self, obj):        
        result = ""
        if obj.is_staff:
            result += _('Colaborador superusuário ') if obj.is_superuser else _('Colaborador ')
        else:
            result += _('Usuário ')
        result += _('(Ativo)') if obj.is_active else _('(Inativo)')
        return result
