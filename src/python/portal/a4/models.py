from django.utils.translation import gettext as _
from django.db.models import ForeignKey, PROTECT, CharField, DateTimeField
from django_better_choices import Choices
from django.contrib.auth.models import AbstractUser, Group


class Grupo(Group):
    pass


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
    email_escolar = CharField(_('e-Mail escolar'), max_length=255, null=True, blank=True)
    email_academico = CharField(_('e-Mail academico'), max_length=255, null=True, blank=True)
    email_secundario = CharField(_('e-Mail pessoal'), max_length=255, null=True, blank=True)
    tipo = CharField(_('tipo'), max_length=255, choices=Tipo)
    campus = ForeignKey('portal.Campus', on_delete=PROTECT, verbose_name=_("campus do aluno"), null=True, blank=True)
    polo = ForeignKey('portal.Polo', on_delete=PROTECT, verbose_name=_("pólo"), null=True, blank=True)
    first_login = DateTimeField(_('first login'), blank=True, null=True)    

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        tipo = Usuario.Tipo.get_key(self.tipo)
        return f"{self.nome} ({self.username} - {tipo})"

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
