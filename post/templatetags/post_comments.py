from django import template

from post.models import PostComment

register = template.Library()

def getAllCommentsByPost(value):
    print("value", value.description)
    return PostComment.objects.filter(for_post=value)

# register isLiked function
register.filter('getCommentsOfPost', getAllCommentsByPost)
