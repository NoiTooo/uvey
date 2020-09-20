from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import views

app_name = 'article'


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('search/', views.SearchResult.as_view(), name='search_result'),
    path('article/<int:pk>', views.Detail.as_view(), name='detail'),
    path('inquiry/', views.Inquiry.as_view(), name='inquiry'),
    path('inquiry/done/', views.InquiryDone.as_view(), name='inquiry_done'),
    path('privacy-policy/', views.PrivacyPolicy.as_view(), name='privacy_policy'),
    # path('post/', views.PostListView.as_view(), name='post_list'),
    # path('post/detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    # path('comment/<int:pk>/', views.CommentView.as_view(), name='comment'),
    # path('reply/<int:pk>/', views.ReplyView.as_view(), name='reply'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)