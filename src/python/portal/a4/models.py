from django.utils.translation import gettext as _
from django.db.models import ForeignKey, PROTECT, CharField, DateTimeField, EmailField
from django_better_choices import Choices
from django.http import HttpRequest
from django.contrib.auth.models import AbstractUser, Group


def logged_user(request: HttpRequest):
    username = request.session.get('usuario_personificado', request.user.username)
    user = Usuario.objects.filter(username=username).first()
    if not user.is_authenticated or not user.is_active:
        raise ValidationError('Você não está autenticado ou não está ativo')
    return user


class Grupo(Group):
    pass


class Usuario(AbstractUser):
    username = CharField(_("IFRN-id"), max_length=150, unique=True, 
                         validators=[AbstractUser.username_validator], 
                         error_messages={"unique": _("A user with that IFRN-id already exists."),})
    nome_registro = CharField(_('nome civil'), max_length=255, blank=True)
    nome_social = CharField(_('nome social'), max_length=255, blank=True)
    nome_usual = CharField(_('nome de apresentação'), max_length=255, blank=True)
    nome = CharField(_('nome no SUAP'), max_length=255, blank=True)
    tipo_usuario = CharField(_('tipo'), max_length=255, blank=True)
    foto = CharField(_('URL da foto'), max_length=255, blank=True)
    email = EmailField(_('e-Mail preferêncial'), null=True, blank=False)
    email_secundario = EmailField(_('e-Mail pessoal'), null=True, blank=True)
    email_corporativo = EmailField(_('e-Mail corporativo'), blank=True)
    email_google_classroom = EmailField(_('e-Mail Gogole Classroom'), null=True, blank=True)
    email_academico = EmailField(_('e-Mail academico'), null=True, blank=True)
    campus = ForeignKey('portal.Campus', on_delete=PROTECT, verbose_name=_("campus do aluno"), null=True, blank=True)
    curso = ForeignKey('portal.Curso', on_delete=PROTECT, verbose_name=_("curso do aluno"), null=True, blank=True)
    polo = ForeignKey('portal.Polo', on_delete=PROTECT, verbose_name=_("pólo do aluno"), null=True, blank=True)
    first_login = DateTimeField(_('first login'), blank=True, null=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.nome_usual} ({self.username} - {self.tipo_usuario})"

    @property
    def show_name(self):
        return self.nome_usual if self.nome_usual is not None and self.nome_usual != '' else self.username
