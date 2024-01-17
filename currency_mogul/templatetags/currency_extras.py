# Module containing some custom filters for the Django template language
from pathlib import Path
from loyal_companion.settings import BASE_DIR
from django import template
register = template.Library()


@register.filter
def file_exists(file_name):
    if Path(BASE_DIR / f'static/images/{file_name}').exists():
        return True
    else:
        return False



