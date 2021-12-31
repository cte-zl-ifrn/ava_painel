from django.db.models.fields import IntegerField
from django.utils.translation import gettext as _
from django.conf import settings
from django.db.models import Model, ForeignKey, CASCADE, TextChoices, BooleanField, IntegerChoices
from django.db.models import CharField, URLField, ImageField, DateTimeField, TextField
from django.db.models.signals import post_save
from django.dispatch import receiver
import qrcode


class Turno(IntegerChoices):
    NOTURNO = 1, _('Noturno')
    VESPERTINO = 2, _('Vespertino')
    MATUTINO = 3, _('Matutino')
    EAD = 5, _('EAD')
    DIURNO = 6, _('Diurno')
    INTEGRAL = 7, _('Integral')


class Ambiente(Model):
    nome = CharField(_('Nome'), max_length=255)
    url = URLField(_('URL'), max_length=255)


class Periodo(Model):
    ano_mes = IntegerField(_('Ano.Período'), unique=True)


class Polo(Model):
    suap_id = CharField(_('ID no SUAP'), max_length=255, unique=True)
    nome = CharField(_('Nome'), max_length=255, unique=True)


class Componente(Model):
    suap_id = CharField(_('ID no SUAP'), max_length=255, unique=True)
    sigla = CharField(_('Sigla'), max_length=255, unique=True)
    token = CharField(_('Token'), max_length=255)
    descricao = CharField(_('Descrição'), max_length=255)
    descricao_historico = CharField(_('Descrição'), max_length=255)
    periodo = IntegerField(_('Perído'))
    tipo = IntegerField(_('Tipo'))
    optativo = BooleanField(_('Optativo'))
    qtd_avaliacoes = BooleanField(_('Qtd. avalições'))


class Diario(Model):
    suap_id = CharField(_('ID no SUAP'), max_length=255, unique=True)
    situacao = CharField(_('Situação'), max_length=255)
    descricao = CharField(_('Descrição'), max_length=255)
    descricao_historico = CharField(_('Descrição'), max_length=255)
    sigla = CharField(_('Sigla'), max_length=255)


class Campus(Model):
    suap_id = CharField(_('ID no SUAP'), max_length=255, unique=True)
    sigla = CharField(_('Sigla'), max_length=255, unique=True)
    token = CharField(_('Token'), max_length=255)
    descricao = CharField(_('Descrição'), max_length=255)
    url = URLField(_('URL'), max_length=255)
    thumbnail = ImageField(_('Thumbnail'), max_length=255)
    active = BooleanField(_('Ativo?'))
    homepage = BooleanField(_('Listar na página principal?'), default=True)

    class Meta:
        verbose_name = _("Campus")
        verbose_name_plural = _("Campi")
        ordering = ['descricao']

    def __str__(self):
        return f'{self.sigla} - {self.descricao}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = qrcode.make(self.url)
        lsigla = self.sigla.lower()
        img.save(f"{settings.MEDIA_ROOT}/qrcode_{lsigla}.png")


class Curso(Model):
    suap_id = CharField(_('ID no SUAP'), max_length=255, unique=True)
    codigo = CharField(_('Código'), max_length=255, unique=True)
    nome = CharField(_('Descrição'), max_length=255)
    descricao = CharField(_('Descrição') max_length=255)
    url_ppc = URLField(_('URL'), max_length=255)
    thumbnail = ImageField(_('Thumbnail'), max_length=255)
    active = BooleanField(_('Ativo?'))
    homepage = BooleanField(_('Listar na página principal?'), default=True)

    class Meta:
        verbose_name = _("Curso")
        verbose_name_plural = _("Cursos")
        ordering = ['nome']

    def __str__(self):
        return f'{self.codigo} - {self.nome}'


class Turma(Model):
    suap_id = CharField(_('ID no SUAP'), max_length=255, unique=True)
    codigo = CharField(_('Código'), max_length=255, unique=True)
    campus = ForeignKey(Campus)
    curso = ForeignKey(Curso)
    período_ano = CharField(_('Período de oferta (ano)'), max_length=255, unique=True)
    período_mes = CharField(_('Período de oferta (mês)'), max_length=255, unique=True)
    período_curso = CharField(_('Período do curso'), max_length=255, unique=True)
    turno = CharField(_('Turno'), max_length=255, unique=True)
    active = BooleanField(_('Ativo?'))

    class Meta:
        verbose_name = _("Turma")
        verbose_name_plural = _("Turmas")
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo}'


class Solicitacao(Model):
    class Status(TextChoices):
        SUCESSO = 'Sucesso', _('Sucesso')
        FALHA = 'Falha', _('Falha')
    timestamp = DateTimeField('Quando ocorreu', auto_now_add=True)
    requisicao = TextField('Requisição', null=True, blank=True)
    requisicao_header = TextField('Cabeçalho da requisição', null=True, blank=True)
    requisicao_invalida = TextField('Requisição inválida', null=True, blank=True)
    resposta = TextField('Resposta', null=True, blank=True)
    resposta_header = TextField('Cabeçalho da resposta', null=True, blank=True)
    resposta_invalida = TextField('Resposta inválida', null=True, blank=True)
    campus = ForeignKey(Campus, on_delete=CASCADE, verbose_name="Campus", null=True, blank=True)
    status = CharField(_("Status"), max_length=255, choices=Status.choices, null=True, blank=True)
    status_code = CharField(_("Status code"), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Solicitação"
        verbose_name_plural = "Solicitações"
        ordering = ['id']


class Usuario(Model):
    suap_id = IntegerField(_('ID no SUAP'), unique=True)
    nome = CharField(_('Nome'), max_length=255)
    login = CharField(_('Login'), max_length=255)
    email = CharField(_('E-Mail principal'), max_length=255)
    email_institucional = CharField(_('E-Mail institucional'), max_length=255)
    email_escolar = CharField(_('E-Mail escolar'), max_length=255)
    email_academico = CharField(_('E-Mail academico'), max_length=255)
    email_pessoal = CharField(_('E-Mail pessoal'), max_length=255)
    tipo = CharField(_('Tipo'), max_length=255)
    status = CharField(_('status'), max_length=255)
    polo = ForeignKey(Polo, on_delete=CASCADE, verbose_name="Pólo", null=True, blank=True)
    campus = ForeignKey(Campus, on_delete=CASCADE, verbose_name="Campus", null=True, blank=True)


class Inscricao(Model):
    suap_id = IntegerField(_('ID no SUAP'), unique=True)
    nome = CharField(_('Nome'), max_length=255)
    login = CharField(_('Login'), max_length=255)
    email = CharField(_('E-Mail principal'), max_length=255)
    email_institucional = CharField(_('E-Mail institucional'), max_length=255)
    email_escolar = CharField(_('E-Mail escolar'), max_length=255)
    email_academico = CharField(_('E-Mail academico'), max_length=255)
    email_pessoal = CharField(_('E-Mail pessoal'), max_length=255)
    tipo = CharField(_('Tipo'), max_length=255)
    status = CharField(_('status'), max_length=255)
    polo = ForeignKey(Polo, on_delete=CASCADE, verbose_name="Pólo", null=True, blank=True)
    campus = ForeignKey(Campus, on_delete=CASCADE, verbose_name="Campus", null=True, blank=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_socialauth_suap_user(sender, instance=None, created=False, **kwargs):
    from social_django.models import UserSocialAuth
    UserSocialAuth.objects.update_or_create(user=instance, defaults={'provider': 'suap', 'uid': instance.username})
