from django.urls import path
from .apps import AvaPortalConfig
from .views import dashboard, contacts, register, term_of_use
from .views import login, authenticate, health, index, raise_error, sync_up


app_name = AvaPortalConfig.name


urlpatterns = [
    path('contacts/', contacts, name="contacts"),
    path('register/', register, name="register"),
    path('term_of_use/', term_of_use, name="term_of_use"),
    path('login/', login, name="login"),
    path('authenticate/', authenticate, name="authenticate"),
    path('health/', health, name="health"),
    path('raise_error/', raise_error, name="raise_error"),
    path('api/moodle_suap/', sync_up, name="api_moodle_suap"),
    path('ava/barramento/api/moodle_suap/', sync_up, name="alias_to_api_moodle_suap"), 
    # path('', dashboard, name="dashboard"),
    path('', index, name="dashboard"),
]
