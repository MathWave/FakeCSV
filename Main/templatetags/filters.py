from django import template
from json import dumps


register = template.Library()


@register.filter('serialize')
def serialize(d):
    return dumps(d)


@register.filter('index')
def index(collection, i):
    return collection[i]


@register.filter('indexof')
def indexof(collection, entity):
    return collection.index(entity)
