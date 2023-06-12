from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from blog.views import pageNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

handler404 = pageNotFound
