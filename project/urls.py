from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from .sitemaps import (
    ArticleSitemap,
    StaticViewSitemap,
    SearchResultSitemap,
)

sitemaps = {
    'Subsidy': ArticleSitemap,
    'static': StaticViewSitemap,
    'search': SearchResultSitemap,
}

admin.site.site_title = 'UVEY Tree—Management screen'
admin.site.site_header = '【UVEY】Management screen'
admin.site.index_title = 'UVEY'

urlpatterns = [
    path('', include('article.urls')),
    path('admin/', admin.site.urls),
    # path('account/', include('register.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
