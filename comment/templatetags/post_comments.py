from django import template

from post.models import PostComment

register = template.Library()

def getAllCommentsByPost(value):
    return PostComment.objects.filter(for_post=value)

def getLatestCommentsOfPost(value, count):
    return PostComment.objects.filter(for_post=value, sub_comment=None).order_by('-date')[:count]

def getLatestSubCommentsOfPost(value, count):
    return PostComment.objects.filter(sub_comment=value).order_by('-date')[:count]

# register isLiked function
register.filter('getCommentsOfPost', getAllCommentsByPost)
register.filter('getLatestCommentsOfPost', getLatestCommentsOfPost)
register.filter('getLatestSubCommentsOfPost', getLatestSubCommentsOfPost)
