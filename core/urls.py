from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name  = "core"
urlpatterns = [
    # --------------------POST---------------------
    path('create_user', views.create_user, name="create_user"),
    path('create_post', views.create_post, name="create_post"),
    # ---------------------------------------------
    # home page
    path('', views.home, name="home"),
    # posts from all users as random
    path('explore', views.explore, name="explore"),
    # profile of the user
    path('<str:user_name>', views.get_user, name="get_user"),
    # followers of the user
    path('<str:user_name>/followers', views.get_followers_of_user, name="get_followers_of_user"),
    # saved posts of the user
    path('<str:user_name>/posts/saved', views.saved_posts_of_user, name="saved_posts_of_user"),
    # liked posts of the user
    path('<str:user_name>/posts/liked', views.liked_posts_of_user, name="liked_posts_of_user"),
    # create a post
    path('posts/create', views.create, name="create"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)