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
                campus,
            )

        if not campus.ambiente.active:
            raise SyncError(
                f"""O campus '{filter['sigla']}' existe e está ativo, mas o ambiente
                    {campus.ambiente.sigla} está inativo.""",
                417,
                campus,
            )
        return campus, pkg

    def sync(self, message: str):
        retorno_json = None
        retorno = None
        campus = None
        try:
            campus, pkg = self._validate_campus(message)
            retorno = requests.post(
                f"{campus.ambiente.url}/local/suap/api/?sync_up_enrolments",
                data={"jsonstring": message},
                headers={"Authentication": f"Token {campus.ambiente.token}"},
            )

            return retorno.text
            retorno_json = json.loads(retorno.text)

            Solicitacao.objects.create(
                recebido=message,
                enviado=message,
                respondido=retorno_json,
                status=Solicitacao.Status.SUCESSO,
                status_code=retorno.status_code,
                campus=campus,
            )

            return self._make(campus, pkg)
        except Exception as e:
            print(e)
            error_text = getattr(retorno, "text", "-")
            raise SyncError(
                f"""Erro na integração. O AVA retornou um erro.
                    Contacte um administrador.
                    Erro: {e}.
                    Cause: {error_text}""",
                getattr(retorno, "status_code", 500),
                campus,
                retorno,
            )

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

        pessoas = d["professores"] + d["alunos"]
        polos = {}
        # for p in pessoas:
        #     if self._get_polo_id(p) and self._get_polo_id(p) not in polos:
        #         polo, created = Polo.objects.update_or_create(
        #             suap_id=p['polo']['id'],
        #             defaults={'nome': p['polo']['nome']}
        #         )
        #         polos[p['polo']['id']] = polo

        for p in pessoas:
            if "matricula" in p.keys():
                papel = Arquetipo.ALUNO
            else:
                papel = (
                    Arquetipo.PROFESSOR if p["tipo"] == "Principal" else Arquetipo.TUTOR
                )
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
