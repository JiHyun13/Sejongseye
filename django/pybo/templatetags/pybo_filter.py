from django import template

register = template.Library()

@register.filter
def sub(val, arg):
    return val - arg

@register.filter
def toStr(val):
    return str(val)