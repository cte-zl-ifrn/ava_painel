from django.utils.translation import gettext as _
from django.conf import settings
from django.db.models import Model, ForeignKey, CASCADE, TextChoices, BooleanField
from django.db.models import CharField, URLField, ImageField, DateTimeField, TextField
from django.db.models.signals import post_save
from django.dispatch import receiver
import qrcode


class Campus(Model):
    suap_id = CharField('ID no SUAP', max_length=255, unique=True)
    sigla = CharField('Sigla', max_length=255, unique=True)
    token = CharField('Token', max_length=255)
    descricao = CharField('Descrição', max_length=255)
    url = URLField('URL', max_length=255)
    thumbnail = ImageField('Thumbnail', max_length=255)
    active = BooleanField('Ativo?')
    homepage = BooleanField('Listar na página principal?', default=True)

    class Meta:
        verbose_name = "Campus"
        verbose_name_plural = "Campi"
        ordering = ['descricao']

    def __str__(self):
        return f'{self.sigla} - {self.descricao}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = qrcode.make(self.url)
        lsigla = self.sigla.lower()
        img.save(f"{settings.MEDIA_ROOT}/qrcode_{lsigla}.png")



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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_socialauth_suap_user(sender, instance=None, created=False, **kwargs):
    from social_django.models import UserSocialAuth
    UserSocialAuth.objects.update_or_create(user=instance, defaults={'provider': 'suap', 'uid': instance.username})
