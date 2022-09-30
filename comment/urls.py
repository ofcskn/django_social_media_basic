from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

app_name  = "comment"
urlpatterns = [
    path('send/to/<str:permalink>',  views.SendView.as_view(), name="send_comment_to_post"),
    path('edit/<int:id>',  views.EditView.as_view(), name="edit"),
    path('delete/<int:id>',  views.DeleteView.as_view(), name="delete"),
    path('reply/to/<int:id>',  views.ReplyView.as_view(), name="reply"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)