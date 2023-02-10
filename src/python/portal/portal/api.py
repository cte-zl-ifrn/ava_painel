from datetime import datetime
from ninja import NinjaAPI
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpRequest
from .services import get_diarios, get_atualizacoes_counts, set_favourite_course
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
    return get_diarios(
        username=settings.SUAP_PORTAL_FAKEUSER or request.user.username,
        semestre=semestre,
        situacao=situacao,
        disciplina=disciplina,
        curso=curso,
        arquetipo=arquetipo,
        ambiente=ambiente,
        q=q,
        page=page,
        page_size=page_size
    )

@api.get("/atualizacoes_counts/")
def atualizacoes_counts(request: HttpRequest):
    return get_atualizacoes_counts(request.user.username)

@api.get("/set_favourite/")
def set_favourite(request: HttpRequest, ava: str, courseid: int, favourite: int):
    return set_favourite_course(request.user.username, ava, courseid, favourite)
