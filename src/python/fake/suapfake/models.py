from tokenize import blank_re
from django.utils.translation import gettext as _
from django.conf import settings
from django.db.models import Model, CharField, JSONField
from pyparsing import null_debug_action
from traitlets import default


DEFAULT_PACKAGE = {
    "campus": {
        "id": 1,
        "descricao": "NOME COMPLETO DO CAMPUS",
        "sigla": "NCC"
    },
    "curso": {
        "id": 1,
        "codigo": "00001",
        "nome": "Tecnologia em Redes de Computadores",
        "descricao": "Tecnologia em Redes de Computadores - Nome Completo do Campus"
    },
    "turma": {
        "id": 1,
        "codigo": "20221.6.00001.1E"
    },
    "diario": {
        "id": 1,
        "situacao": "Aberto",
        "descricao": "Bancos de Dados",
        "descricao_historico": "Bancos de Dados",
        "sigla": "TEC.0001"
    },
    "professores": [
        {
            "id": 1,
            "login": "1234567",
            "nome": "Nome completo de um professor principal",
            "email": "nome.sobrenome@ifrn.edu.br",
            "email_secundario": "nome.sobrenome@gmail.com",
            "status": "ativo",
            "tipo": "Principal"
        }
    ],
    "alunos": [
        {
            "id": 1,
            "matricula": "20183000010001",
            "nome": "Nome completo do aluno",
            "email": "nome.compelto@academico.ifrn.edu.br",
            "email_secundario": "nome.completo@hotmail.com",
            "situacao": "ativo",
            "polo": None
        }
    ],
    "polo": None,
    "componente": {
        "id": 1,
        "sigla": "TEC.0001",
        "descricao": "Bancos de Dados",
        "descricao_historico": "Bancos de Dados",
        "periodo": None,
        "tipo": 1,
        "optativo": False,
        "qtd_avaliacoes": 2
    }
}

class Diario(Model):
    # suap_id = CharField(_('ID do diário no SUAP'), max_length=255, unique=True)
    # codigo = CharField(_('código do diário'), max_length=255, unique=True)
    pacote_enviado = JSONField(_('pacote a enviar/enviado'), default=DEFAULT_PACKAGE)
    pacote_recebido = JSONField(_('pacote recebido'), null=True, blank=True)
    
    class Meta:
        verbose_name = _("diário")
        verbose_name_plural = _("diários")
        ordering = ['id']

    def __str__(self):
        return f'{self.pacote_enviado["turma"]["codigo"]}.{self.pacote_enviado["diario"]["sigla"]}'
