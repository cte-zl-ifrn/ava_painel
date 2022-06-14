from django.http import HttpResponse
from django.utils.translation import gettext as _
import json
from functools import partial, update_wrapper
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.contrib.admin.utils import flatten_fieldsets, unquote
from django.contrib.admin import helpers
from django.forms.formsets import all_valid
from django.core.exceptions import PermissionDenied
from django.utils.html import format_html 
from django.urls import path, reverse
from django.views.generic import RedirectView
from django.template.response import SimpleTemplateResponse, TemplateResponse
from sc4py import *
from .models import Diario
import requests


@admin.register(Diario)
class DiarioAdmin(admin.ModelAdmin):
    list_display = ['codigo_diario', 'acoes']
    exclude = ['pacote_recebido']

    def codigo_diario(self, obj):
        return f"{obj}"

    def acoes(self, obj):
        if obj.pacote_recebido:
            url = obj.pacote_recebido['url']
            return format_html(
                f'<a style="border: 1px solid black; padding: 0 5px; background: red; color: black; margin: 0 5px 0 0;" href="{reverse("admin:suapfake_diario_sync", args=[obj.id])}">Sincronizar</a>'
                f'<a style="border: 1px solid black; padding: 0 5px; background: aquamarine; color: black; margin: 0 5px 0 0;" href="{url}">Acessar AVA</a>'
            )
        else:
            return format_html(
                f'<a href="{reverse("admin:suapfake_diario_sync", args=[obj.id])}">Sincronizar</a>'
            )

    acoes.short_description = 'Ações'
    acoes.allow_tags = True
    
    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)
        info = self.model._meta.app_label, self.model._meta.model_name
        return [ 
            path( "<path:object_id>/sync_moodle/", wrap(self.sync_view), name="%s_%s_sync" % info) 
        ] + super().get_urls()

    def sync_view(self, request, object_id, form_url="", extra_context=None):
        try:
            diario = get_object_or_404(Diario, pk=object_id)
            response = requests.post(
                url=settings.MOODLE_SYNC_URL, 
                json=diario.pacote_enviado, 
                headers={'AUTHENTICATION': f'Token {settings.MOODLE_SYNC_TOKEN}'}
            )
            diario.pacote_recebido = json.loads(response.content)
            diario.save()
            return redirect('admin:suapfake_diario_changelist')
        except Exception as e:
            raise Exception(f"Erro ao tentar sincronizar. Solicite ao administrador que acesse o portal e verifique a causa.")
        

