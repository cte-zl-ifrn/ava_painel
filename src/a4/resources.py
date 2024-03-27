from import_export.resources import ModelResource
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, DateTimeWidget
from .models import Usuario
from painel.models import Campus


class UsuarioResource(ModelResource):
    """
    SELECT DISTINCT *
    FROM (
            SELECT "username",
                   "nome_registro",
                   "nome_usual",
                   "nome_social",
                   "email",
                   "email_secundario",
                   "email_google_classroom",
                   "email_academico",
                   "tipo_usuario",
                   "is_superuser",
                   "is_active",
                   "is_staff",
                   "foto",
                   "date_joined",
                   "first_login",
                   "last_login",
                   "last_json"
            FROM painel_vinculocurso pvc
                     INNER JOIN a4_usuario au ON (pvc.colaborador_id = au.id)
            UNION
            SELECT "username",
                   "nome_registro",
                   "nome_usual",
                   "nome_social",
                   "email",
                   "email_secundario",
                   "email_google_classroom",
                   "email_academico",
                   "tipo_usuario",
                   "is_superuser",
                   "is_active",
                   "is_staff",
                   "foto",
                   "date_joined",
                   "first_login",
                   "last_login",
                   "last_json"
            FROM painel_vinculopolo pvp
                     INNER JOIN a4_usuario au ON (pvp.colaborador_id = au.id)) t
    """

    campus = Field(
        attribute="campus",
        column_name="campus",
        widget=ForeignKeyWidget("painel.Campus", field="sigla"),
    )
    curso = Field(
        attribute="curso",
        column_name="curso",
        widget=ForeignKeyWidget("painel.Curso", field="codigo"),
    )
    polo = Field(
        attribute="polo",
        column_name="polo",
        widget=ForeignKeyWidget("painel.Polo", field="nome"),
    )

    class Meta:
        model = Usuario
        export_order = (
            "username",
            "nome_registro",
            "nome_usual",
            "nome_social",
            "email",
            "email_secundario",
            "email_google_classroom",
            "email_academico",
            "tipo_usuario",
            "is_superuser",
            "is_active",
            "is_staff",
            "polo",
            "campus",
            "curso",
            "foto",
            "last_json",
        )
        import_id_fields = ("username",)
        fields = export_order
        skip_unchanged = True
