from django.urls import path
from .apps import PortalConfig
from .views import sync_up


app_name = PortalConfig.name


urlpatterns = [
    path('api/moodle_suap/', sync_up, name="api_moodle_suap"),
]
