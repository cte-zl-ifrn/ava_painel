from import_export.resources import ModelResource
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, DateTimeWidget
from .models import Ambiente, Campus, Curso, Polo, Papel, Usuario, VinculoPolo, VinculoCurso, CursoPolo


class AmbienteResource(ModelResource):
    class Meta:
        model = Ambiente
        export_order = (
            "nome",
            "url",
            "token",
            "cor_mestra",
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
        export_order = ("sigla", "ambiente", "suap_id", "active")
        import_id_fields = ("sigla",)
        fields = export_order
        skip_unchanged = True


class PapelResource(ModelResource):
    class Meta:
        model = Papel
        export_order = ["papel", "sigla", "nome", "contexto", "active"]
        import_id_fields = ("papel",)
        fields = export_order
        skip_unchanged = True


class CursoResource(ModelResource):
    class Meta:
        model = Curso
        export_order = ("codigo", "nome", "descricao", "suap_id")
        import_id_fields = ("codigo",)
        fields = export_order
        skip_unchanged = True


class CursoVinculoResource(ModelResource):
    """
    SELECT      au.username,
                pc.codigo,
                pp.papel,
                pcc.sigla,
                pvc.active
    FROM        painel_vinculocurso pvc
                    INNER JOIN a4_usuario au ON (pvc.colaborador_id = au.id)
                    INNER JOIN painel_curso pc ON (pvc.curso_id = pc.id)
                    INNER JOIN painel_papel pp ON (pvc.papel_id=pp.id)
                    INNER JOIN painel_campus pcc ON (pvc.campus_id=pcc.id)
    """

    colaborador = Field(
        attribute="colaborador",
        column_name="colaborador",
        widget=ForeignKeyWidget(Usuario, field="username"),
    )

    curso = Field(
        attribute="curso",
        column_name="curso",
        widget=ForeignKeyWidget(Curso, field="codigo"),
    )

    papel = Field(
        attribute="papel",
        column_name="papel",
        widget=ForeignKeyWidget(Papel, field="papel"),
    )

    campus = Field(
        attribute="campus",
        column_name="campus",
        widget=ForeignKeyWidget(Campus, field="sigla"),
    )

    class Meta:
        model = VinculoCurso
        export_order = ["colaborador", "curso", "papel", "campus", "active"]
        import_id_fields = (
            "colaborador",
            "curso",
            "papel",
            "campus",
        )
        fields = export_order
        skip_unchanged = True


class PoloResource(ModelResource):
    class Meta:
        model = Polo
        export_order = ["suap_id", "nome"]
        import_id_fields = ("suap_id",)
        fields = export_order
        skip_unchanged = True


class PoloCursoResource(ModelResource):
    """
    SELECT      pc.codigo curso,
                pcc.sigla campus,
                pp.suap_id polo,
                pvc.active
    FROM        painel_cursopolo pvc
                    INNER JOIN painel_polo pp ON (pvc.polo_id=pp.id)
                    INNER JOIN painel_curso pc ON (pvc.curso_id = pc.id)
                    INNER JOIN painel_campus pcc ON (pvc.campus_id = pcc.id)
    """

    curso = Field(
        attribute="curso",
        column_name="curso",
        widget=ForeignKeyWidget(Curso, field="codigo"),
    )

    polo = Field(
        attribute="polo",
        column_name="polo",
        widget=ForeignKeyWidget(Polo, field="suap_id"),
    )

    campus = Field(
        attribute="campus",
        column_name="campus",
        widget=ForeignKeyWidget(Campus, field="sigla"),
    )

    class Meta:
        model = CursoPolo
        export_order = ["curso", "polo", "active"]
        import_id_fields = ("curso", "polo")
        fields = export_order
        skip_unchanged = True


class PoloVinculoResource(ModelResource):
    """
    SELECT      au.username colaborador,
                ppp.suap_id polo,
                pp.papel,
                pvp.active
    FROM        painel_vinculopolo pvp
                    INNER JOIN a4_usuario au ON (pvp.colaborador_id = au.id)
                    INNER JOIN painel_papel pp ON (pvp.papel_id=pp.id)
                    INNER JOIN painel_polo ppp ON (pvp.polo_id = ppp.id)
    """

    colaborador = Field(
        attribute="colaborador",
        column_name="colaborador",
        widget=ForeignKeyWidget(Usuario, field="username"),
    )

    polo = Field(
        attribute="polo",
        column_name="polo",
        widget=ForeignKeyWidget(Polo, field="suap_id"),
    )

    papel = Field(
        attribute="papel",
        column_name="papel",
        widget=ForeignKeyWidget(Papel, field="papel"),
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
