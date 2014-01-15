__author__ = 'DarkSector'
from django import template

register = template.Library()


@register.filter
def cut(value, arg):
    return value.replace(arg, '')

@register.filter
def replacewithappname(value, app_name):
    replaced_app_name = '/'+app_name+'/'
    return value.replace('^', replaced_app_name)