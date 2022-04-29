from django.utils.translation import gettext as _
from django.utils import timezone
from django.utils.crypto import salted_hmac
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Model, ForeignKey, CASCADE, PROTECT, ManyToManyField, BooleanField
from django.db.models import CharField, URLField, ImageField, DateTimeField, TextField, IntegerField, SmallIntegerField
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser, Group, UserManager, _user_get_permissions, _user_has_module_perms, _user_has_perm
from django.dispatch import receiver
from django_better_choices import Choices
from pyparsing import Char
import qrcode


class Turno(Choices):
    NOTURNO = Choices.Value(_("Noturno"), value='N')
    VESPERTINO = Choices.Value(_("Vespertino"), value='V')
    MATUTINO = Choices.Value(_("Matutino"), value='M')
    EAD = Choices.Value(_("EAD"), value='E')
    DIURNO = Choices.Value(_("Diurno"), value='D')
    INTEGRAL = Choices.Value(_("Integral"), value='I')
    DESCONHECIDO = Choices.Value(_("Desconhecido"), value='_')


class Ambiente(Model):
    nome = CharField(_('nome do ambiente'), max_length=255)
    url = URLField(_('URL'), max_length=255)

    class Meta:
        verbose_name = _("ambiente")
        verbose_name_plural = _("ambientes")
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome}'


class Periodo(Model):
    ano_mes = IntegerField(_('período'), primary_key=True)

    class Meta:
        verbose_name = _("período")
        verbose_name_plural = _("períodos")
        ordering = ['ano_mes']

    def __str__(self):
        return f'{self.ano_mes}'


class Polo(Model):
    suap_id = CharField(_('ID do pólo no SUAP'), max_length=255, unique=True)
    nome = CharField(_('nome do pólo'), max_length=255, unique=True)

    class Meta:
        verbose_name = _("pólo")
        verbose_name_plural = _("pólos")
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome}'


class Componente(Model):
    suap_id = CharField(_('ID do componente no SUAP'), max_length=255, unique=True)
    sigla = CharField(_('sigla do componente'), max_length=255, unique=True)
    # token = CharField(_('token'), max_length=255)
    descricao = CharField(_('descrição'), max_length=512)
    descricao_historico = CharField(_('descrição no histórico'), max_length=512)
    periodo = IntegerField(_('período'), null=True, blank=True)
    tipo = IntegerField(_('tipo'))
    optativo = BooleanField(_('optativo'))
    qtd_avaliacoes = IntegerField(_('qtd. avalições'))

    class Meta:
        verbose_name = _("componente")
        verbose_name_plural = _("componentes")
        ordering = ['sigla']

    def __str__(self):
        return f'{self.sigla}'


class Campus(Model):
    suap_id = CharField(_('ID do campus no SUAP'), max_length=255, unique=True)
    sigla = CharField(_('sigla do campus'), max_length=255, unique=True)
    token = CharField(_('token'), max_length=255)
    descricao = CharField(_('descrição'), max_length=255)
    url = URLField(_('URL'), max_length=255)
    thumbnail = ImageField(_('thumbnail'), max_length=255)
    active = BooleanField(_('ativo?'))
    homepage = BooleanField(_('listar na página principal?'), default=True)

    class Meta:
        verbose_name = _("campus")
        verbose_name_plural = _("campi")
        ordering = ['sigla']

    def __str__(self):
        return f'{self.sigla} - {self.descricao}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = qrcode.make(self.url)
        lsigla = self.sigla.lower()
        img.save(f"{settings.MEDIA_ROOT}/qrcode_{lsigla}.png")


class Curso(Model):
    suap_id = CharField(_('ID do curso no SUAP'), max_length=255, unique=True)
    codigo = CharField(_('código do curso'), max_length=255, unique=True)
    nome = CharField(_('nome do curso'), max_length=255)
    descricao = CharField(_('descrição'), max_length=255)
    url_ppc = URLField(_('URL'), max_length=255)
    thumbnail = ImageField(_('thumbnail'), max_length=255)
    active = BooleanField(_('ativo?'))
    homepage = BooleanField(_('listar na página principal?'), default=True)

    class Meta:
        verbose_name = _("curso")
        verbose_name_plural = _("cursos")
        ordering = ['nome']

    def __str__(self):
        return f'{self.codigo} - {self.nome}'


