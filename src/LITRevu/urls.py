from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import feed.views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', feed.views.feed, name='feed'),
    path('feed/', include("feed.urls")),
    path('authentication/', include("authentication.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
