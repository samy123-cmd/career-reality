from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from content.models import Article, Category

class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.last_reality_check

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return ['home', 'about', 'editorial', 'salary_reality', 'privacy_policy', 'analyzer_home']

    def location(self, item):
        return reverse(item)
