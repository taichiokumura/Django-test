from django import template

register = template.Library()

@register.filter
def range_filter(value):
    return range(value)

@register.filter
def get_item(container, key):
    if isinstance(container, dict):
        return container.get(key)
    elif isinstance(container, list) and isinstance(key, int):
        return container[key]
    return None

