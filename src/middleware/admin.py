import json
from functools import update_wrapper
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.utils.html import format_html
from django.db import transaction
from django.urls import path, reverse
from django.contrib.admin import register, display
from django.db.models import JSONField
from django.forms import ModelForm
from django_json_widget.widgets import JSONEditorWidget
from base.admin import BaseModelAdmin
from .models import Solicitacao
from painel.models import Diario


@register(Solicitacao)
class SolicitacaoAdmin(BaseModelAdmin):
    list_display = ("quando", "status_merged", "campus_sigla", "codigo_diario", "acoes", "professores")
    list_filter = ("status", "status_code", "campus")
    search_fields = ["recebido", "enviado", "respondido", "diario__codigo"]
    autocomplete_fields = ["campus", "diario"]
    date_hierarchy = "timestamp"
    ordering = ("-timestamp",)

    class SolicitacaoAdminForm(ModelForm):
        class Meta:
            model = Solicitacao
            widgets = {"recebido": JSONEditorWidget(), "enviado": JSONEditorWidget(), "respondido": JSONEditorWidget()}
            fields = "__all__"
            readonly_fields = ["timestamp"]

    formfield_overrides = {JSONField: {"widget": JSONEditorWidget}}
    form = SolicitacaoAdminForm

    @display(description="Status")
    def status_merged(self, obj):
        return format_html(f"""{Solicitacao.Status[obj.status].display}<br>{obj.status_code}""")

    @display(description="Ações")
    def acoes(self, obj):
        return format_html(
            f"""<a class="export_link" href="{reverse("admin:middleware_solicitacao_sync", args=[obj.id])}">Reenviar</a>"""
        )

    @display(description="Campus", ordering="campus__sigla")
    def campus_sigla(self, obj):
        return obj.campus.sigla if obj.campus else "-"

    @display(description="Quando", ordering="timestamp")
    def quando(self, obj):
        return obj.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    @display(description="Professores", ordering="timestamp")
    def professores(self, obj):
        try:
            recebido = json.loads(obj.recebido)
            return format_html("<ul>" + "".join([f"<li>{x['nome']}</li>" for x in recebido["professores"]]) + "</ul>")
        except Exception:
            return "-"

    @display(description="Diário", ordering="timestamp")
    def codigo_diario(self, obj):
        try:
            recebido = json.loads(obj.recebido)
            codigo = f"{recebido['turma']['codigo']}.{recebido['diario']['sigla']}#{recebido['diario']['id']}"
            try:
                respondido = json.loads(obj.respondido.replace("'", '"'))
                suap_url = "https://suap.ifrn.edu.br"
                return format_html(
                    f"""<a href='{respondido['url']}'>{codigo}</a><br>
                        <a href='{respondido['url_sala_coordenacao']}'>Coordenação</a><br>
                        <a href='{suap_url}/edu/meu_diario/{recebido['diario']['id']}/1/'>SUAP</a>"""
                )
            except Exception:
                return codigo
        except Exception:
            return "-"

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
                wrap(self.sync_moodle_view),
                name="%s_%s_sync" % info,
            )
        ] + super().get_urls()

    @transaction.atomic
    def sync_moodle_view(self, request, object_id, form_url="", extra_context=None):
        s = get_object_or_404(Solicitacao, pk=object_id)
        try:
            solicitacao = Diario.objects.sync(json.dumps(s.recebido))
            return redirect("admin:middleware_solicitacao_view", object_id=solicitacao.id)
        except Exception as e:
            return HttpResponse(f"{e}")
