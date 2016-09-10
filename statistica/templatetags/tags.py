import json
from django import template

register = template.Library()

@register.filter(name='round_float')
def round_float(value):
    if isinstance(value,float):
        value = round(value,3)
    return value

@register.filter(name='to_json')
def to_json(value):
    return json.load(value)
