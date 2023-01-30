from django.utils.translation import gettext as _
import requests, json
from functools import update_wrapper
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.utils.html import format_html
from django.db import transaction
from django.urls import path, reverse
from django.contrib.admin import register, ModelAdmin
from django.conf import settings
from .models import Solicitacao
from portal.models import Diario, h2d


@register(Solicitacao)
class SolicitacaoAdmin(ModelAdmin):
    list_display = ('timestamp', 'status', 'status_code', 'campus', 'diario', 'status_code')
    list_display = ('timestamp', 'status', 'status_code', 'campus', 'diario', 'status_code', 'acoes')
    list_filter = ('status', 'status_code', 'campus')
    search_fields = ['campus', 'requisicao', 'requisicao_header', 'resposta', 'resposta_header', 'diario__codigo']
    autocomplete_fields = ['campus', 'diario']
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)

    def acoes(self, obj):
        return format_html(
            f'<a style="border: 1px solid black; padding: 0 5px; background: silver; color: black; margin: 0 5px 0 0;" href="{reverse("admin:middleware_solicitacao_sync", args=[obj.id])}">Reenviar</a>'
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
        
    @transaction.atomic
    def sync_view(self, request, object_id, form_url="", extra_context=None):
        s = get_object_or_404(Solicitacao, pk=object_id)
        try:
            Diario.sync(s.requisicao, s.requisicao_header)
        except Exception as e:
            return HttpResponse(e.message)
            
