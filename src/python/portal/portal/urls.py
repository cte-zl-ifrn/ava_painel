from django.urls import path
from .apps import PortalConfig
from .views import dashboard
from portal.api import api


app_name = PortalConfig.name


urlpatterns = [
    path("portal/api/v1/", api.urls),
    path('', dashboard, name="dashboard"),
]
