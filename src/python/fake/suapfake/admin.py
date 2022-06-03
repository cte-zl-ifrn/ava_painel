from functools import partial, update_wrapper
from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, reverse
from django.views.generic import RedirectView
from django.template.response import SimpleTemplateResponse, TemplateResponse
from .models import Diario


@admin.register(Diario)
class DiarioAdmin(admin.ModelAdmin):
    list_display = ['codigo_diario', 'acoes']
    exclude = ['pacote_recebido']

    def codigo_diario(self, obj):
        return f"{obj}"

    def acoes(self, obj):
        if obj.pacote_recebido:
            return format_html(
                f'<a href="{reverse("admin:suapfake_diario_sync", args=[obj.id])}">Sincronizar</a>'
                f'<a href="{obj.pacote_recebido}">Acessar AVA</a>'
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
            path( "<path:object_id>/", wrap(self.sync_view), name="%s_%s_sync" % info) 
        ] + super().get_urls()

    def sync_view(self, request, object_id, form_url="", extra_context=None):
        form_template = None
        app_label = 'suapfake'
        model_name = 'diario'
        context = {}

        return TemplateResponse(
            request,
            form_template or [
                "admin/%s/%s/preview_form.html" % (app_label, model_name),
                "admin/%s/preview_form.html" % app_label,
                "admin/preview_form.html",
            ],
            context
        )
