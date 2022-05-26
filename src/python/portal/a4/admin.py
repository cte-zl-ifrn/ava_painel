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
    list_display = ('username', 'nome', 'email', 'email_secundario', 'tipo', 'auth')
    list_filter = ('tipo', 'polo__nome', 'campus__sigla')
    fieldsets = [
        (None, {"fields": ['username', 'tipo'],}),
        (_('Aluno'), {"fields": ['campus', 'polo'],}),
        (_('Emails'), {"fields": ['email', 'email_escolar', 'email_academico', 'email_secundario'],}),
        (_('Auth'), {"fields": ['is_active', 'is_superuser', 'groups'],}),
        (_('Dates'), {"fields": ['date_joined', 'first_login', 'last_login'],}),
    ]

    @display
    def auth(self, obj):        
        result = ""
        if obj.is_staff:
            result += _('Colaborador superusuário ') if obj.is_superuser else _('Colaborador ')
        else:
            result += _('Usuário ')
        result += _('(Ativo)') if obj.is_active else _('(Inativo)')
        return result
