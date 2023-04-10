import json
from import_export.resources import ModelResource
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, DateTimeWidget

from .models import Ambiente, Campus, Curso


DEFAULT_DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'
DEFAULT_DATETIME_FORMAT_WIDGET = DateTimeWidget(format=DEFAULT_DATETIME_FORMAT)


class AmbienteResource(ModelResource):
    class Meta:
        model = Ambiente
        export_order = ('sigla', 'nome', 'url', 'token', 'cor_mestra', 'cor_degrade', 'cor_progresso', 'active')
        import_id_fields = ('sigla',)
        fields = export_order
        skip_unchanged = True


class CampusResource(ModelResource):
    ambiente = Field(attribute='ambiente', column_name='sigla_ambiente', widget=ForeignKeyWidget(Ambiente, field='sigla'))
    
    class Meta:
        model = Campus
        export_order = ('sigla', 'descricao', 'ambiente', 'suap_id', 'active')
        import_id_fields = ('sigla',)
        fields = export_order
        skip_unchanged = True


class CursoResource(ModelResource):
    class Meta:
        model = Curso
        export_order = ('codigo', 'nome', 'descricao', 'suap_id')
        import_id_fields = ('codigo',)
        fields = export_order
        skip_unchanged = True


# class CursoResource(resources.ModelResource):
#     class Meta:
#         model = Curso
#         export_order = ('nome', 'carga_horaria')
#         import_id_fields = ('nome',)
#         fields = export_order
#         skip_unchanged = True


# class AVAResource(resources.ModelResource):
#     instituicao = Field(attribute='instituicao', column_name='sigla_instituicao', widget=ForeignKeyWidget(Instituicao, field='sigla'))

#     class Meta:
#         model = AVA
#         export_order = ('nome', 'url', 'instituicao', 'tipo', 'token')
#         import_id_fields = ('url',)
#         fields = export_order
#         skip_unchanged = True
#         use_natural_foreign_keys = True


# class OfertaResource(resources.ModelResource):
#     curso = Field(attribute='curso', column_name='nome_curso', widget=ForeignKeyWidget(Curso, field='nome'))
#     ava = Field(attribute='ava', column_name='url_ava', widget=ForeignKeyWidget(AVA, field='url'))

#     class Meta:
#         model = Oferta
#         export_order = ('curso', 'ava', 'idnumber', 'url')
#         import_id_fields = ('curso','ava', 'idnumber')
#         fields = export_order
#         skip_unchanged = True


# class UsuarioResource(resources.ModelResource):
#     cpf = Field(attribute='username', column_name='cpf')
#     cadastrado_em = Field(attribute='date_joined', column_name='cadastrado_em', widget=DEFAULT_DATETIME_FORMAT_WIDGET)
#     primeiro_login_em = Field(attribute='first_login', column_name='primeiro_login_em', widget=DEFAULT_DATETIME_FORMAT_WIDGET)
#     ultimo_login_em = Field(attribute='last_login', column_name='ultimo_login_em', widget=DEFAULT_DATETIME_FORMAT_WIDGET)
#     aceitou_termo_uso_em = Field(attribute='aceitou_termo_uso_em', column_name='aceitou_termo_uso_em', widget=DEFAULT_DATETIME_FORMAT_WIDGET)
#     membro_da_equipe = Field(attribute='is_staff', column_name='membro_da_equipe')
#     ativo = Field(attribute='is_active', column_name='ativo')
 
#     class Meta:
#         model = Usuario
#         export_order = ('cpf', 'email', 'nome_completo', 'cadastrado_em', 'primeiro_login_em', 'ultimo_login_em', 'aceitou_termo_uso_em', 'ativo', 'membro_da_equipe')
#         import_id_fields = ('cpf',)
#         fields = export_order
#         skip_unchanged = True
#         # widgets = {
#         #     'cadastrado_em': {'format': DEFAULT_DATETIME_FORMAT},
#         #     'primeiro_login_em': {'format': DEFAULT_DATETIME_FORMAT},
#         #     'ultimo_login_em': {'format': DEFAULT_DATETIME_FORMAT},
#         #     'aceitou_termo_uso_em': {'format': DEFAULT_DATETIME_FORMAT},
#         # }

#     def dehydrate_fullname(self, obj):
#         first_name = getattr(obj, "first_name", "")
#         last_name = getattr(obj.author, "last_name", "")
#         return f'{first_name} {last_name}'.strip()


# class UsuarioMixin(resources.ModelResource):
#     usuario = Field(attribute='usuario', column_name='cpf', widget=ForeignKeyWidget(Usuario, field='username'))
#     email = Field(attribute='usuario__email', column_name='email')
#     nome_completo = Field(attribute='usuario__nome_completo', column_name='nome_completo')
#     cadastrado_em = Field(attribute='usuario__date_joined', column_name='cadastrado_em')
#     primeiro_login_em = Field(attribute='usuario__first_login', column_name='primeiro_login_em')
#     ultimo_login_em = Field(attribute='usuario__last_login', column_name='ultimo_login_em')
#     aceitou_termo_uso_em = Field(attribute='usuario__aceitou_termo_uso_em', column_name='aceitou_termo_uso_em')

#     class Meta:
#         model = Aluno
#         export_order = ('usuario', 'nome_completo', 'email', 'cadastrado_em', 'primeiro_login_em', 'ultimo_login_em', 'aceitou_termo_uso_em')
    

# class RepresentanteResource(UsuarioMixin):
#     papel = Field(attribute='papel', column_name='papel', )
#     instituicao = Field(attribute='instituicao', column_name='sigla_instituicao', widget=ForeignKeyWidget(Instituicao, field='sigla'))

#     def get_import_fields(self):
#         return [field for fieldname, field in self.fields.items() if fieldname in ('instituicao', 'papel', 'instituicao', 'usuario')]
    
#     class Meta:
#         model = Representante
#         export_order = ('papel', 'instituicao') + UsuarioMixin.Meta.export_order
#         import_id_fields = ('papel', 'instituicao', 'usuario')
#         fields = export_order
#         skip_unchanged = True

# class AlunoResource(UsuarioMixin, resources.ModelResource):
#     class Meta:
#         model = Aluno
#         export_order = UsuarioMixin.Meta.export_order
#         import_id_fields = ('usuario',)
#         fields = export_order
#         skip_unchanged = True


# class CertificadoResource(resources.ModelResource):
#     usuario = Field(attribute='usuario', column_name='cpf', widget=ForeignKeyWidget(Usuario, field='username'))
#     nome_completo = Field(attribute='aluno__usuario__nome_completo', column_name='nome_completo')
#     email = Field(attribute='aluno__usuario__email', column_name='email')
#     curso = Field(attribute='oferta__curso__nome', column_name='curso')
#     url_oferta = Field(attribute='oferta__ava__url', column_name='url_oferta')
#     idnumber_oferta = Field(attribute='oferta__idnumber', column_name='idnumber_oferta')
#     url_oferta = Field(attribute='oferta__url', column_name='url_oferta')

#     class Meta:
#         model = Certificado
#         export_order = ('usuario', 'nome_completo', 'email', 'curso', 'url_oferta', 'idnumber_oferta', 'url_oferta', 'codigo_validacao', 'url_validacao', 'conceito', 'recebido_em', 'gerado_em', 'iniciou_em')
#         import_id_fields = ('usuario',)
#         fields = export_order
#         skip_unchanged = True