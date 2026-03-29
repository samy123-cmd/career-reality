from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from content.models import Article, Category
from ainews.models import AINewsItem


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # Keep deterministic ordering so sitemap pagination is stable.
        return Article.objects.filter(status='published').order_by('-updated_at', '-id')

    def lastmod(self, obj):
        return obj.last_reality_check


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Category.objects.all()


class AINewsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return AINewsItem.objects.filter(status='published').order_by('-reviewed_at', '-published_at')

    def lastmod(self, obj):
        return obj.reviewed_at or obj.published_at


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        # Only include pages that are actually indexable.
        # revenue_model, sponsorship_policy, and analyzer_home are noindexed
        # and must NOT appear here (contradicts the noindex directive).
        return [
            'home',
            'about',
            'editorial',
            'salary_reality',
            'salary_calculator',
            'privacy_policy',
            'contact',
            'terms',
            'topic_clusters',
            'career_reality_index',
            'ai_news_hub',
        ]

    def location(self, item):
        return reverse(item)
