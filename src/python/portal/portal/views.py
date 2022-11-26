from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    # campus = Campus.objects.filter(homepage=True)
    categorias = [
        {"titulo": "Todos", "url": "#todos", "current": True},
        {"titulo": "Meus cursos", "url": "#Meus_cursos", "current": False},
        {"titulo": "Destaques", "url": "#Destaques", "current": False},
        {"titulo": "Gestão", "url": "#Gestão", "current": False},
        {"titulo": "Administração", "url": "#Administração", "current": False},
        {"titulo": "Qualidade de vida", "url": "#qualidade", "current": False}
    ]
    # return render(request, 'portal/index.html', context={'categorias': categorias})
    return render(request, "portal/dashboard.html", context={'page_title': 'Dashboard v1'})
