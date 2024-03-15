from django.utils.translation import gettext as _
import json
import requests
from django.db.models import Manager
from middleware.models import Solicitacao
from a4.models import Usuario


class SyncError(Exception):
    def __init__(self, message, code, campus=None, retorno=None, params=None):
        super().__init__(message, code, params)
        self.message = message
        self.code = code
        self.campus = campus
        self.retorno = retorno


class DiarioManager(Manager):
    def _validate_campus(self, message: str):
        from painel.models import Campus

        try:
            pkg = json.loads(message)
        except Exception as e:
            raise SyncError(f"O JSON está inválido: {e} {message}.", 407)

        try:
            filter = {
                "suap_id": pkg["campus"]["id"],
                "sigla": pkg["campus"]["sigla"],
                "active": True,
            }
        except Exception:
            raise SyncError("O JSON não tinha a estrutura definida.", 406)

        campus = Campus.objects.filter(**filter).first()
        if campus is None:
            raise SyncError(
                f"""Não existe um campus com o id '{filter['suap_id']}'
                                e a sigla '{filter['sigla']}'.""",
                404,
            )

        if not campus.active:
            raise SyncError(
                f"O campus '{filter['sigla']}' existe, mas está inativo.",
                412,
            )

        if not campus.ambiente.active:
            raise SyncError(
                f"""O campus '{filter['sigla']}' existe e está ativo, mas o ambiente {campus.ambiente.nome} está inativo.""",  # noqa
                417,
            )
        return campus, pkg

    def sync(self, recebido: str):
        from painel.models import (
            Curso,
        )

        retorno_json = None
        retorno = None
        campus = None
        solicitacao = Solicitacao.objects.create(
            recebido=json.loads(recebido),
            enviado=None,
            respondido=None,
            status=Solicitacao.Status.PROCESSANDO,
            status_code=None,
            campus=None,
        )

        try:
            campus, pkg = self._validate_campus(recebido)
            curso = Curso.objects.filter(codigo=pkg["curso"]["codigo"]).first()
            solicitacao.campus = campus
            solicitacao.enviado = dict(*pkg, *{"coortes": curso.coortes}) if curso else pkg
            solicitacao.save()

            retorno = requests.post(
                f"{campus.ambiente.url}/local/suap/api/?sync_up_enrolments",
                json=solicitacao.enviado,
                headers={"Authentication": f"Token {campus.ambiente.token}"},
            )

            try:
                solicitacao.respondido = json.loads(retorno.text)
            except Exception as e:
                solicitacao.respondido = {"error": f"{e}"}

            solicitacao.status = Solicitacao.Status.SUCESSO
            solicitacao.status_code = retorno.status_code
            solicitacao.save()

            # self._make(campus, pkg)

            return solicitacao
        except Exception as e:
            error_message = getattr(retorno, "text", "-")
            error_text = f"""
                Erro na integração. O AVA retornou um erro.
                Contacte um administrador.
                Erro: {e}.
                Cause: {error_message}
            """
            solicitacao.respondido = {"error": {"error_message": f"{e}", "error": f"{error_message}"}}
            solicitacao.status = Solicitacao.Status.FALHA
            solicitacao.status_code = getattr(e, "code", 500)
            solicitacao.save()
            raise SyncError(error_text, solicitacao.status_code)

    def _get_polo_id(self, person):
        if "polo" in person and person["polo"] and not isinstance(person["polo"], int):
            return person["polo"]["id"]
        else:
            return None

    def _make(self, campus, d):
        from painel.models import (
            Diario,
            Turma,
            Componente,
            Curso,
            Arquetipo,
            Inscricao,
            Polo,
        )

        curso, created = Curso.objects.update_or_create(
            codigo=d["curso"]["codigo"],
            defaults={
                "suap_id": d["curso"]["id"],
                "nome": d["curso"]["nome"],
                "descricao": d["curso"]["descricao"],
            },
        )
        turma, created = Turma.objects.update_or_create(
            codigo=d["turma"]["codigo"],
            defaults={
                "suap_id": d["turma"]["id"],
                "campus": campus,
            },
        )
        componente, created = Componente.objects.update_or_create(
            sigla=d["componente"]["sigla"],
            defaults={
                "suap_id": d["componente"]["id"],
                "descricao": d["componente"]["descricao"],
                "descricao_historico": d["componente"]["descricao_historico"],
                "periodo": d["componente"]["periodo"],
                "tipo": d["componente"]["tipo"],
                "optativo": d["componente"]["optativo"],
                "qtd_avaliacoes": d["componente"]["qtd_avaliacoes"],
            },
        )

        diario, created = Diario.objects.update_or_create(
            codigo=turma.codigo + "." + d["diario"]["sigla"],
            defaults={
                "suap_id": d["diario"]["id"],
                "situacao": d["diario"]["situacao"],
                "descricao": d["diario"]["descricao"],
                "descricao_historico": d["diario"]["descricao_historico"],
                "turma": turma,
                "componente": componente,
            },
        )

        pessoas = d.get("professores", []) + d.get("alunos", [])
        polos = {}
        for p in pessoas:
            if self._get_polo_id(p) and self._get_polo_id(p) not in polos:
                polo, created = Polo.objects.update_or_create(
                    suap_id=p["polo"]["id"],
                    defaults={"nome": p["polo"].get("descricao", None)},
                )
                polos[p["polo"]["id"]] = polo

        for p in pessoas:
            if "matricula" in p.keys():
                papel = Arquetipo.ALUNO
            else:
                papel = Arquetipo.PROFESSOR if p["tipo"] == "Principal" else Arquetipo.TUTOR
            polo = polos.get(self._get_polo_id(p), None)

            is_active = "ativo" == p.get("situacao", p.get("status", "")).lower()
            username = p.get("login", p.get("matricula", None))
            usuario, created = Usuario.objects.update_or_create(
                username=username,
                defaults={
                    "nome_registro": p["nome"],
                    # 'email': p['email'],
                    # 'email_secundario': p.get('email_secundario', None),
                    "is_active": is_active,
                    "polo": polo,
                    "curso": curso if papel == Arquetipo.ALUNO else None,
                },
            )
            inscricao, created = Inscricao.objects.update_or_create(
                diario=diario,
                usuario=usuario,
                defaults={
                    "polo": polo,
                    "papel": papel,
                    "active": is_active,
                },
            )
            if created:
                inscricao.notify()
        return diario
