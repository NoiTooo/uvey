from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from article.models import Article


class ArticleSitemap(Sitemap):
    """
    記事のサイトマップ
    """
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Article.objects.filter(is_published=True)

    # モデルに get_absolute_url() が定義されている場合は不要
    def location(self, obj):
        return reverse('article:detail', args=[obj.pk])

    def lastmod(self, obj):
        return obj.updated_at


class IndexSitemap(Sitemap):
    """
    Index(TOP)ページのサイトマップ
    """
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return [
            'article:index',
        ]

    def location(self, item):
        return reverse(item)


class SearchResultSitemap(Sitemap):
    """
    検索結果ページのサイトマップ
    """
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return [
            'article:search_result',
        ]

    def location(self, item):
        return reverse(item)


class StaticViewSitemap(Sitemap):
    """
    静的ページのサイトマップ
    """
    changefreq = "monthly"
    priority = 0.3

    def items(self):
        return [
            'article:search_result',
            'article:inquiry',
            'article:privacy_policy',
        ]

    def location(self, item):
        return reverse(item)
