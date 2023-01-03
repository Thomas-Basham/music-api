from django import template

register = template.Library()

@register.filter(name='set_var')
def setvar(val=None):
  return val