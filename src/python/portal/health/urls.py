from django.urls import path
from .apps import HealthConfig
from .views import health


app_name = HealthConfig.name


urlpatterns = [
    path('health/', health, name="health"),
]
