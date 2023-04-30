from django.urls import path
from .apps import MiddlewareConfig
from .views import moodle_suap


app_name = MiddlewareConfig.name


urlpatterns = [
    path("api/moodle_suap/", moodle_suap, name="api_moodle_suap"),
]