class Turma(Model):
    codigo = CharField(_('código da turma'), max_length=255, unique=True)
    suap_id = CharField(_('ID da turma no SUAP'), max_length=255, unique=True)
    campus = ForeignKey(Campus, on_delete=PROTECT, verbose_name=_("campus"))
    periodo = ForeignKey(Periodo, on_delete=PROTECT, verbose_name=_("periodo"))
    semestre = SmallIntegerField(_('semestre'))
    curso = ForeignKey(Curso, on_delete=PROTECT, verbose_name=_('curso'))
    sigla = CharField(_('sigla da turma'), max_length=8)
    turno = CharField(_("turno"), max_length=1, choices=Turno)

    class Meta:
        verbose_name = _("turma")
        verbose_name_plural = _("turmas")
        ordering = ['codigo']

    def __str__(self):
        return self.codigo
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        self.turno = self.sigla[-1:]
        return super().save(force_insert, force_update, using, update_fields)


class Diario(Model):
    suap_id = CharField(_('ID do diário no SUAP'), max_length=255, unique=True)
    codigo = CharField(_('código do diário'), max_length=255, unique=True)
    situacao = CharField(_('situação'), max_length=255)
    descricao = CharField(_('descrição'), max_length=255)
    descricao_historico = CharField(_('descrição no histórico'), max_length=255)
    turma = ForeignKey(Turma, on_delete=PROTECT, verbose_name=_('turma'))
    componente = ForeignKey(Componente, on_delete=PROTECT, verbose_name=_('componente'))

    class Meta:
        verbose_name = _("diário")
        verbose_name_plural = _("diários")
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo}'


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
    campus = ForeignKey(Campus, on_delete=CASCADE, null=True, blank=True)
    status = CharField(_("status"), max_length=255, choices=Status, null=True, blank=True)
    status_code = CharField(_("status code"), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _("Solicitação")
        verbose_name_plural = _("Solicitações")
        ordering = ['id']

    def __str__(self):
        return f'{self.id}'


class Usuario(AbstractUser):
    class Tipo(Choices):
        INCERTO    = Choices.Value(_("Incerto"),    value='I', is_servidor=True,  is_colaborador=True,  username_length=0)
        SERVIDOR   = Choices.Value(_("Servidor"),   value='S', is_servidor=True,  is_colaborador=True,  username_length=7)
        TECNICO    = Choices.Value(_("Técnico"),    value='T', is_servidor=True,  is_colaborador=True,  username_length=7)
        DOCENTE    = Choices.Value(_("Docente"),    value='D', is_servidor=True,  is_colaborador=True,  username_length=7)
        ESTAGIARIO = Choices.Value(_("Estagiário"), value='E', is_servidor=True,  is_colaborador=True,  username_length=7)
        PRESTADOR  = Choices.Value(_("Prestador"),  value='P', is_servidor=False, is_colaborador=True,  username_length=11)
        ALUNO      = Choices.Value(_("Aluno"),      value='A', is_servidor=False, is_colaborador=False, username_length=15)

        @classmethod
        def get_by_length(cls, username_length):
            for key, tipo in Usuario.Tipo.items():
                if username_length == tipo.username_length:
                    return tipo
            return Usuario.Tipo.INCERTO

    nome = CharField(_('nome do usuário'), max_length=255)
    # email = CharField(_('e-Mail'), max_length=255, null=True, blank=True)
    email_escolar = CharField(_('e-Mail escolar'), max_length=255, null=True, blank=True)
    email_academico = CharField(_('e-Mail academico'), max_length=255, null=True, blank=True)
    email_secundario = CharField(_('e-Mail pessoal'), max_length=255, null=True, blank=True)
    tipo = CharField(_('tipo'), max_length=255, choices=Tipo)
    campus = ForeignKey(Campus, on_delete=PROTECT, verbose_name=_("campus do aluno"), null=True, blank=True)
    polo = ForeignKey(Polo, on_delete=PROTECT, verbose_name=_("pólo"), null=True, blank=True)
    first_login = DateTimeField(_('first login'), blank=True, null=True)    

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.nome} ({self.username} - {self.tipo})"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        names = self.nome.split(" ")
        self.first_name = " ".join(names[:-1])
        self.last_name = "".join(names[-1:])
        if len(self.username) == 11:
            self.tipo = Usuario.Tipo.PRESTADOR
        elif len(self.username) < 11:
            self.tipo = Usuario.Tipo.SERVIDOR
        else:
            self.tipo = Usuario.Tipo.ALUNO
        super().save(force_insert, force_update, using, update_fields)
