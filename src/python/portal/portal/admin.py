from django.utils.translation import gettext as _
from django.contrib.admin import register, display, ModelAdmin
from .models import Ambiente, Periodo, Polo, Componente, Diario, Campus, Curso, Turma


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
