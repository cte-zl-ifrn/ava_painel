from django.utils.translation import gettext as _
from django.conf import settings
from django.db.models import Model, CharField, JSONField


class Diario(Model):
    suap_id = CharField(_('ID do diário no SUAP'), max_length=255, unique=True)
    codigo = CharField(_('código do diário'), max_length=255, unique=True)
    pacote_enviado = JSONField(_('pacote enviado'))
    pacote_recebido = JSONField(_('pacote recebido'))
    
    class Meta:
        verbose_name = _("diário")
        verbose_name_plural = _("diários")
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo}'
