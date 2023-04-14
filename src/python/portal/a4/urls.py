from django.urls import path
from .apps import A4Config
from .views import register, login, authenticate, logout
from .views import personificar, despersonificar


app_name = A4Config.name


urlpatterns = [
    path('register/', register, name="register"),
    path('login/', login, name="login"),
    path('authenticate/', authenticate, name="authenticate"),
    path('logout/', logout, name="logout"),
    path('personificar/<path:username>/', personificar, name="personificar"),
    path('despersonificar/', despersonificar, name="despersonificar"),
]
