from sys import breakpointhook
from django.conf import settings
from django.utils.translation import gettext as _
from django.http import HttpRequest
from django.urls import reverse
from portal.models import Ambiente
from a4.models import logged_user


def layout_settings(request: HttpRequest) -> dict:
    usuario_personificado = request.session.get('usuario_personificado', None)
    return {
        "site_title": "Portal",
        "layout_home_url_name": "portal:dashboard",
        "layout_register_url_name": "portal:register",
        "layout_term_of_use_url_name": "portal:term_of_use",
        "layout_site_name": "Portal",
        "logged_user": logged_user(request),
        "suap_base_url": settings.SUAP_BASE_URL,
        "personificando": usuario_personificado is not None,
        # "layout_has_navbar_search": True,
        # "layout_has_fullscreen_toggler": True,
        # "layout_has_customizer": True,
        "layout_has_auth_remembering": True,
        "last_startup": settings.LAST_STARTUP,
        "portal_version": settings.PORTAL_VERSION,
        "gtag": settings.GTAG_CODE if hasattr(settings, 'GTAG_CODE') else False,
        "layout_auto_page_title": request.path.lower().replace("/", " ").lstrip().title(),
        "ambientes": Ambiente.objects.filter(active=True),
        "admins": Ambiente.admins(),
    }


def top_menu(request: HttpRequest) -> dict:
    staff_menus = [{"label": _("Admin"), "url": reverse('admin:index'), },] if request.user.is_staff else []
        
    return {
        "layout_navbar_top_menu":
        [
            {"label": _("Início"), "url": reverse('portal:dashboard'), },
        ] + staff_menus
    }


def user(request: HttpRequest) -> dict:
    return {
        "user_display_name": request.user.get_short_name() if hasattr(request.user, 'get_short_name') and request.user.get_short_name() else request.user.username,
        "user_profile_url": "#",
        "user_profile_thumbnail_url": '/static/adminlte3/img/avatar.png',
    }


def sidebar_menu(request: HttpRequest) -> dict:
    return {
        "layout_sidebar_menu":
        [
            {
                "label": _("Dashboard"), "url": "#", "icon": "fas fa-tachometer-alt", "color": "text-info", "is_active": True, 
                "subitens": [
                    {"label": _("Dashboard v1"), "url": "/", },
                    {"label": _("Dashboard v2"), "url": "/", },
                    {
                        "label": _("Dashboard v3"), "url": "/", 
                        "subitens": [
                            {"label": _("Dashboard v3.1"), "url": "/", },
                            {"label": _("Dashboard v3.2"), "url": "/", },
                            {"label": _("Dashboard v3.3"), "url": "/", },
                        ]
                    },
                ]
            },
            {"label": _("Contacts"), "url": "/contacts/", "icon": "fas fa-user",},
            {
                "label": _("Widgets"), "url": "#", "icon": "fas fa-th", "color": "text-warning",
                "badge": {"label": "new", "color": "badge-danger"},
            },
            {
                "label": _("Layout Options"), "url": "#", "icon": "fas fa-copy", "color": "text-danger",
                "badge": {"label": "6", "color": "badge-info"},
                "subitens": [
                    {
                        "label": _("Top Navigation"), "url": "#", 
                        "badge": {"label": "3", "color": "badge-info"},
                    },
                    {
                        "label": _("Top Navigation + Sidebar"), "url": "#", 
                        "badge": {"label": "3", "color": "badge-info"},
                    },
                    {"label": _("Boxed"), "url": "#", },
                    {"label": _("Fixed Sidebar"), "url": "#", },
                    {"label": _("Fixed Sidebar <small>+ Custom Area</small>"), "url": "#", },
                    {"label": _("Fixed Navbar"), "url": "#", },
                    {"label": _("Fixed Footer"), "url": "#", },
                    {"label": _("Collapsed Sidebar"), "url": "#", },
                ]
            },
            {"label": _("Charts"), "url": "/widgets/", "icon": "fas fa-chart-pie",},
            {"label": _("UI Elements"), "url": "/widgets/", "icon": "fas fa-tree",},
            {"label": _("Forms"), "url": "/widgets/", "icon": "fas fa-edit",},
            {"label": _("Tables"), "url": "/widgets/", "icon": "fas fa-table",},
            
            {"label": _("EXEMPLOS"),},
            {
                "label": _("Calendar"), "url": "/widgets/", "icon": "fas fa-calendar-alt",
                "badge": {"label": "2", "color": "badge-info"},
            },
            {"label": _("Gallery"), "url": "/widgets/", "icon": "fas fa-image",},
            {"label": _("Kanban board"), "url": "/widgets/", "icon": "fas fa-columns",},
            {"label": _("Mailbox"), "url": "/widgets/", "icon": "fas fa-envelope",},
            {"label": _("Pages"), "url": "/widgets/", "icon": "fas fa-book",},
            {
                "label": _("Extras"), "url": "/widgets/", "icon": "fas fa-plus-square",
                "subitens": [
                ]
            },
            {"label": _("Search"), "url": "/widgets/", "icon": "fas fa-search",},
            
            {"label": _("MISCELLANEOUS"),},
            {"label": _("Tabbed IFrame Plugin"), "url": "/widgets/", "icon": "fas fa-ellipsis-h",},
            {"label": _("Documentation"), "url": "/widgets/", "icon": "fas fa-file",},
            
        ]
    }


def messages(request: HttpRequest) -> dict:
    return {}
    return {
        "layout_navbar_message_bar":
            {
                "count": "+20",
                "see_all_url": "#",
                "messages": [
                    {
                        "message_url": "#",
                        "user_thumbnail_url": f"{settings.STATIC_URL}adminlte3/img/user1-128x128.jpg",
                        "user_name": "Brad Diesel",
                        "text": "Call me whenever you can...",
                        "since": "4 Hours Ago",
                        "star_color": "danger",
                    },
                    {
                        "message_url": "#",
                        "user_thumbnail_url": f"{settings.STATIC_URL}adminlte3/img/user8-128x128.jpg",
                        "user_name": "John Pierce",
                        "text": "I got your message bro",
                        "since": "4 Hours Ago",
                        "star_color": "muted",
                    },
                    {
                        "message_url": "#",
                        "user_thumbnail_url": f"{settings.STATIC_URL}adminlte3/img/user3-128x128.jpg",
                        "user_name": "Nora Silvester",
                        "text": "The subject goes here",
                        "since": "4 Hours Ago",
                        "star_color": "warning",
                    },
                ]
            }
    }


def notifications(request: HttpRequest) -> dict:
    return {}
    return {
        "layout_navbar_notifications_bar":
            {
                "count": "10",
                "count_label": _("{} notificações").format(215),
                "see_all_url": "#",
                "notification_group": [
                    {
                        "url": "#",
                        "label": _("{} novas mensagens").format(204),
                        "since": _("{} mins").format(4),
                        "icon": "fas fa-envelope",
                    },
                    {
                        "url": "#",
                        "label": _("{} requisições de amizade").format(8),
                        "since": _("{} horas").format(12),
                        "icon": "fas fa-users",
                    },
                    {
                        "url": "#",
                        "label": _("{} novos relatórios").format(3),
                        "since": _("{} days").format(2),
                        "icon": "fas fa-file",
                    },
                ]
            }
    }


def gtag(request):
    if getattr(settings, 'GTAG_ID', None) is not None:
        return {'gtag_id': settings.GTAG_ID}
    return {}
