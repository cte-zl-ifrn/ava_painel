from django.utils.translation import gettext as _
import re
import json
import requests
from django.utils.timezone import now
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core import validators
from django.forms import ValidationError
from django.db.models import (
    ForeignKey,
    PROTECT,
    BooleanField,
    URLField,
    CharField,
    DateTimeField,
    IntegerField,
    SmallIntegerField,
)
from django_better_choices import Choices
from simple_history.models import HistoricalRecords
from safedelete.models import SafeDeleteModel
from djrichtextfield.models import RichTextField
from a4.models import Usuario, TipoUsuario
from middleware.models import Solicitacao
from portal import request2dict


class SyncError(Exception):
    def __init__(self, message, code, campus=None, retorno=None, params=None):
        super().__init__(message, code, params)
        self.message = message
        self.code = code
        self.campus = campus
        self.retorno = retorno


class Turno(Choices):
    NOTURNO = Choices.Value(_("Noturno"), value="N")
    VESPERTINO = Choices.Value(_("Vespertino"), value="V")
    MATUTINO = Choices.Value(_("Matutino"), value="M")
    EAD = Choices.Value(_("EAD"), value="E")
    DIURNO = Choices.Value(_("Diurno"), value="D")
    INTEGRAL = Choices.Value(_("Integral"), value="I")
    DESCONHECIDO = Choices.Value(_("Desconhecido"), value="_")


Turno.kv = [{"id": p, "label": p.display} for p in Turno.values()]


class Contexto(Choices):
    CURSO = Choices.Value(_("Curso"), value="c")
    POLO = Choices.Value(_("Pólo"), value="p")


Contexto.kv = [{"id": p, "label": p.display} for p in Contexto.values()]


class ActiveMixin:
    @property
    def active_icon(self):
        return "✅" if self.active else "⛔"


class Arquetipo(Choices):
    ALUNO = Choices.Value(_("Aluno"), value="student")
    PROFESSOR = Choices.Value(_("Professor"), value="editingteacher")
    TUTOR = Choices.Value(_("Tutor"), value="teacher")
    EQUIPE = Choices.Value(_("Coordenador"), value="manager")
    CONTEUDISTA = Choices.Value(_("Conteudista"), value="coursecreator")


Arquetipo.kv = [{"id": p, "label": p.display} for p in Arquetipo.values()]


class Situacao(Choices):
    IN_PROGRESS = Choices.Value(_("✳️ Diários em andamento"), value="inprogress")
    FUTURE = Choices.Value(_("🗓️ Diários a iniciar"), value="future")
    PAST = Choices.Value(_("📕 Encerrados pelo professor"), value="past")
    FAVOURITES = Choices.Value(_("⭐ Meus diários favoritos"), value="favourites")
    ALL = Choices.Value(_("♾️ Todos os diários (lento)"), value="allincludinghidden")


Situacao.kv = [{"id": p, "label": p.display} for p in Situacao.values()]


class Ordenacao(Choices):
    CURSO = Choices.Value(_("📗 Ordenado por nome da disciplina"), value="fullname")
    CODIGO = Choices.Value(_("🔢 Ordenado por código do diário"), value="shortname")
    # ULTIMO_ACESSO = Choices.Value(
    #     _("🕓 Ordenado pelo último acessado"), value="ul.timeaccess desc"
    # )


Ordenacao.kv = [{"id": p, "label": p.display} for p in Ordenacao.values()]


class Visualizacao(Choices):
    ROWS = Choices.Value(_("Ver como linhas"), value="list")
    CARDS = Choices.Value(_("Ver como cartões"), value="cards")


Visualizacao.kv = [{"id": p, "label": p.display} for p in Visualizacao.values()]


