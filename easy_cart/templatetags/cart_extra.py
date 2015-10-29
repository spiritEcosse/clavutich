__author__ = 'igor'
from django.utils.safestring import mark_safe
from django.utils.html import escapejs
import json
from django import template
register = template.Library()
from django.core import serializers


@register.filter
def to_js(value):
    """
    To use a python variable in JS, we call json.dumps to serialize as JSON server-side and reconstruct using
    JSON.parse. The serialized string must be escaped appropriately before dumping into the client-side code.
    """
    return json.dumps(value)
    return serializers.serialize('json', value)
