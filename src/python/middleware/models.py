from django.utils.translation import gettext as _
from django.db.models import Model, CharField, DateTimeField, TextField, JSONField
from django_better_choices import Choices


class Solicitacao(Model):
    class Status(Choices):
        SUCESSO = Choices.Value(_("Sucesso"),    value='S')
        FALHA   = Choices.Value(_("Falha"), value='F')

    timestamp = DateTimeField(_('quando ocorreu'), auto_now_add=True)
    requisicao = TextField(_('requisição'), null=True, blank=True)
    requisicao_header = TextField(_('cabeçalho da requisição'), null=True, blank=True)
    requisicao_invalida = TextField(_('requisição inválida'), null=True, blank=True)
    resposta = TextField(_('resposta'), null=True, blank=True)
    resposta_header = TextField(_('cabeçalho da resposta'), null=True, blank=True)
    resposta_invalida = TextField(_('resposta inválida'), null=True, blank=True)
    campus = JSONField(_('campus'), null=True, blank=True)
    status = CharField(_("status"), max_length=256, choices=Status, null=True, blank=True)
    status_code = CharField(_("status code"), max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = _("Solicitação")
        verbose_name_plural = _("Solicitações")
        ordering = ['id']

    def __str__(self):
        return f'{self.id}'# Create your models here.
