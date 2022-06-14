from django.contrib.admin import ModelAdmin, register
from .models import Solicitacao


# @register(Solicitacao)
# class SolicitacaoAdmin(ModelAdmin):
#     list_display = ('timestamp', 'status', 'status_code', 'campus', 'resposta')
#     list_filter = ('status', 'status_code', 'campus')
#     search_fields = ['campus', 'requisicao', 'requisicao_invalida', 'requisicao_header', 'resposta', 'resposta_header', 'resposta_invalida']    
#     autocomplete_fields = ['campus']
#     date_hierarchy = 'timestamp'
#     ordering = ('-timestamp',)
