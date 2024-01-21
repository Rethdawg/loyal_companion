# Custom tags for use in the app
from django import template
from memory_crystal.models import Category
register = template.Library()


@register.inclusion_tag('memory_crystal/offcanvas.html')
def render_offcanvas():
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}


@register.inclusion_tag('memory_crystal/pagination.html')
def paginate(paginated_obj):
    return {'page_obj': paginated_obj}
