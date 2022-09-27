from django import template

from post.models import PostAction

register = template.Library()

def isLiked(value, arg):
    return PostAction.objects.filter(user=arg,post=value, action_number=0).count() > 0

def isSaved(value, arg):
    return PostAction.objects.filter(user=arg,post=value, action_number=1).count() > 0

# register isLiked function
register.filter('isLiked', isLiked)
register.filter('isSaved', isSaved)
