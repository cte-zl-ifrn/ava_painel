from dataclasses import field
from encodings import search_function
from tabnanny import verbose
from django.utils.translation import gettext as _
from django.contrib.admin import register, display, ModelAdmin, TabularInline
# from import_export.admin import ImportExportModelAdmin
from .models import Ambiente, Periodo, Polo, Componente, Diario, Campus, Curso, Turma, Solicitacao, Usuario


#### 
# Inlines
####

class SolicitacaoInline(TabularInline):
    model = Solicitacao
    extra = 0


#### 
# Admins
####

@register(Ambiente)
class AmbienteAdmin(ModelAdmin):
    list_display = ('nome', 'url')
    search_fields = ('nome', 'url')


@register(Periodo)
class PeriodoAdmin(ModelAdmin):
    list_display = ('ano_mes',)
    search_fields =  ('ano_mes',)


@register(Polo)
class PoloAdmin(ModelAdmin):
    list_display = ('nome', 'suap_id')
    search_fields =  ('suap_id', 'nome')


@register(Componente)
class ComponenteAdmin(ModelAdmin):
    list_display = ('suap_id', 'sigla', 'descricao', 'periodo', 'tipo', 'optativo', 'qtd_avaliacoes',)
    list_filter = ('optativo', 'qtd_avaliacoes', 'periodo', 'tipo')
    search_fields =  ('sigla', 'suap_id', 'descricao', 'descricao_historico', 'descricao_historico', )


@register(Campus)
class CampusAdmin(ModelAdmin):
    list_display = ('sigla','descricao','active','homepage',)
    list_filter = ('active', 'homepage')
    search_fields = ('sigla', 'descricao', 'suap_id', 'url',)
    inlines = [SolicitacaoInline]


@register(Curso)
class CursoAdmin(ModelAdmin):
    list_display = ('codigo', 'nome', 'suap_id', 'active', 'homepage')
    list_filter = ('active', 'homepage')
    search_fields = ('codigo', 'nome', 'suap_id', 'descricao',)


@register(Turma)
class TurmaAdmin(ModelAdmin):
    list_display = ('codigo', 'campus', 'periodo', 'semestre', 'curso', 'sigla')
    list_filter = ('turno', 'periodo', 'campus', 'semestre', 'curso')
    search_fields = ('codigo', 'sigla')


@register(Diario)
class DiarioAdmin(ModelAdmin):
    list_display = ('codigo', 'situacao', 'descricao', 'turma', 'componente')
    list_filter = ('situacao',)
    search_fields =  ('codigo', 'suap_id', 'descricao', 'descricao_historico', 'sigla')


@register(Solicitacao)
class SolicitacaoAdmin(ModelAdmin):
    list_display = ('timestamp', 'status', 'status_code', 'campus', 'resposta')
    list_filter = ('status', 'status_code', 'campus')
    search_fields = ['campus', 'requisicao', 'requisicao_invalida', 'requisicao_header', 'resposta', 'resposta_header', 'resposta_invalida']    
    autocomplete_fields = ['campus']
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)


@register(Usuario)
class UsuarioAdmin(ModelAdmin):
    list_display = ('username', 'nome', 'email', 'email_secundario', 'tipo', 'auth')
    list_filter = ('tipo', 'polo__nome', 'campus__sigla')
    fieldsets = [
        (None, {"fields": ['username', 'tipo'],}),
        (_('Aluno'), {"fields": ['campus', 'polo'],}),
        (_('Emails'), {"fields": ['email', 'email_escolar', 'email_academico', 'email_secundario'],}),
        (_('Auth'), {"fields": ['is_active', 'is_superuser', 'groups'],}),
        (_('Dates'), {"fields": ['date_joined', 'first_login', 'last_login'],}),
    ]

    @display
    def auth(self, obj):        
        result = ""
        if obj.is_staff:
            result += 'Colaborador superusuário ' if obj.is_superuser else 'Colaborador '
        else:
            result += 'Usuário '
        result += '(Ativo)' if obj.is_active else '(Inativo)'
        return result
