from django.urls import path, include, re_path
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

admin.site.site_title = 'Portal AVA - Administração'
admin.site.site_header = admin.site.site_title

urlpatterns = [
    path('admin/login/', RedirectView.as_view(url='/login/')),
    path('admin/', admin.site.urls),
    path('', include('a4.urls')),
    path('', include('health.urls')),
    path('', include('middleware.urls')),
    path('', include('portal.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
        re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    ]

static_urlpatterns = [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('/__debug__/', include(debug_toolbar.urls)))
