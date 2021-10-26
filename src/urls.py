from django.urls import path, include
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from avaportal.views import index, sync_up, health

urlpatterns = [
    path('health/', health),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('admin/login/', RedirectView.as_view(url='/oauth/login/suap/')),
    path('admin/', admin.site.urls),
    path('api/moodle_suap/', sync_up),
    path('ava/barramento/api/moodle_suap/', sync_up), 
    path('', index),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('/__debug__/', include(debug_toolbar.urls)))
