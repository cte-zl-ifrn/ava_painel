from tokenize import blank_re
from django.utils.translation import gettext as _
from django.conf import settings
from django.db.models import Model, JSONField
from simple_history.models import HistoricalRecords
from safedelete.models import SafeDeleteModel


def get_default_pacote():
    return {
        "campus": {"id": 1, "descricao": "Campus EaD", "sigla": "EAD"},
        "curso": {
            "id": 1,
            "codigo": "00001",
            "nome": "Tecnologia em Redes de Computadores",
            "descricao": "Tecnologia em Redes de Computadores - Nome Completo do Campus",
        },
        "turma": {"id": 1, "codigo": "20221.6.00001.1E"},
        "componente": {
            "id": 1,
            "sigla": "TEC.0001",
            "descricao": "Bancos de Dados",
            "descricao_historico": "Bancos de Dados",
            "periodo": None,
            "tipo": 1,
            "optativo": False,
            "qtd_avaliacoes": 2,
        },
        "diario": {
            "id": 1,
            "situacao": "Aberto",
            "descricao": "Bancos de Dados",
            "descricao_historico": "Bancos de Dados",
            "sigla": "TEC.0001",
        },
        "professores": [
            {
                "id": 1,
                "login": "1234567",
                "nome": "Nome completo de um professor principal",
                "email": "nome.sobrenome@ifrn.edu.br",
                "email_secundario": "nome.sobrenome@gmail.com",
                "status": "ativo",
                "tipo": "Principal",
            }
        ],
        "alunos": [
            {
                "id": 1,
                "matricula": "201830000100001",
                "nome": "Nome completo do aluno",
                "email": "nome.compelto@academico.ifrn.edu.br",
                "email_secundario": "nome.completo@hotmail.com",
                "situacao": "ativo",
                "polo": {"id": 1, "descricao": "Pólo Assú"},
            }
        ],
    }


class Diario(SafeDeleteModel):
    # suap_id = CharField(_('ID do diário no SUAP'), max_length=255, unique=True)
    # codigo = CharField(_('código do diário'), max_length=255, unique=True)
    pacote_enviado = JSONField(_("pacote a enviar/enviado"), default=get_default_pacote)
    pacote_recebido = JSONField(_("pacote recebido"), null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("diário fake")
        verbose_name_plural = _("diários fake")
        ordering = ["id"]

    def __str__(self):
        return f'{self.pacote_enviado["turma"]["codigo"]}.{self.pacote_enviado["diario"]["sigla"]}'
