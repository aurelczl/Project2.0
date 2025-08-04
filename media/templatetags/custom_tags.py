# myapp/templatetags/custom_tags.py

from django import template

register = template.Library()

@register.filter
def get_field_display(instance, field_name):
    value = getattr(instance, field_name)
    return value if value not in [None, '', []] else None
