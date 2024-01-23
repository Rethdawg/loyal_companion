from django import template
register = template.Library()


@register.inclusion_tag('memory_crystal/pagination.html')
def paginate(paginated_obj):
    return {'page_obj': paginated_obj}
