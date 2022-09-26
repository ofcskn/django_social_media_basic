from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

app_name  = "account"
urlpatterns = [
    path('login', views.LoginView.as_view(), name="login",),
    path('register', views.RegisterView.as_view(), name="register"),
    path('profile', login_required(views.ProfileEditView.as_view()), name="profile"),
    path('change/password', login_required(views.ProfileChangePasswordView.as_view()), name="change_password"),
    path('logout', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name="logout"),
    # list following request by the logged user
    path('requests/following', views.following_requests, name="following_requests"),
    # accept the following request
    path('requests/following/<int:id>/accept', views.accept_following_request, name="accept_following_request"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)