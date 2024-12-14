from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from django.views.static import serve
from django.conf import settings
from finance_site.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('finance_site.urls')),
    path('users/', include('users.urls', namespace='users')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

handler404 = page_not_found
