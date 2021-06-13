from django import template
from json import dumps


register = template.Library()


@register.filter('serialize')
def serialize(d):
    return dumps(d)


@register.filter('enum')
def enum(collection):
    return enumerate(collection)
