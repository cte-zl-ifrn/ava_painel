from django.utils.translation import gettext as _
import json
import re
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


class BaseChoices(Choices):
    @classmethod
    @property
    def kv(cls):
        return [{"id": p, "label": p.display} for p in Contexto.values()]


class Contexto(Choices):
    CURSO = Choices.Value(_("Curso"), value="c")
    POLO = Choices.Value(_("Pólo"), value="p")


class Situacao(Choices):
    IN_PROGRESS = Choices.Value(_("✳️ Diários em andamento"), value="inprogress")
    FUTURE = Choices.Value(_("🗓️ Diários a iniciar"), value="future")
    PAST = Choices.Value(_("📕 Encerrados pelo professor"), value="past")
    FAVOURITES = Choices.Value(_("⭐ Meus diários favoritos"), value="favourites")
    ALL = Choices.Value(_("♾️ Todos os diários (lento)"), value="allincludinghidden")


class Ordenacao(Choices):
    CURSO = Choices.Value(_("📗 Ordenado por nome da disciplina"), value="fullname")
    CODIGO = Choices.Value(_("🔢 Ordenado por código do diário"), value="shortname")


class Visualizacao(Choices):
    ROWS = Choices.Value(_("Ver como linhas"), value="list")
    CARDS = Choices.Value(_("Ver como cartões"), value="cards")


class ActiveMixin:
    @property
    def active_icon(self):
        return "✅" if self.active else "⛔"


class Ambiente(SafeDeleteModel):
    def _c(color: str):
        return f"""<span style='background: {color}; color: #fff; padding: 1px 5px;
                                font-size: 95%; border-radius: 4px;'>{color}</span>"""

    cor_mestra = CharField(
        _("cor mestra"),
        max_length=255,
        help_text=mark_safe(
            f"""Escolha uma cor em RGB.
                Ex.: {_c('#a04ed0')} {_c('#396ba7')} {_c('#559c1a')}
                {_c('#fabd57')} {_c('#fd7941')} {_c('#f54f3b')} {_c('#2dcfe0')}"""
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
                "style": f"background-color: {a.cor_mestra}",
                "color": a.cor_mestra,
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
                "url": f"{a.url}/admin/",
            }
            for a in Ambiente.objects.filter(active=True)
        ]


class Campus(SafeDeleteModel):
    suap_id = CharField(_("ID do campus no SUAP"), max_length=255, unique=True)
    sigla = CharField(_("sigla do campus"), max_length=255, unique=True)
    ambiente = ForeignKey(Ambiente, on_delete=PROTECT)
    active = BooleanField(_("ativo?"))

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("campus")
        verbose_name_plural = _("campi")
        ordering = ["sigla"]

    def __str__(self):
        return self.sigla


class Papel(ActiveMixin, SafeDeleteModel):
    nome = CharField(_("nome do papel"), max_length=256)
    sigla = CharField(_("sigla"), max_length=10, blank=True, null=False, unique=True)
    papel = CharField(_("papel"), max_length=256, unique=True)
    contexto = CharField(_("contexto"), max_length=1, choices=Contexto)
    active = BooleanField(_("ativo?"))

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("papel")
        verbose_name_plural = _("papéis")
        ordering = ["nome"]

    def __str__(self):
        sigla = f"{self.sigla}:" if self.sigla else ""
        return f"{sigla}{self.nome} {self.active_icon}"


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

    def __codigo_papel(self, papel):
        return f".{papel.sigla}" if papel.sigla else ""

    @property
    def coortes(self):
        cohorts = {}

        try:

            def dados_coorte(v, campus):
                campus_curso = f"{campus.sigla}.{self.codigo}"
                id = f"{campus_curso}{self.__codigo_papel(v.papel)}"
                return {
                    "idnumber": id,
                    "nome": f"{campus_curso} - {v.papel.nome}",
                    "descricao": f"{v.papel.nome}: {campus_curso} - {self.nome}",
                    "ativo": v.active,
                    "colaboradores": [],
                    "role": v.papel.papel,
                }

            def dados_colaborador(vc):
                return {
                    "login": vc.colaborador.username,
                    "email": vc.colaborador.email,
                    "nome": vc.colaborador.show_name,
                    "status": "Ativo" if vc.active else "Inativo",
                }

            for vc in self.vinculocurso_set.all():
                campus_curso = f"{vc.campus.sigla}.{self.codigo}"
                id = f"{campus_curso}{self.__codigo_papel(vc.papel)}"
                if id not in cohorts:
                    cohorts[id] = dados_coorte(vc, vc.campus)
                cohorts[id]["colaboradores"].append(dados_colaborador(vc))

            for cp in self.cursopolo_set.all():
                campus_curso = f"{cp.campus.sigla}.{self.codigo}"
                for vp in cp.polo.vinculopolo_set.all():
                    id = f"{campus_curso}{self.__codigo_papel(vp.papel)}"
                    if id not in cohorts:
                        cohorts[id] = cohorts[id] = dados_coorte(vp, cp.campus)
                    cohorts[id]["colaboradores"].append(dados_colaborador(vc))
        finally:
            return [c for c in cohorts.values()]


class VinculoCurso(ActiveMixin, SafeDeleteModel):
    campus = ForeignKey(Campus, on_delete=PROTECT)
    curso = ForeignKey(Curso, on_delete=PROTECT)
    papel = ForeignKey(Papel, on_delete=PROTECT, limit_choices_to={"contexto": Contexto.CURSO})
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
        verbose_name_plural = _("cursos x colaboradores")
        ordering = ["papel", "curso", "colaborador"]

    def __str__(self):
        return f"{self.papel}{self.curso} {self.colaborador} {self.active_icon}"


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


class CursoPolo(ActiveMixin, SafeDeleteModel):
    curso = ForeignKey(Curso, on_delete=PROTECT)
    campus = ForeignKey(Campus, on_delete=PROTECT)
    polo = ForeignKey(Polo, on_delete=PROTECT)
    active = BooleanField(_("ativo?"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("pólo do curso")
        verbose_name_plural = _("pólos x cursos")
        ordering = ["curso", "polo"]

    def __str__(self):
        return f"{self.curso}:{self.polo} {self.active_icon}"


class VinculoPolo(ActiveMixin, SafeDeleteModel):
    papel = ForeignKey(Papel, on_delete=PROTECT, limit_choices_to={"contexto": Contexto.POLO})
    polo = ForeignKey(Polo, on_delete=PROTECT)
    colaborador = ForeignKey(
        Usuario,
        on_delete=PROTECT,
        related_name="vinculos_polos",
        limit_choices_to={"tipo_usuario__in": TipoUsuario.COLABORADORES_KEYS},
    )
    active = BooleanField(_("ativo?"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("vínculo no pólo")
        verbose_name_plural = _("pólos X colaboradores")
        ordering = ["papel", "polo", "colaborador"]

    def __str__(self):
        return f"{self.papel}{self.polo} {self.colaborador} {self.active_icon}"


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
        return Popup.objects.filter(active=True, start_at__lte=now(), end_at__gte=now()).first()
