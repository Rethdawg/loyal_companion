from django import template

register = template.Library()


@register.filter
def truncate(text):
    return text[:50]


@register.inclusion_tag('overseer/pagination.html')
def paginate(paginated_obj):
    return {'page_obj': paginated_obj}