class Ambiente(SafeDeleteModel):
    def _c(color: str):
        return f"<span style='background: {color}; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>{color}</span>"

    sigla = CharField(
        _("sigla do ambiente"),
        max_length=255,
        unique=True,
        help_text=mark_safe(f"Esta é a sigla que vai aparecer no dashboard"),
    )
    cor_mestra = CharField(
        _("cor mestra"),
        max_length=255,
        help_text=mark_safe(
            f"Escolha uma cor em RGB. Ex.: {_c('#a04ed0')} {_c('#396ba7')} {_c('#559c1a')} {_c('#fabd57')} {_c('#fd7941')} {_c('#f54f3b')} {_c('#2dcfe0')}"
        ),
    )
    cor_degrade = CharField(
        _("cor do degradê"),
        max_length=255,
        help_text=mark_safe(
            f"Escolha uma cor em RGB. Ex.: {_c('#53296d')} {_c('#203d60')} {_c('#315810')} {_c('#ae8133')} {_c('#d05623')} {_c('#fd7941')} {_c('#09afc0')}"
        ),
    )
    cor_progresso = CharField(
        _("cor do progresso"),
        max_length=255,
        help_text=mark_safe(
            f"Escolha uma cor em RGB. Ex.: {_c('#ecdafa')} {_c('#b4d0f2')} {_c('#d2f4b7')} {_c('#ffebca')} {_c('#ffd1be')} {_c('#ffbab2')} {_c('#d2f2f5')}"
        ),
    )
    nome = CharField(_("nome do ambiente"), max_length=255)
    url = CharField(_("URL"), max_length=255)
    token = CharField(_("token"), max_length=255)
    active = BooleanField(_("ativo?"), default=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("ambiente")
        verbose_name_plural = _("ambientes")
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome}"

    @property
    def base_url(self):
        return self.url if self.url[-1:] != "/" else self.url[:-1]

    @property
    def base_api_url(self):
        return f"{self.base_url}/local/suap/api"

    @staticmethod
    def as_dict():
        return [
            {
                "id": a.id,
                "label": a.nome,
                "sigla": a.sigla,
                "style": f"background-color: {a.cor_degrade}",
                "color": a.cor_degrade,
            }
            for a in Ambiente.objects.filter(active=True)
        ]

    @staticmethod
    def admins():
        return [
            {
                "id": a.id,
                "nome": re.subn("🟥 |🟦 |🟧 |🟨 |🟩 |🟪 ", "", a.nome)[0],
                "cor_mestra": a.cor_mestra,
                "cor_degrade": a.cor_degrade,
                "cor_progresso": a.cor_progresso,
                "url": f"{a.url}/admin/",
            }
            for a in Ambiente.objects.filter(active=True)
        ]


class Campus(SafeDeleteModel):
    suap_id = CharField(_("ID do campus no SUAP"), max_length=255, unique=True)
    sigla = CharField(_("sigla do campus"), max_length=255, unique=True)
    descricao = CharField(_("descrição"), max_length=255)
    ambiente = ForeignKey(Ambiente, on_delete=PROTECT)
    active = BooleanField(_("ativo?"))

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("campus")
        verbose_name_plural = _("campi")
        ordering = ["sigla"]

    def __str__(self):
        return f"{self.descricao} ({self.sigla})"


class Curso(SafeDeleteModel):
    suap_id = CharField(_("ID do curso no SUAP"), max_length=255, unique=True)
    codigo = CharField(_("código do curso"), max_length=255, unique=True)
    nome = CharField(_("nome do curso"), max_length=255)
    descricao = CharField(_("descrição"), max_length=255)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("curso")
        verbose_name_plural = _("cursos")
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.codigo})"


