__author__ = 'DarkSector'
from django import template

register = template.Library()


@register.simple_tag
def cut(value, arg):
    return value.replace(arg, '')