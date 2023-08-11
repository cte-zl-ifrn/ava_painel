from django.urls import path
from .apps import PainelConfig
from .views import dashboard
from painel.api import api


app_name = PainelConfig.name


urlpatterns = [
    path("painel/api/v1/", api.urls),
    path("", dashboard, name="dashboard"),
]
