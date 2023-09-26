from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from middleware.models import Solicitacao


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    # https://ead.ifrn.edu.br/ava/academico/lib/ajax/service.php?info=core_course_get_enrolled_courses_by_timeline_classification
    return render(request, "painel/dashboard.html")


@login_required
def syncs(request: HttpRequest, id_diario: int) -> HttpResponse:
    solicitacoes = Solicitacao.objects.by_diario_id(id_diario)
    return render(request, "painel/syncs.html", context={"solicitacoes": solicitacoes})
