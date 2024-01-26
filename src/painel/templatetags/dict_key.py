from django.template.defaultfilters import register


@register.filter(name="dict_key")
def dict_key(d, k, e=None):
    """Returns the given key from a dictionary."""
    return d.get(k) if d is not None else e
