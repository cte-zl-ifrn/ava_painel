from django.templatetags.static import static
from django.utils.html import format_html
from django.template import Library


register = Library()


@register.simple_tag()
def boolean_icon(field_val):
    icon_url = static(
        "admin/img/icon-%s.svg"
        % {
            True: "yes",
            "True": "yes",
            False: "no",
            "False": "no",
            None: "unknown",
            "None": "unknown",
        }[field_val]
    )
    return format_html('<img src="{}" alt="{}">', icon_url, field_val)
