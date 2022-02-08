from django.utils.translation import gettext as _
from django.utils import timezone
from django.utils.crypto import salted_hmac
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import Group, UserManager, _user_get_permissions, _user_has_module_perms, _user_has_perm
from django.db.models import Model, ForeignKey, CASCADE, ManyToManyField, BooleanField
from django.db.models import CharField, URLField, ImageField, DateTimeField, TextField, IntegerField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_better_choices import Choices
import qrcode


class Turno(Choices):
    NOTURNO = Choices.Value(_("Noturno"), value=1)
    VESPERTINO = Choices.Value(_("Vespertino"), value=2)
    MATUTINO = Choices.Value(_("Matutino"), value=3)
    EAD = Choices.Value(_("EAD"), value=5)
    DIURNO = Choices.Value(_("Diurno"), value=6)
    INTEGRAL = Choices.Value(_("Integral"), value=7)


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
    ano_mes = IntegerField(_('ano.período'), unique=True)

    class Meta:
        verbose_name = _("período")
        verbose_name_plural = _("períodos")
        ordering = ['ano_mes']

    def __str__(self):
        return f'{self.ano_mes}'


class Polo(Model):
    suap_id = CharField(_('ID no SUAP'), max_length=255, unique=True)
    nome = CharField(_('nome do pólo'), max_length=255, unique=True)

    class Meta:
        verbose_name = _("pólo")
        verbose_name_plural = _("pólos")
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome}'


class Componente(Model):
    suap_id = CharField(_('ID no SUAP'), max_length=255, unique=True)
    sigla = CharField(_('sigla do componente'), max_length=255, unique=True)
    token = CharField(_('token'), max_length=255)
    descricao = CharField(_('descrição'), max_length=255)
    descricao_historico = CharField(_('descrição no histórico'), max_length=255)
    periodo = IntegerField(_('período'))
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
    suap_id = CharField(_('ID no SUAP'), max_length=255, unique=True)
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
    suap_id = CharField(_('ID no SUAP'), max_length=255, unique=True)
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
    suap_id = CharField(_('ID no SUAP'), max_length=255, unique=True)
    codigo = CharField(_('código da turma'), max_length=255, unique=True)
    campus = ForeignKey(Campus, on_delete=CASCADE, )
    curso = ForeignKey(Curso, on_delete=CASCADE, )
    periodo_ano = CharField(_('período de oferta (ano)'), max_length=255)
    periodo_mes = CharField(_('período de oferta (mês)'), max_length=255)
    periodo_curso = CharField(_('período do curso'), max_length=255)
    turno = IntegerField(_('turno'), choices=Turno, max_length=255)
    active = BooleanField(_('ativo?'))

    class Meta:
        verbose_name = _("turma")
        verbose_name_plural = _("turmas")
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo}'


class Diario(Model):
    suap_id = CharField(_('ID no SUAP'), max_length=255, unique=True)
    codigo = CharField(_('código do diário'), max_length=255, unique=True)
    situacao = CharField(_('situação'), max_length=255)
    descricao = CharField(_('descrição'), max_length=255)
    descricao_historico = CharField(_('descrição no histórico'), max_length=255)
    sigla = CharField(_('sigla'), max_length=255)
    turma = ForeignKey(Turma, on_delete=CASCADE, )

    class Meta:
        verbose_name = _("diário")
        verbose_name_plural = _("diários")
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo}'


class Solicitacao(Model):
    class Status(Choices):
        SUCESSO = Choices.Value(_("Noturno"),    value='S')
        FALHA   = Choices.Value(_("Vespertino"), value='F')

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


class Usuario(Model):
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
        
    username = CharField(_('username'), max_length=150, unique=True)
    nome = CharField(_('nome do usuário'), max_length=255)
    email = CharField(_('e-Mail principal'), max_length=255)
    email_institucional = CharField(_('e-Mail institucional'), max_length=255)
    email_escolar = CharField(_('e-Mail escolar'), max_length=255)
    email_academico = CharField(_('e-Mail academico'), max_length=255)
    email_pessoal = CharField(_('e-Mail pessoal'), max_length=255)
    tipo = CharField(_('tipo'), max_length=255)
    campus = ForeignKey(Campus, on_delete=CASCADE, verbose_name="Campus", null=True, blank=True)
    polo = ForeignKey(Polo, on_delete=CASCADE, verbose_name="Pólo", null=True, blank=True)

    groups = ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name="user_set", related_query_name="user")
    is_staff = BooleanField(_('equipe'), default=False)
    is_active = BooleanField(_('active'), default=True)
    is_superuser = BooleanField(_('superusuário'), default=False)

    date_joined = DateTimeField(_('date joined'), default=timezone.now)
    last_login = DateTimeField(_('last login'), blank=True, null=True)    

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.nome

    def get_short_name(self):
        return self.nome.split()[0]

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_user_permissions(self, obj=None):
        return _user_get_permissions(self, obj, 'user')

    def get_group_permissions(self, obj=None):
        return _user_get_permissions(self, obj, 'group')

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, 'all')

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True
        return _user_has_module_perms(self, app_label)

    def natural_key(self):
        return (self.username,)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    @classmethod
    def get_email_field_name(cls):
        return 'email'

    @classmethod
    def normalize_username(cls, username):
        return username
