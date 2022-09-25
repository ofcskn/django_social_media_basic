from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name  = "account"
urlpatterns = [
    path('login', views.LoginView.as_view(), name="login",),
    path('register', views.RegisterView.as_view(), name="register"),
    path('profile', views.profile, name="profile"),
    path('logout', views.logout, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)