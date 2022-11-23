from django.utils.translation import gettext as _
from django.db.models import ForeignKey, PROTECT, CharField, DateTimeField, EmailField
from django_better_choices import Choices
from django.contrib.auth.models import AbstractUser, Group


class Grupo(Group):
    pass


class Usuario(AbstractUser):
    class Tipo(Choices):
        INCERTO    = Choices.Value(_("Incerto"),    value='I', is_servidor=False, is_colaborador=False, username_length=0)
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
    username = CharField(_("IFRN-id"), max_length=150, unique=True, 
                         validators=[AbstractUser.username_validator], 
                         error_messages={"unique": _("A user with that IFRN-id already exists."),})
    nome_civil = CharField(_('nome civil'), max_length=255)
    nome_social = CharField(_('nome social'), max_length=255)
    nome_apresentacao = CharField(_('nome de apresentação'), max_length=255)
    tipo = CharField(_('tipo'), max_length=255, choices=Tipo)
    email = EmailField(_('e-Mail preferêncial'), null=True, blank=False)
    email_secundario = EmailField(_('e-Mail pessoal'), null=True, blank=True)
    email_corporativo = EmailField(_('e-Mail corporativo'), blank=True)
    email_escolar = EmailField(_('e-Mail escolar'), null=True, blank=True)
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
        tipo = Usuario.Tipo.get_key(self.tipo)
        return f"{self.nome_apresentacao} ({self.username} - {tipo})"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # names = self.nome_civil.split(" ")
        # self.first_name = " ".join(names[:-1])
        # self.last_name = "".join(names[-1:])
        # self.nome_apresentacao = self.nome_social if self.nome_social else self.nome_civil
        self.tipo = Usuario.Tipo.get_by_length(len(self.username))
        super().save(force_insert, force_update, using, update_fields)
