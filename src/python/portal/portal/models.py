from django.utils.translation import gettext as _
import re
import json
import requests
from django.conf import settings
from django.core import validators
from django.forms import ValidationError
from django.db.models import Model, ForeignKey, PROTECT, BooleanField
from django.db.models import CharField, URLField, ImageField, DateTimeField, IntegerField, SmallIntegerField
from django_better_choices import Choices
from a4.models import Usuario
from middleware.models import Solicitacao


def h2d(r):
    {k:v for k,v in r.headers.items()}


class SyncError(Exception):
    def __init__(self, message, code, campus=None, retorno=None, params=None):
        super().__init__(message, code, params)
        self.message = message
        self.code = code
        self.campus = campus
        self.retorno = retorno


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
                       validators=[validators.RegexValidator(TURMA_RE)])

    curso = ForeignKey(Curso, on_delete=PROTECT, verbose_name=_('curso'))
    ano_mes = SmallIntegerField(verbose_name=_("ano/mês"))
    periodo = SmallIntegerField(_('período'))
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

    @classmethod
    def sync(cls, message_string, headers):
        def _validate_campus():
            try:
                pkg = json.loads(message_string)
                filter = {"suap_id": pkg["campus"]["id"], "sigla": pkg["campus"]["sigla"]}
            except:
                raise SyncError(f"O JSON está inválido.", 406)
            
            campus = Campus.objects.filter(**filter).first()
            if campus is None:
                raise SyncError(f"Não existe um campus com o id '{filter['suap_id']}' e a sigla '{filter['sigla']}'.", 404)

            if not campus.active:
                raise SyncError(f"O campus '{filter['sigla']}' existe, mas está inativo.", 412, campus)
            
            if not campus.ambiente.active:
                raise SyncError(f"O campus '{filter['sigla']}' existe e está ativo, mas o ambiente {campus.ambiente.sigla} está inativo.", 417, campus)
            return campus, pkg
        
        campus, pkg = _validate_campus()
        try:
            retorno = requests.post(
                f"{campus.ambiente.url}/auth/suap/sync_up.php", 
                data={"jsonstring": message_string},
                headers={"Authentication": f"Token {campus.ambiente.token}"}
            )
        except Exception as e:
            
            raise SyncError(f"Erro na integração. O Moodle disse: {e}", 513, campus)
        
        
        retorno_json = None
        if retorno.status_code != 200:
            try:
                retorno_json = json.loads(retorno.text)
            except:
                retorno_json = {}
            raise SyncError(f"Erro na integração. Contacte um administrador. Erro: {retorno_json}", retorno.status_code, campus, retorno)
        
        try:
            retorno_json = json.loads(retorno.text)
        except:
            raise SyncError(f"Erro na integração. Contacte um desenvolvedor.", retorno.status_code, campus, retorno)
        
        Solicitacao.objects.create(
            requisicao=message_string,
            requisicao_header=headers,
            
            resposta=retorno_json,
            resposta_header=h2d(retorno),
            
            status=Solicitacao.Status.SUCESSO,
            status_code=retorno.status_code,
            
            campus=campus
        )
        
        try:
            Diario.make(pkg)
        except Exception as e:
            raise SyncError(f"Erro na integração. Contacte um administrador.", 512, campus, retorno)
        
        return retorno_json
    
    @classmethod
    def make(cls, d):
        def get_polo_id(person):
            if 'polo' in person and person['polo']:
                return person['polo']['id']
            else:
                return None
                        
        campus = Campus.objects.get(suap_id=d['campus']['id'])
        curso, created = Curso.objects.update_or_create(
            codigo=d['curso']['codigo'],
            defaults={
                'suap_id': d['curso']['id'],
                'nome': d['curso']['nome'],
                'descricao': d['curso']['descricao'],
            }
        )
        turma, created = Turma.objects.update_or_create(
            codigo=d['turma']['codigo'],
            defaults={
                'suap_id': d['turma']['id'],
                'campus': campus,
            }
        )
        componente, created = Componente.objects.update_or_create(
            sigla=d['componente']['sigla'],
            defaults={
                'suap_id': d['componente']['id'],
                'descricao': d['componente']['descricao'],
                'descricao_historico': d['componente']['descricao_historico'],
                'periodo': d['componente']['periodo'],
                'tipo': d['componente']['tipo'],
                'optativo': d['componente']['optativo'],
                'qtd_avaliacoes': d['componente']['qtd_avaliacoes'],
            }
        )
        diario, created = Diario.objects.update_or_create(
            codigo=turma.codigo + '.' + d['diario']['sigla'],
            defaults={
                'suap_id': d['diario']['id'],
                'situacao': d['diario']['situacao'],
                'descricao': d['diario']['descricao'],
                'descricao_historico': d['diario']['descricao_historico'],
                'turma': turma,
                'componente': componente,
            }
        )
        
        pessoas = d['professores'] + d['alunos']
        polos = {}
        for p in pessoas:
            if get_polo_id(p) and get_polo_id(p) not in polos:
                polo, created = Polo.objects.update_or_create(
                    suap_id=p['polo']['id'],
                    defaults={'nome': p['polo']['nome']}
                )
                polos[p['polo']['id']] = polo

        for p in pessoas:

            if 'matricula' in p.keys():
                papel = Papel.ALUNO
            else:
                papel = Papel.PROFESSOR if p['tipo'] == 'Principal' else Papel.TUTOR
                
            is_active = 'ativo' == p.get('situacao', p.get('status', '')).lower()
            username = p.get('login', p.get('matricula', None))
            polo = polos.get(get_polo_id(p))
            usuario, created = Usuario.objects.update_or_create(
                username=username,
                defaults={
                    'nome': p['nome'],
                    'email': p['email'],
                    # 'email_escolar': pessoa['email_escolar'],
                    # 'email_academico': pessoa['email_academico'],
                    # 'email_secundario': pessoa['email_secundario'],
                    'is_active': is_active,
                    'tipo': Usuario.Tipo.get_by_length(len(username)),
                    # 'campus': campus if papel == Papel.ALUNO else None,
                    'polo': polo,
                    'curso': curso if papel == Papel.ALUNO else None,
                }
            )
            inscricao, created = Inscricao.objects.update_or_create(
                diario=diario,
                usuario=usuario,
                defaults={
                    'polo': polo,
                    'papel': papel,
                    'active': is_active,
                }
            )
            if created:
                inscricao.notify()
        return diario
    
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
    polo = ForeignKey(Polo, on_delete=PROTECT, null=True, blank=True)
    papel = CharField(_('papel'), max_length=1, choices=Papel)
    active = BooleanField(_('ativo?'))
    
    class Meta:
        verbose_name = _("inscrição")
        verbose_name_plural = _("inscrições")
        ordering = ['diario', 'usuario']

    def __str__(self):
        return f'{self.diario} - {self.usuario}'
    
    def notify(self):
        pass
