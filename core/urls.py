from urllib import request
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

app_name  = "core"
urlpatterns = [
    # home page
    path('', login_required(views.HomeView.as_view()), name="home"),
    # posts from all users as random
    path('explore', views.explore, name="explore"),
    # profile of the user
    path('<str:user_name>', views.ProfileView.as_view(), name="get_user"),
    # followers of the user
    path('<str:user_name>/followers', views.get_followers_of_user, name="get_followers_of_user"),
    # saved posts of the user
    path('<str:user_name>/saved', views.saved_posts_of_user, name="saved_posts_of_user"),
    # liked posts of the user
    path('<str:user_name>/liked', views.liked_posts_of_user, name="liked_posts_of_user"),
    # follow the user
    path('<str:to_user_name>/follow', views.follow_user, name="follow_user"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)