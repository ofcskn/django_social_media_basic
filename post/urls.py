from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

app_name  = "post"
urlpatterns = [
    path('<int:id>', views.DetailView.as_view(), name="detail"),
    path('create',  login_required(views.CreateView.as_view()), name="create"),
    path('<int:id>/action/<str:action_name>',  login_required(views.ActionView.as_view()), name="action"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)