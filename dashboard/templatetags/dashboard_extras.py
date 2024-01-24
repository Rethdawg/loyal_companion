from django import template
from weatherman.api_utils import call_or_retrieve_forecast, get_latlon_from_city
from django.contrib import messages
register = template.Library()


@register.inclusion_tag('dashboard/pagination.html')
def paginate(paginated_obj):
    return {'page_obj': paginated_obj}
