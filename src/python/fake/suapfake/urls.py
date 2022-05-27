from django.urls import path
from django.views.generic import RedirectView
from .apps import SuapFakeConfig
from .views import login, authenticate


app_name = SuapFakeConfig.name

urlpatterns = [
    path('login/', login, name="login"),
    path('authenticate/', authenticate, name="authenticate"),
    path('', RedirectView.as_view(url='/admin/suapfake/diario/')),
]
