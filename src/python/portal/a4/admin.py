from typing import Sequence, Union, Callable, Any
from functools import update_wrapper
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import path, reverse
from django.contrib.admin import ModelAdmin, register, site, display 
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect
from .models import Usuario, Grupo

site.unregister(Group)


@register(Grupo)
class GrupoAdmin(ModelAdmin):
    pass


@register(Usuario)
class UsuarioAdmin(ModelAdmin):
    list_display = ['username', 'nome_usual', 'email', 'tipo_usuario', 'auth', 'acoes']
    list_filter = ['tipo_usuario', 'is_superuser', 'is_active', 'is_staff', 'polo__nome', 'campus__sigla']
    search_fields = ['username', 'nome_usual', 'email', 'email_secundario']
    fieldsets = [
        (_('Identificação'),
          {"fields": ['username', 'nome_usual', 'nome_registro', 'nome_social'],
           "description": _("Identifica o usuário.")}),
        (_('Autorização e autenticação'),
          {"fields": ['tipo_usuario', ('is_active', 'is_staff', 'is_superuser')],
           "description": _("Controla a identidade do usuário nos sistemas, qual seu papel e quais suas autorizações.")}),
        (_('Aluno'), 
          {"fields": [('campus', 'polo')], 
           "description": _("Estes campos só têm relevância para usuários do tipo aluno.")}),
        (_('Emails'),
          {"fields": [('email_secundario', 'email'), ('email_google_classroom', 'email_academico')],
           "description": _("Conjunto de e-mails do usuário")}),
        (_('Dates'),
          {"fields": [('date_joined', 'first_login', 'last_login')],
           "description": _("Eventos relevantes relativos a este usuário")}),
    ]
    readonly_fields: Sequence[str] = ['date_joined', 'first_login', 'last_login']
    # autocomplete_fields: Sequence[str] = ['groups']

    @display
    def auth(self, obj):        
        result = '<img src="/painel/static/admin/img/icon-yes.svg" alt="True"> ' if obj.is_active else '<img src="/painel/static/admin/img/icon-no.svg" alt="False"> '
        result += _('Colaborador') if obj.is_staff else _('Usuário')
        result += " " + _('superusuário') if obj.is_staff else ""
        return mark_safe(result)

    @display(description=_('Ações'))
    def acoes(self, obj):
        if not obj.is_superuser:
          url = reverse("a4:personificar", args=[obj.username])
          result = f'<a href="{url}">Personificar</a>'
        else:
          result = '-'
        return format_html(result)
    acoes.allow_tags = True
