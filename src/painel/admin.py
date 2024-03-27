from django.utils.translation import gettext as _
from django.db.models import Model
from django.contrib.admin import register, display, StackedInline, TabularInline
from django.utils.safestring import mark_safe
from base.admin import BaseModelAdmin
from painel.models import (
    Ambiente,
    Campus,
    Papel,
    Curso,
    Polo,
    CursoPolo,
    VinculoCurso,
    VinculoPolo,
    Popup,
)
from painel.resources import (
    AmbienteResource,
    CampusResource,
    PapelResource,
    CursoResource,
    CursoVinculoResource,
    PoloResource,
    PoloCursoResource,
    PoloVinculoResource,
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
    search_fields = ["nome", "url"]
    list_filter = [
        "active",
    ] + BaseModelAdmin.list_filter
    fieldsets = [
        (_("Identificação"), {"fields": ["nome", "cor_mestra"]}),
        (_("Integração"), {"fields": ["active", "url", "token"]}),
    ]
    inlines = [CampusInline]
    resource_classes = [AmbienteResource]

    @display(description="Cores")
    def cores(self, obj):
        return mark_safe(f"<span style='background: {obj.cor_mestra};'>&nbsp;&nbsp;&nbsp;</span>")


@register(Campus)
class CampusAdmin(BaseModelAdmin):
    list_display = ["sigla", "ambiente", "active"]
    history_list_display = list_display
    field_to_highlight = list_display[0]
    list_filter = ["active", "ambiente"] + BaseModelAdmin.list_filter
    search_fields = ["sigla", "suap_id"]
    resource_classes = [CampusResource]


@register(Curso)
class CursoAdmin(BaseModelAdmin):
    list_display = ["codigo", "nome"]
    history_list_display = list_display
    field_to_highlight = list_display[0]
    search_fields = ["codigo", "nome", "suap_id", "descricao"]
    resource_classes = [CursoResource]
    inlines = [CursoPoloInline, VinculoCursoInline]


@register(Polo)
class PoloAdmin(BaseModelAdmin):
    list_display = ["nome"]
    search_fields = ["nome", "suap_id"]
    resource_classes = [PoloResource]
    inlines = [VinculoPoloInline]


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


@register(VinculoCurso)
class VinculoCursoAdmin(BaseModelAdmin):
    list_display = ["papel", "curso", "colaborador", "active"]
    list_filter = ["active", "papel"] + BaseModelAdmin.list_filter
    search_fields = ["colaborador__nome_social", "colaborador__nome_civil"]
    autocomplete_fields = ["curso", "colaborador"]
    resource_classes = [CursoVinculoResource]


@register(VinculoPolo)
class VinculoPoloAdmin(BaseModelAdmin):
    list_display = ["papel", "polo", "colaborador", "active"]
    list_filter = ["active", "papel", "papel"] + BaseModelAdmin.list_filter
    search_fields = ["colaborador__nome_social", "colaborador__nome_civil"]
    autocomplete_fields = ["polo", "colaborador"]
    resource_classes = [PoloVinculoResource]


@register(CursoPolo)
class CursoPoloResourceAdmin(BaseModelAdmin):
    list_display = ["curso", "polo", "active"]
    list_filter = ["active"] + BaseModelAdmin.list_filter
    autocomplete_fields = ["curso", "polo"]
    resource_classes = [PoloCursoResource]
