from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    # https://ead.ifrn.edu.br/ava/academico/lib/ajax/service.php?info=core_course_get_enrolled_courses_by_timeline_classification
    return render(request, "painel/dashboard.html")
