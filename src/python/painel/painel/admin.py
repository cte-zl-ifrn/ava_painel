from django.utils.translation import gettext as _
from functools import update_wrapper
from django.urls import path, reverse
from django.db.models import Model
from django.contrib.admin import register, display, StackedInline, TabularInline
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.utils import quote, unquote
from django.contrib.admin.options import IS_POPUP_VAR, TO_FIELD_VAR, flatten_fieldsets
from django.contrib.admin.helpers import AdminErrorList, AdminForm, InlineAdminFormSet
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.core.exceptions import PermissionDenied
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportMixin, ExportActionMixin
from simple_history.admin import SimpleHistoryAdmin
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter
from base.admin import BaseModelAdmin
from .models import (
    Ambiente,
    Polo,
    Componente,
    Diario,
    Campus,
    Curso,
    Turma,
    Inscricao,
    Popup,
    Papel,
    VinculoPolo,
    VinculoCurso,
    CursoPolo,
)
from .resources import (
    AmbienteResource,
    CampusResource,
    CursoResource,
    PapelResource,
    VinculoPoloResource,
    VinculoCursoResource,
    CursoPoloResource,
)


####
# Inlines
####


class CampusInline(StackedInline):
    model: Model = Campus
    extra: int = 0


class VinculoCursoInline(TabularInline):
    model: Model = VinculoCurso
    extra: int = 0


class VinculoPoloInline(TabularInline):
    model: Model = VinculoPolo
    extra: int = 0


class CursoPoloInline(TabularInline):
    model: Model = CursoPolo
    extra: int = 0


####
# Admins
####


@register(Ambiente)
class AmbienteAdmin(BaseModelAdmin):
    list_display = ["nome", "cores", "url", "active"]
    history_list_display = list_display
    field_to_highlight = list_display[0]
    search_fields = ["nome", "sigla", "url"]
    list_filter = [
        "active",
    ] + BaseModelAdmin.list_filter
    fieldsets = [
        (_("Identificação"), {"fields": ["nome", "sigla"]}),
        (
            _("Cores do ambiente"),
            {"fields": ["cor_mestra", "cor_degrade", "cor_progresso"]},
        ),
        (_("Integração"), {"fields": ["active", "url", "token"]}),
    ]
    inlines = [CampusInline]
    resource_classes = [AmbienteResource]

    @display(description="Cores")
    def cores(self, obj):
        return mark_safe(
            f"<span style='background: {obj.cor_mestra};'>&nbsp;&nbsp;&nbsp;</span>"
            + f"<span style='background: {obj.cor_degrade};'>&nbsp;&nbsp;&nbsp;</span>"
            + f"<span style='background: {obj.cor_progresso};'>&nbsp;&nbsp;&nbsp;</span>"
        )


@register(Campus)
class CampusAdmin(BaseModelAdmin):
    list_display = ["sigla", "descricao", "ambiente", "active"]
    history_list_display = list_display
    field_to_highlight = list_display[0]
    list_filter = ["active", "ambiente"] + BaseModelAdmin.list_filter
    search_fields = ["sigla", "descricao", "suap_id"]
    resource_classes = [CampusResource]


@register(Curso)
class CursoAdmin(BaseModelAdmin):
    list_display = ["codigo", "nome"]
    history_list_display = list_display
    field_to_highlight = list_display[0]
    search_fields = ["codigo", "nome", "suap_id", "descricao"]
    resource_classes = [CursoResource]
    inlines = [CursoPoloInline, VinculoCursoInline]


@register(Turma)
class TurmaAdmin(BaseModelAdmin):
    list_display = ["codigo", "campus", "ano_mes", "periodo", "curso", "sigla", "turno"]
    list_filter = [
        "turno",
        "ano_mes",
        "periodo",
        "campus",
        "curso",
    ] + BaseModelAdmin.list_filter
    readonly_fields = ["ano_mes", "periodo", "curso", "sigla", "turno"]
    search_fields = ["codigo"]


@register(Componente)
class ComponenteAdmin(BaseModelAdmin):
    list_display = ["sigla", "descricao", "periodo"]
    list_filter = [
        "optativo",
        "qtd_avaliacoes",
        "periodo",
        "tipo",
    ] + BaseModelAdmin.list_filter
    search_fields = ["sigla", "suap_id", "descricao", "descricao_historico"]


@register(Diario)
class DiarioAdmin(BaseModelAdmin):
    list_display = ["codigo", "situacao", "descricao", "turma", "componente"]
    list_filter = ["situacao"] + BaseModelAdmin.list_filter
    search_fields = ["codigo", "suap_id", "descricao", "descricao_historico", "sigla"]


@register(Polo)
class PoloAdmin(BaseModelAdmin):
    list_display = ["nome"]
    search_fields = ["nome", "suap_id"]
    inlines = [VinculoPoloInline]


@register(Inscricao)
class InscricaoAdmin(BaseModelAdmin):
    list_display = ["diario", "usuario", "papel", "polo", "active"]
    list_filter = ["active", "papel", "polo"] + BaseModelAdmin.list_filter
    search_fields = ["diario__codigo", "usuario__username"]


@register(Popup)
class PopupAdmin(BaseModelAdmin):
    list_display = ["titulo", "start_at", "end_at", "active", "mostrando"]
    list_filter = [
        "active",
        "start_at",
        "end_at",
        "url",
        "mensagem",
    ] + BaseModelAdmin.list_filter
    search_fields = ["titulo", "mensagem", "url"]


@register(Papel)
class PapelAdmin(BaseModelAdmin):
    list_display = ["nome", "sigla", "contexto", "active"]
    list_filter = ["active", "contexto"] + BaseModelAdmin.list_filter
    search_fields = ["nome", "sigla", "contexto"]
    resource_classes = [PapelResource]


@register(VinculoPolo)
class VinculoPoloAdmin(BaseModelAdmin):
    list_display = ["papel", "polo", "colaborador", "active"]
    list_filter = ["active", "papel", "papel"] + BaseModelAdmin.list_filter
    search_fields = ["colaborador__nome_social", "colaborador__nome_civil"]
    autocomplete_fields = ["polo", "colaborador"]
    resource_classes = [VinculoPoloResource]


@register(VinculoCurso)
class VinculoCursoAdmin(BaseModelAdmin):
    list_display = ["papel", "curso", "colaborador", "active"]
    list_filter = ["active", "papel"] + BaseModelAdmin.list_filter
    search_fields = ["colaborador__nome_social", "colaborador__nome_civil"]
    autocomplete_fields = ["curso", "colaborador"]
    resource_classes = [VinculoCursoResource]


@register(CursoPolo)
class CursoPoloResourceAdmin(BaseModelAdmin):
    list_display = ["curso", "polo", "active"]
    list_filter = ["active"] + BaseModelAdmin.list_filter
    autocomplete_fields = ["curso", "polo"]
    resource_classes = [CursoPoloResource]