class Turma(SafeDeleteModel):
    TURMA_RE = re.compile(r"(\d{5})\.(\d)\.(\d{5})\.(..)")
    suap_id = CharField(_("ID da turma no SUAP"), max_length=255, unique=True)
    campus = ForeignKey(Campus, on_delete=PROTECT, verbose_name=_("campus"))
    codigo = CharField(
        _("código da turma"),
        max_length=255,
        unique=True,
        validators=[validators.RegexValidator(TURMA_RE)],
    )

    curso = ForeignKey(Curso, on_delete=PROTECT, verbose_name=_("curso"))
    ano_mes = SmallIntegerField(verbose_name=_("ano/mês"))
    periodo = SmallIntegerField(_("período"))
    sigla = CharField(_("sigla da turma"), max_length=8)
    turno = CharField(_("turno"), max_length=1, choices=Turno)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("turma")
        verbose_name_plural = _("turmas")
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo}"

    def save(self, *args, **kwargs):
        parts = Turma.TURMA_RE.findall(self.codigo)[0]
        self.ano_mes = parts[0]
        self.periodo = parts[1]
        self.curso = Curso.objects.get(codigo=parts[2])
        self.sigla = parts[3]
        self.turno = self.sigla[-1:] if self.sigla[-1:] in Turno else "_"
        super().save(*args, **kwargs)


class Componente(SafeDeleteModel):
    suap_id = CharField(_("ID do componente no SUAP"), max_length=255, unique=True)
    sigla = CharField(_("sigla do componente"), max_length=255, unique=True)
    descricao = CharField(_("descrição"), max_length=512)
    descricao_historico = CharField(_("descrição no histórico"), max_length=512)
    periodo = IntegerField(_("período"), null=True, blank=True)
    tipo = IntegerField(_("tipo"), null=True, blank=True)
    optativo = BooleanField(_("optativo"), null=True, blank=True)
    qtd_avaliacoes = IntegerField(_("qtd. avalições"), null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("componente")
        verbose_name_plural = _("componentes")
        ordering = ["sigla"]

    def __str__(self):
        return f"{self.sigla}"


class Diario(SafeDeleteModel):
    DIARIO_RE = re.compile(r"(\d{5}\.\d\.\d{5}\...)\.(.*\..*)")
    suap_id = CharField(_("ID do diário no SUAP"), max_length=255, unique=True)
    codigo = CharField(
        _("código do diário"),
        max_length=255,
        unique=True,
        validators=[validators.RegexValidator(DIARIO_RE)],
    )
    situacao = CharField(_("situação"), max_length=255)
    descricao = CharField(_("descrição"), max_length=255)
    descricao_historico = CharField(_("descrição no histórico"), max_length=255)
    turma = ForeignKey(Turma, on_delete=PROTECT, verbose_name=_("turma"))
    componente = ForeignKey(Componente, on_delete=PROTECT, verbose_name=_("componente"))

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("diário")
        verbose_name_plural = _("diários")
        ordering = ["codigo"]

    def save(self, *args, **kwargs):
        parts = Diario.DIARIO_RE.findall(self.codigo)[0]
        self.turma = Turma.objects.get(codigo=parts[0])
        self.componente = Componente.objects.get(sigla=parts[1])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo}"

    @classmethod
    def sync(cls, message_string, headers):
        def _validate_campus():
            try:
                pkg = json.loads(message_string)
            except Exception as e:
                raise SyncError(f"O JSON está inválido: {e} {message_string}.", 407)

            try:
                filter = {
                    "suap_id": pkg["campus"]["id"],
                    "sigla": pkg["campus"]["sigla"],
                    "active": True,
                }
            except:
                raise SyncError(f"O JSON não tinha a estrutura definida.", 406)

            campus = Campus.objects.filter(**filter).first()
            if campus is None:
                raise SyncError(
                    f"Não existe um campus com o id '{filter['suap_id']}' e a sigla '{filter['sigla']}'.",
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
                    f"O campus '{filter['sigla']}' existe e está ativo, mas o ambiente {campus.ambiente.sigla} está inativo.",
                    417,
                    campus,
                )
            return campus, pkg

        campus, pkg = _validate_campus()
        try:
            retorno = requests.post(
                f"{campus.ambiente.url}/local/suap/api/sync_up_enrolments.php",
                data={"jsonstring": message_string},
                headers={"Authentication": f"Token {campus.ambiente.token}"},
            )
        except Exception as e:
            raise SyncError(f"Erro na integração. O Moodle disse: {e}", 513, campus)

        retorno_json = None
        if retorno.status_code != 200:
            try:
                retorno_json = json.loads(retorno.text)
            except Exception as e:
                error_text = ""
                # error_text = (
                #     re.sub("<[^<]+?>", "", retorno.text)
                #     .replace("  ", " ")
                #     .replace("\n", " ")
                # )
                raise SyncError(
                    f"Erro na integração. Contacte um administrador. Erro: {e}. {error_text}",
                    retorno.status_code,
                    campus,
                    retorno,
                )

        try:
            retorno_json = json.loads(retorno.text)
        except Exception as ie:
            raise SyncError(
                f"Erro na integração ({ie}). Contacte um desenvolvedor.",
                retorno.status_code,
                campus,
                retorno,
            )

        Solicitacao.objects.create(
            requisicao_header=headers,
            requisicao=message_string,
            resposta_header=request2dict(retorno),
            resposta=retorno_json,
            status=Solicitacao.Status.SUCESSO,
            status_code=retorno.status_code,
            campus=campus,
        )

        try:
            Diario.make(pkg)
        except Exception as e:
            raise SyncError(
                f"Erro na integração. Contacte um administrador. {e}",
                512,
                campus,
                retorno,
            )

        return retorno_json

    @classmethod
    def make(cls, d):
        def get_polo_id(person):
            if (
                "polo" in person
                and person["polo"]
                and not isinstance(person["polo"], int)
            ):
                return person["polo"]["id"]
            else:
                return None

        campus = Campus.objects.get(suap_id=d["campus"]["id"])

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
        #     if get_polo_id(p) and get_polo_id(p) not in polos:
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
            polo = polos.get(get_polo_id(p), None)

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


