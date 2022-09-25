
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
    path('account/', include('account.urls')),
    path('post/', include('post.urls')),
    path('admin/', admin.site.urls),
]
