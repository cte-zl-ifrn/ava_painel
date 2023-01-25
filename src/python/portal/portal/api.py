from ninja import NinjaAPI
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
from .services import get_diarios, get_informativos
from .models import Arquetipo


api = NinjaAPI(docs_decorator=staff_member_required)


@api.get("/diarios/")
def diarios(
        request, 
        semestre: str = None,
        situacao: str = None,
        ordenacao: str = None,
        disciplina: str = None,
        curso: str = None,
        arquetipo: str = None,
        ambiente: str = None,
        q: str = None,
        page: int = 1,
        page_size: int = 9,
    ):
    return get_diarios(request.user.username, semestre, situacao, disciplina, curso, arquetipo, ambiente, q, page, page_size)
    # return get_diarios('1723011', semestre, situacao, disciplina, curso, arquetipo, ambiente, q, page, page_size)


@api.get("/informativos/")
def informativos(request):
    return get_informativos(request.user.username)


@api.get("/notificacoes/")
def informativos(request):
    return get_informativos(request.user.username)


@api.get("/mensagens/")
def informativos(request):
    return get_informativos(request.user.username)