class Polo(SafeDeleteModel):
    suap_id = CharField(_("ID do pólo no SUAP"), max_length=255, unique=True)
    nome = CharField(_("nome do pólo"), max_length=255, unique=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("pólo")
        verbose_name_plural = _("pólos")
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome}"


class Inscricao(SafeDeleteModel):
    diario = ForeignKey(Diario, on_delete=PROTECT)
    usuario = ForeignKey(settings.AUTH_USER_MODEL, on_delete=PROTECT)
    polo = ForeignKey(Polo, on_delete=PROTECT, null=True, blank=True)
    papel = CharField(_("papel"), max_length=256, choices=Arquetipo)
    active = BooleanField(_("ativo?"))

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("inscrição")
        verbose_name_plural = _("inscrições")
        ordering = ["diario", "usuario"]

    @property
    def active_icon(self):
        return "✅" if self.active else "⛔"

    def __str__(self):
        return f"{self.diario} - {self.usuario} - {self.papel} - {self.active}"

    def notify(self):
        pass


class Popup(ActiveMixin, SafeDeleteModel):
    titulo = CharField(_("título"), max_length=256)
    url = URLField(_("url"), max_length=256)
    mensagem = RichTextField(_("mensagem"))
    start_at = DateTimeField(_("inicia em"))
    end_at = DateTimeField(_("termina em"))
    active = BooleanField(_("ativo?"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("popup")
        verbose_name_plural = _("popups")
        ordering = ["start_at", "titulo"]

    def __str__(self):
        return f"{self.titulo} - {self.active_icon}"

    def save(self, *args, **kwargs):
        if self.start_at > self.end_at:
            return ValidationError("O término deve ser maior do que o início.")
        super().save(*args, **kwargs)

    def mostrando(self):
        return self.active and self.start_at <= now() and self.end_at >= now()

    @staticmethod
    def activePopup():
        return Popup.objects.filter(
            active=True, start_at__lte=now(), end_at__gte=now()
        ).first()


class Papel(ActiveMixin, SafeDeleteModel):
    nome = CharField(_("nome do papel"), max_length=256)
    sigla = CharField(_("sigla"), max_length=10, blank=True, null=False, unique=True)
    contexto = CharField(_("contexto"), max_length=1, choices=Contexto)
    active = BooleanField(_("ativo?"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("papel")
        verbose_name_plural = _("papéis")
        ordering = ["nome"]

    def __str__(self):
        return f"{self.sigla}:{self.nome} {self.active_icon}"


class Popup(ActiveMixin, SafeDeleteModel):
    titulo = CharField(_("título"), max_length=256)
    url = URLField(_("url"), max_length=256)
    mensagem = RichTextField(_("mensagem"))
    start_at = DateTimeField(_("inicia em"))
    end_at = DateTimeField(_("termina em"))
    active = BooleanField(_("ativo?"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("popup")
        verbose_name_plural = _("popups")
        ordering = ["start_at", "titulo"]

    def __str__(self):
        return f"{self.titulo} - {self.active_icon}"

    def save(self, *args, **kwargs):
        if self.start_at > self.end_at:
            return ValidationError("O término deve ser maior do que o início.")
        super().save(*args, **kwargs)

    def mostrando(self):
        return self.active and self.start_at <= now() and self.end_at >= now()

    @staticmethod
    def activePopup():
        return Popup.objects.filter(
            active=True, start_at__lte=now(), end_at__gte=now()
        ).first()


class Papel(ActiveMixin, SafeDeleteModel):
    nome = CharField(_("nome do papel"), max_length=256)
    sigla = CharField(_("sigla"), max_length=10, blank=True, null=False, unique=True)
    contexto = CharField(_("contexto"), max_length=1, choices=Contexto)
    active = BooleanField(_("ativo?"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("papel")
        verbose_name_plural = _("papéis")
        ordering = ["sigla"]

    def __str__(self):
        return f"{self.sigla}:{self.nome} {self.active_icon}"


class VinculoPolo(ActiveMixin, SafeDeleteModel):
    papel = ForeignKey(
        Papel, on_delete=PROTECT, limit_choices_to={"contexto": Contexto.POLO}
    )
    polo = ForeignKey(Polo, on_delete=PROTECT)
    colaborador = ForeignKey(
        Usuario,
        on_delete=PROTECT,
        related_name="vinculos_polos",
        limit_choices_to={"tipo_usuario__in": [TipoUsuario.ALUNO]},
    )
    active = BooleanField(_("ativo?"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("vínculo no pólo")
        verbose_name_plural = _("vínculos nos pólos")
        ordering = ["papel", "polo", "colaborador"]

    def __str__(self):
        return f"{self.papel}:{self.polo} {self.colaborador} {self.active_icon}"


class VinculoCurso(ActiveMixin, SafeDeleteModel):
    papel = ForeignKey(
        Papel, on_delete=PROTECT, limit_choices_to={"contexto": Contexto.CURSO}
    )
    curso = ForeignKey(Curso, on_delete=PROTECT)
    colaborador = ForeignKey(
        Usuario,
        on_delete=PROTECT,
        related_name="vinculos_cursos",
        limit_choices_to={"tipo_usuario__in": TipoUsuario.COLABORADORES_KEYS},
    )
    active = BooleanField(_("ativo?"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("vínculo no curso")
        verbose_name_plural = _("vínculos nos cursos")
        ordering = ["papel", "curso", "colaborador"]

    def __str__(self):
        return f"{self.papel}:{self.curso} {self.colaborador} {self.active_icon}"


class CursoPolo(ActiveMixin, SafeDeleteModel):
    curso = ForeignKey(Curso, on_delete=PROTECT)
    polo = ForeignKey(Polo, on_delete=PROTECT)
    active = BooleanField(_("ativo?"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("pólo do curso")
        verbose_name_plural = _("pólos do curso")
        ordering = ["curso", "polo"]

    def __str__(self):
        return f"{self.curso}:{self.polo} {self.active_icon}"
