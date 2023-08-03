from django.utils.translation import gettext as _
from django.db.models import CharField, DateTimeField, TextField, ForeignKey, PROTECT
from django_better_choices import Choices
from simple_history.models import HistoricalRecords
from safedelete.models import SafeDeleteModel


class Solicitacao(SafeDeleteModel):
    class Status(Choices):
        SUCESSO = Choices.Value(_("Sucesso"), value="S")
        FALHA = Choices.Value(_("Falha"), value="F")

    timestamp = DateTimeField(_("quando ocorreu"), auto_now_add=True)
    status = CharField(
        _("status"), max_length=256, choices=Status, null=True, blank=True
    )
    status_code = CharField(_("status code"), max_length=256, null=True, blank=True)
    campus = ForeignKey("painel.Campus", on_delete=PROTECT, null=True, blank=True)
    diario = ForeignKey("painel.Diario", on_delete=PROTECT, null=True, blank=True)
    recebido = TextField(_("JSON recebido"), null=True, blank=True)
    enviado = TextField(_("JSON enviado"), null=True, blank=True)
    respondido = TextField(_("JSON respondido"), null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("solicitação")
        verbose_name_plural = _("solicitações")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.id} - {self.diario}"
