from django import template

register = template.Library()

@register.filter(name='get_value')
def get_type(value):
    return type(value)
