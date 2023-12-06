import json
import requests
from functools import update_wrapper
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.contrib.admin import register
from django.utils.html import format_html
from django.urls import path, reverse
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget
from base.admin import BaseModelAdmin
from suapfake.models import Diario


@register(Diario)
class DiarioAdmin(BaseModelAdmin):
    list_display = ["codigo_diario", "acoes"]
    # readonly_fields = ["pacote_recebido"]

    formfield_overrides = {JSONField: {"widget": JSONEditorWidget}}

    def codigo_diario(self, obj):
        return f"{obj}"

    def acoes(self, obj):
        def acao(label: str, url: str, bgcolor: str):
            style = f"""background: {bgcolor};
                        border: 1px solid black;
                        padding: 0 5px;
                        color: black;
                        margin: 0 5px 0 0;"""
            return f'<a style="{style}" href="{url}">{label}</a>'

        if obj.pacote_recebido:
            if "url" in obj.pacote_recebido:
                return format_html(
                    acao(
                        "Sincronizar",
                        reverse("admin:suapfake_diario_sync", args=[obj.id]),
                        "silver",
                    )
                    + acao(
                        "Diário",
                        obj.pacote_recebido["url"],
                        "aquamarine",
                    )
                    + acao(
                        "Coordenação",
                        obj.pacote_recebido["url_sala_coordenacao"],
                        "aquamarine",
                    )
                )

            else:
                return format_html(
                    f"""<a style="border: 1px solid black; padding: 0 5px; background: silver; color: black; margin: 0 5px 0 0;" href="{reverse("admin:suapfake_diario_sync", args=[obj.id])}">Sincronizar</a>"""
                    f'<a style="border: 1px solid black; padding: 0 5px; background: red; color: black; margin: 0 5px 0 0;" href="#">Error</a>'
                )
        else:
            return format_html(
                f'<a style="border: 1px solid black; padding: 0 5px; background: silver; color: black; margin: 0 5px 0 0;" href="{reverse("admin:suapfake_diario_sync", args=[obj.id])}">Sincronizar</a>'
            )

    acoes.short_description = "Ações"
    acoes.allow_tags = True

    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name
        return [
            path(
                "<path:object_id>/sync_moodle/",
                wrap(self.sync_view),
                name="%s_%s_sync" % info,
            )
        ] + super().get_urls()

    def sync_view(self, request, object_id, form_url="", extra_context=None):
        try:
            diario = get_object_or_404(Diario, pk=object_id)
        except Exception as e:
            raise Exception("Erro ao tentar sincronizar. Diário não localizado.")
        try:
            response = requests.post(
                url="http://localhost:8000/api/moodle_suap/",
                json=diario.pacote_enviado,
                headers={"AUTHENTICATION": f"Token {settings.MOODLE_SYNC_TOKEN}"},
            )
        except Exception as e:
            raise Exception(f"Erro ao tentar sincronizar. Resposta inválida: {e}")

        try:
            diario.pacote_recebido = json.loads(response.content)
            diario.save()
            return redirect("admin:suapfake_diario_changelist")
        except Exception as e:
            raise Exception(
                f"""Erro ao tentar sincronizar. Não foi possível converter para JSON.
                    {response.content}"""
            )
