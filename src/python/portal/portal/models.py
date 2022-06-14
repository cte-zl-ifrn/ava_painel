from django.utils.translation import gettext as _
import re
from django.conf import settings
from django.core import validators
from django.forms import ValidationError
from django.db.models import Model, ForeignKey, PROTECT, BooleanField
from django.db.models import CharField, URLField, ImageField, DateTimeField, IntegerField, SmallIntegerField
from django_better_choices import Choices
from a4.models import Usuario


class Turno(Choices):
    NOTURNO = Choices.Value(_("Noturno"), value='N')
    VESPERTINO = Choices.Value(_("Vespertino"), value='V')
    MATUTINO = Choices.Value(_("Matutino"), value='M')
    EAD = Choices.Value(_("EAD"), value='E')
    DIURNO = Choices.Value(_("Diurno"), value='D')
    INTEGRAL = Choices.Value(_("Integral"), value='I')
    DESCONHECIDO = Choices.Value(_("Desconhecido"), value='_')


class Papel(Choices):
    ALUNO = Choices.Value(_("Aluno"), value='A')
    PROFESSOR = Choices.Value(_("Professor"), value='P')
    TUTOR_REMOTO = Choices.Value(_("Tutor remoto"), value='R')


class Ambiente(Model):
    sigla = CharField(_('sigla do ambiente'), max_length=255, unique=True)
    nome = CharField(_('nome do ambiente'), max_length=255)
    url = CharField(_('URL'), max_length=255)
    token = CharField(_('token'), max_length=255)
    active = BooleanField(_('ativo?'), default=True)

    class Meta:
        verbose_name = _("ambiente")
        verbose_name_plural = _("ambientes")
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome}'


class Campus(Model):
    suap_id = CharField(_('ID do campus no SUAP'), max_length=255, unique=True)
    sigla = CharField(_('sigla do campus'), max_length=255, unique=True)
    descricao = CharField(_('descrição'), max_length=255)
    ambiente = ForeignKey(Ambiente, on_delete=PROTECT)
    active = BooleanField(_('ativo?'))

    class Meta:
        verbose_name = _("campus")
        verbose_name_plural = _("campi")
        ordering = ['sigla']

    def __str__(self):
        return f'{self.descricao} ({self.sigla})'


class Curso(Model):
    suap_id = CharField(_('ID do curso no SUAP'), max_length=255, unique=True)
    codigo = CharField(_('código do curso'), max_length=255, unique=True)
    nome = CharField(_('nome do curso'), max_length=255)
    descricao = CharField(_('descrição'), max_length=255)

    class Meta:
        verbose_name = _("curso")
        verbose_name_plural = _("cursos")
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} ({self.codigo})'


class Turma(Model):
    TURMA_RE = re.compile(r'(\d{5})\.(\d)\.(\d{5})\.(..)')
    suap_id = CharField(_('ID da turma no SUAP'), max_length=255, unique=True)
    campus = ForeignKey(Campus, on_delete=PROTECT, verbose_name=_("campus"))
    codigo = CharField(_('código da turma'), max_length=255, unique=True, 
                       validators=[validators.RegexValidator(TURMA_RE)]
                       )
    ano_mes = SmallIntegerField(verbose_name=_("ano/mês"))
    periodo = SmallIntegerField(_('período'))
    curso = ForeignKey(Curso, on_delete=PROTECT, verbose_name=_('curso'))
    sigla = CharField(_('sigla da turma'), max_length=8)
    turno = CharField(_("turno"), max_length=1, choices=Turno)

    class Meta:
        verbose_name = _("turma")
        verbose_name_plural = _("turmas")
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo}'
    
    def save(self, *args, **kwargs):
        parts = Turma.TURMA_RE.findall(self.codigo)[0]
        self.ano_mes = parts[0]
        self.periodo = parts[1]
        self.curso = Curso.objects.get(codigo=parts[2])
        self.sigla = parts[3]
        self.turno = self.sigla[-1:] if self.sigla[-1:] in Turno else '_'
        super().save(*args, **kwargs)
        

class Componente(Model):
    suap_id = CharField(_('ID do componente no SUAP'), max_length=255, unique=True)
    sigla = CharField(_('sigla do componente'), max_length=255, unique=True)
    descricao = CharField(_('descrição'), max_length=512)
    descricao_historico = CharField(_('descrição no histórico'), max_length=512)
    periodo = IntegerField(_('período'), null=True, blank=True)
    tipo = IntegerField(_('tipo'), null=True, blank=True)
    optativo = BooleanField(_('optativo'), null=True, blank=True)
    qtd_avaliacoes = IntegerField(_('qtd. avalições'), null=True, blank=True)

    class Meta:
        verbose_name = _("componente")
        verbose_name_plural = _("componentes")
        ordering = ['sigla']

    def __str__(self):
        return f'{self.sigla}'
   
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        self.turno = self.sigla[-1:]
        return super().save(force_insert, force_update, using, update_fields)


class Diario(Model):
    DIARIO_RE = re.compile(r'(\d{5}\.\d\.\d{5}\...)\.(.*\..*)')
    suap_id = CharField(_('ID do diário no SUAP'), max_length=255, unique=True)
    codigo = CharField(_('código do diário'), max_length=255, unique=True, 
                       validators=[validators.RegexValidator(DIARIO_RE)]
                       )
    situacao = CharField(_('situação'), max_length=255)
    descricao = CharField(_('descrição'), max_length=255)
    descricao_historico = CharField(_('descrição no histórico'), max_length=255)
    turma = ForeignKey(Turma, on_delete=PROTECT, verbose_name=_('turma'))
    componente = ForeignKey(Componente, on_delete=PROTECT, verbose_name=_('componente'))

    class Meta:
        verbose_name = _("diário")
        verbose_name_plural = _("diários")
        ordering = ['codigo']
        
    def save(self, *args, **kwargs):
        parts = Diario.DIARIO_RE.findall(self.codigo)[0]
        self.turma = Turma.objects.get(codigo=parts[0])
        self.componente = Componente.objects.get(sigla=parts[1])
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.codigo}'


class Polo(Model):
    suap_id = CharField(_('ID do pólo no SUAP'), max_length=255, unique=True)
    nome = CharField(_('nome do pólo'), max_length=255, unique=True)

    class Meta:
        verbose_name = _("pólo")
        verbose_name_plural = _("pólos")
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome}'


class Inscricao(Model):
    diario = ForeignKey(Diario, on_delete=PROTECT)
    usuario = ForeignKey(settings.AUTH_USER_MODEL, on_delete=PROTECT)
    papel = CharField(_('papel'), max_length=1, choices=Papel)
    active = BooleanField(_('ativo?'))
    
    class Meta:
        verbose_name = _("inscrição")
        verbose_name_plural = _("inscrições")
        ordering = ['diario', 'usuario']

    def __str__(self):
        return f'{self.diario} - {self.usuario}'
