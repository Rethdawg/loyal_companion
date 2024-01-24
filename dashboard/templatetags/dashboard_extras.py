from django import template

register = template.Library()


@register.inclusion_tag('dashboard/pagination.html')
def paginate(paginated_obj):
    return {'page_obj': paginated_obj}
