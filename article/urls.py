from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import views

app_name = 'article'

admin.site.site_title = 'UVEY Tree—Management screen'
admin.site.site_header = '【UVEY】Management screen'
admin.site.index_title = 'UVEY'


urlpatterns = [
    path('', views.Index.as_view(), name = 'index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)