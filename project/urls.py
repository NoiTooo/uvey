from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import TemplateView

from .sitemaps import (
    ArticleSitemap,
    IndexSitemap,
    SearchResultSitemap,
    StaticViewSitemap,
)

sitemaps = {
    'article': ArticleSitemap,
    'index': IndexSitemap,
    'search': SearchResultSitemap,
    'static': StaticViewSitemap,
}

admin.site.site_title = 'UVEY Tree—Management screen'
admin.site.site_header = '【UVEY】Management screen'
admin.site.index_title = 'UVEY'

urlpatterns = [
    path('', include('article.urls')),
    path('admin/', admin.site.urls),
    # path('account/', include('register.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    # article/templates内にrobots.txtが入っている
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
