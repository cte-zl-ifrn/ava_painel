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
    list_display = ['username', 'nome_apresentacao', 'email', 'tipo', 'auth', 'acoes']
    list_filter = ['tipo', 'is_superuser', 'is_active', 'is_staff', 'polo__nome', 'campus__sigla']
    search_fields = ['username', 'nome_apresentacao', 'email', 'email_secundario']
    fieldsets = [
        (_('Identificação'),
          {"fields": ['nome_civil', 'nome_social', 'username'],
           "description": _("Identifica o usuário.")}),
        (_('Autorização e autenticação'),
          {"fields": ['tipo', ('is_active', 'is_staff', 'is_superuser')],
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
        result = '<img src="/painel/static/admin/img/icon-yes.svg" alt="True"> ' if obj.is_active else '<img src="/painel/static/admin/img/icon-no.svg" alt="False"> '
        result += _('Colaborador') if obj.is_staff else _('Usuário')
        result += " " + _('superusuário') if obj.is_staff else ""
        # result += _('(Ativo)') if obj.is_active else _('(Inativo)')
        
        return mark_safe(result)

    @display(description=_('Ações'))
    def acoes(self, obj):
        if not obj.is_superuser:
          url = reverse("admin:a4_usuario_personificar", args=[obj.username])
          result = f'<a href="{url}">Personificar</a>'
        else:
          result = '-'
        return format_html(result)
    acoes.allow_tags = True

    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)
        return [ 
            path(
              "<path:username>/personificar/",
              wrap(self.personificar_view),
              name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_personificar"
            )
        ] + super().get_urls()

    def personificar_view(self, request, username, form_url="", extra_context=None):
        if not request.user.is_superuser:
            raise ValidationError('Só super usuários podem personificar')
        if 'usuario_personificado' in request.session:
            raise ValidationError('Você já está personificando um usuário')

        u = get_object_or_404(Usuario, username=username)
        if u.is_superuser:
            raise ValidationError('Ninguém pode personificar um super usuário')

        request.session['usuario_personificado'] = username
        return redirect(reverse("admin:a4_usuario_changelist"))
        
