from django import template
from sprinklercontrolapp.models import Sprinkler

register = template.Library()

@register.simple_tag
def sprinkler_count():
    return Sprinkler.objects.count()

