from django import template
from sprinklercontrolapp.models import Sprinkler

register = template.Library()

@register.simple_tag
def sprinkler_count():
    return Sprinkler.objects.count()

@register.filter(name='access')
def access(value, arg):
    return value[arg]

@register.filter(name='datetime')
def todate(value):
    return value.strftime("%m")