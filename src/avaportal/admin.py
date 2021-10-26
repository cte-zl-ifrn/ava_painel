# from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import register, ModelAdmin, TabularInline
from .models import Campus, Solicitacao

@register(Campus)
class CampusAdmin(ModelAdmin):
    list_display = ['sigla', 'descricao', 'active', 'homepage']
    search_fields = ['sigla', 'descricao', 'suap_id', 'url']
    list_filter = ['active', 'homepage']


@register(Solicitacao)
class SolicitacaoAdmin(ModelAdmin):
    list_display = ['timestamp', 'status', 'status_code', 'campus', 'resposta']
    search_fields = ['campus', 'requisicao', 'requisicao_invalida', 'requisicao_header', 'resposta', 'resposta_header', 'resposta_invalida']
    autocomplete_fields = ['campus']
    date_hierarchy = 'timestamp'
    list_filter = ['status', 'status_code', 'campus']

