from ninja import NinjaAPI
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
from .services import get_disciplinas, get_situacoes, get_semestres, get_diarios, get_informativos


api = NinjaAPI(docs_decorator=staff_member_required)


@api.get("/disciplinas/")
def disciplinas(request):
    return get_disciplinas(request.user.username)


@api.get("/situacoes/")
def situacoes(request):
    return get_situacoes()


@api.get("/semestres/")
def semestres(request):
    return get_semestres(request.user.username)


@api.get("/diarios/")
def diarios(request, student: int = 1, disciplina: str = None, situacao: str = None, semestre: str = None):
    return get_diarios(student, request.user.username, disciplina, situacao, semestre)

@api.get("/informativos/")
def informativos(request):
    return get_informativos(request.user.username)


@api.get("/notificacoes/")
def informativos(request):
    return get_informativos(request.user.username)


@api.get("/mensagens/")
def informativos(request):
    return get_informativos(request.user.username)
