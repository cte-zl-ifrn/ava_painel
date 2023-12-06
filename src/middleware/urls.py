from django.urls import path
from .apps import MiddlewareConfig
from .views import sync_up_enrolments, sync_down_grades


app_name = MiddlewareConfig.name


urlpatterns = [
    path("api/moodle_suap/", sync_up_enrolments, name="api_sync_up_enrolments"),
    path("api/sync_down_grades/", sync_down_grades, name="api_sync_down_grades"),
]
