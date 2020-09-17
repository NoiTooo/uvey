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
    path('', views.Index.as_view(), name='index'),
    path('search/', views.SearchResult.as_view(), name='search_result'),
    path('article/<int:pk>', views.Detail.as_view(), name='detail'),
    path('inquiry/', views.Inquiry.as_view(), name='inquiry'),
    path('inquiry/done/', views.InquiryDone.as_view(), name='inquiry_done'),
    path('privacy-policy/', views.PrivacyPolicy.as_view(), name='privacy_policy')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)