from django import template
from django.utils.encoding import uri_to_iri

register = template.Library()

def getStringFromUnicode(value):
    print(value)
    return uri_to_iri(value)

# register isLiked function
register.filter('getStringFromUnicode', getStringFromUnicode)
