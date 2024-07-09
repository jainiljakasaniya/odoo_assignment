from django import template

register = template.Library()

@register.filter
def get_item(array, index):
    try:
        return array[int(index)]
    except (IndexError, ValueError, TypeError):
        return None
