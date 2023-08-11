from import_export.resources import ModelResource
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, DateTimeWidget
from .models import (
    Ambiente,
    Campus,
    Curso,
    Papel,
    Polo,
    Usuario,
    VinculoPolo,
    VinculoCurso,
    CursoPolo,
)


DEFAULT_DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
DEFAULT_DATETIME_FORMAT_WIDGET = DateTimeWidget(format=DEFAULT_DATETIME_FORMAT)


class AmbienteResource(ModelResource):
    class Meta:
        model = Ambiente
        export_order = (
            "nome",
            "url",
            "token",
            "cor_mestra",
            "cor_degrade",
            "cor_progresso",
            "active",
        )
        import_id_fields = ("nome",)
        fields = export_order
        skip_unchanged = True


class CampusResource(ModelResource):
    ambiente = Field(
        attribute="ambiente",
        column_name="nome_ambiente",
        widget=ForeignKeyWidget(Ambiente, field="nome"),
    )

    class Meta:
        model = Campus
        export_order = ("sigla", "descricao", "ambiente", "suap_id", "active")
        import_id_fields = ("sigla",)
        fields = export_order
        skip_unchanged = True


class CursoResource(ModelResource):
    class Meta:
        model = Curso
        export_order = ("codigo", "nome", "descricao", "suap_id")
        import_id_fields = ("codigo",)
        fields = export_order
        skip_unchanged = True


class PapelResource(ModelResource):
    class Meta:
        model = Papel
        export_order = ["sigla", "nome", "contexto", "active"]
        import_id_fields = ("sigla",)
        fields = export_order
        skip_unchanged = True


class VinculoPoloResource(ModelResource):
    papel = Field(
        attribute="papel",
        column_name="papel",
        widget=ForeignKeyWidget(Papel, field="nome"),
    )

    polo = Field(
        attribute="polo",
        column_name="polo",
        widget=ForeignKeyWidget(Polo, field="nome"),
    )

    colaborador = Field(
        attribute="colaborador",
        column_name="colaborador",
        widget=ForeignKeyWidget(Usuario, field="username"),
    )

    class Meta:
        model = VinculoPolo
        export_order = ["papel", "polo", "colaborador", "active"]
        import_id_fields = (
            "papel",
            "polo",
            "colaborador",
        )
        fields = export_order
        skip_unchanged = True


class VinculoCursoResource(ModelResource):
    papel = Field(
        attribute="papel",
        column_name="papel",
        widget=ForeignKeyWidget(Papel, field="sigla"),
    )

    curso = Field(
        attribute="curso",
        column_name="curso",
        widget=ForeignKeyWidget(Curso, field="codigo"),
    )

    colaborador = Field(
        attribute="colaborador",
        column_name="colaborador",
        widget=ForeignKeyWidget(Usuario, field="username"),
    )

    class Meta:
        model = VinculoCurso
        export_order = ["papel", "curso", "colaborador", "active"]
        import_id_fields = (
            "papel",
            "curso",
            "colaborador",
        )
        fields = export_order
        skip_unchanged = True


class CursoPoloResource(ModelResource):
    curso = Field(
        attribute="curso",
        column_name="curso",
        widget=ForeignKeyWidget(Curso, field="codigo"),
    )

    polo = Field(
        attribute="polo",
        column_name="polo",
        widget=ForeignKeyWidget(Polo, field="nome"),
    )

    class Meta:
        model = CursoPolo
        export_order = ["curso", "polo", "active"]
        import_id_fields = (
            "curso",
            "polo",
        )
        fields = export_order
        skip_unchanged = True
