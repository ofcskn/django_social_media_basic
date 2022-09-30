from django import template

from post.models import PostComment

register = template.Library()

def getAllCommentsByPost(value):
    return PostComment.objects.filter(for_post=value)

def getLatestCommentsOfPost(value, count):
    return PostComment.objects.filter(for_post=value).order_by('-date')[:count]

# register isLiked function
register.filter('getCommentsOfPost', getAllCommentsByPost)
register.filter('getLatestCommentsOfPost', getLatestCommentsOfPost)
