from django.utils.translation import gettext as _
from django.db.models import Model
from django.contrib.admin import register, display, ModelAdmin, StackedInline, TabularInline
from .models import Ambiente, Polo, Componente, Diario, Campus, Curso, Turma, Inscricao


#### 
# Inlines
####

class CampusInline(StackedInline):
    model: Model = Campus
    extra: int = 0


#### 
# Admins
####

@register(Ambiente)
class AmbienteAdmin(ModelAdmin):
    list_display = ['nome', 'sigla', 'url', 'active']
    search_fields = ['nome', 'url']
    list_filter = ['active']
    fieldsets = [
        (_("Nome"), {"fields": ['nome']}),
        (_("Dashboard"), {"fields": [('sigla', 'cor')]}),
        (_("Integração"), {"fields": [('active', 'url', 'token')]})
    ]
    inlines = [CampusInline]


@register(Campus)
class CampusAdmin(ModelAdmin):
    list_display = ['sigla', 'descricao', 'ambiente', 'active']
    list_filter = ['active', 'ambiente']
    search_fields = ['sigla', 'descricao', 'suap_id']


@register(Curso)
class CursoAdmin(ModelAdmin):
    list_display = ['codigo', 'nome']
    search_fields = ['codigo', 'nome', 'suap_id', 'descricao']


@register(Turma)
class TurmaAdmin(ModelAdmin):
    list_display = ['codigo', 'campus', 'ano_mes', 'periodo', 'curso', 'sigla', 'turno']
    list_filter = ['turno', 'ano_mes', 'periodo', 'campus', 'curso']
    readonly_fields = ['ano_mes', 'periodo', 'curso', 'sigla', 'turno']
    search_fields = ['codigo']


@register(Componente)
class ComponenteAdmin(ModelAdmin):
    list_display = ['sigla', 'descricao', 'periodo']
    list_filter = ['optativo', 'qtd_avaliacoes', 'periodo', 'tipo']
    search_fields =  ['sigla', 'suap_id', 'descricao', 'descricao_historico']


@register(Diario)
class DiarioAdmin(ModelAdmin):
    list_display = ['codigo', 'situacao', 'descricao', 'turma', 'componente']
    list_filter = ['situacao']
    search_fields =  ['codigo', 'suap_id', 'descricao', 'descricao_historico', 'sigla']


@register(Polo)
class PoloAdmin(ModelAdmin):
    list_display = ['nome']
    search_fields =  ['nome', 'suap_id']


@register(Inscricao)
class InscricaoAdfmin(ModelAdmin):
    list_display = ['diario', 'usuario', 'papel', 'polo', 'active']
    list_filter = ['active', 'papel', 'polo']
    search_fields =  ['diario__codigo', 'usuario__username']
    
    class Meta:
        verbose_name = _("inscrição")
        verbose_name_plural = _("inscrições")
        ordering = ['diario', 'usuario']

    def __str__(self):
        return f'{self.diario} - {self.usuario}'
