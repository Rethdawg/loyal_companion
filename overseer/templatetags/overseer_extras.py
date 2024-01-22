from django import template

register = template.Library()


@register.filter
def truncate(text):
    return text[:50]
