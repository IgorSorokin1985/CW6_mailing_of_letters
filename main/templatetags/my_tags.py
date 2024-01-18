from django import template

register = template.Library()

@register.filter
def my_media(val):
    """
    This tag for media files.
    """
    if val:
        return f'/media/{val}'
    else:
        return '#'
