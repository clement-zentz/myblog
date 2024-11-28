# blog/templatetags/svg_tags.py

from django import template
# from django.templatetags.static import static
from django.utils.safestring import mark_safe
import os
from django.conf import settings

register = template.Library()

@register.simple_tag
def load_svg(icon_name):
    svg_path = f'blog/icons/{icon_name}.svg'
    full_path = os.path.join(settings.STATIC_ROOT, svg_path)
    with open(full_path, 'r') as file:
        svg_content = file.read()
    return mark_safe(svg_content)