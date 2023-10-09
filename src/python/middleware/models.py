from django.utils.translation import gettext as _
from django.db.models import CharField, DateTimeField, JSONField, ForeignKey, PROTECT, QuerySet
from django_better_choices import Choices
from django.utils.html import format_html
from simple_history.models import HistoricalRecords
from safedelete.models import SafeDeleteModel, SafeDeleteManager


class SolicitacaoManager(SafeDeleteManager):
    def by_diario_id(self, diario_id: int) -> QuerySet:
        filter = f'"diario":{{"id":{diario_id},'
        return self.filter(recebido__contains=filter).order_by("-id")

    def ultima_do_diario(self, diario_id: int) -> QuerySet:
        filter = f'"diario":{{"id":{diario_id},'
        return self.filter(recebido__contains=filter).order_by("-id")[0:1].get()


class Solicitacao(SafeDeleteModel):
    class Status(Choices):
        SUCESSO = Choices.Value(_("Sucesso"), value="S")
        FALHA = Choices.Value(_("Falha"), value="F")
        PROCESSANDO = Choices.Value(_("Processando"), value="P")

    timestamp = DateTimeField(_("quando ocorreu"), auto_now_add=True)
    status = CharField(_("status"), max_length=256, choices=Status, null=True, blank=True)
    status_code = CharField(_("status code"), max_length=256, null=True, blank=True)
    campus = ForeignKey("painel.Campus", on_delete=PROTECT, null=True, blank=True)
    diario = ForeignKey("painel.Diario", on_delete=PROTECT, null=True, blank=True)
    recebido = JSONField(_("JSON recebido"), null=True, blank=True)
    enviado = JSONField(_("JSON enviado"), null=True, blank=True)
    respondido = JSONField(_("JSON respondido"), null=True, blank=True)

    objects = SolicitacaoManager()

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("solicitação")
        verbose_name_plural = _("solicitações")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.id} - {self.diario}"

    @property
    def status_merged(self):
        return format_html(f"""{Solicitacao.Status[self.status].display}<br>{self.status_code}""")
