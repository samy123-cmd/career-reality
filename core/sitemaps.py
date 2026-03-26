from django.contrib.sitemaps import Sitemap
from django.db.models import Count, Q
from django.urls import reverse
from content.models import Article, Category
from ainews.models import AINewsItem
from core.publishing import AI_SECTION_INDEXABLE, INDEXABLE_CATEGORY_MIN_ARTICLES


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # Keep deterministic ordering so sitemap pagination is stable.
        return Article.objects.filter(status='published').order_by('-updated_at', '-id')

    def lastmod(self, obj):
        return obj.last_reality_check or (obj.updated_at.date() if obj.updated_at else None)


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Category.objects.annotate(
            pub_count=Count('article', filter=Q(article__status='published'))
        ).filter(pub_count__gte=INDEXABLE_CATEGORY_MIN_ARTICLES).order_by('order', 'name')


class AINewsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        if not AI_SECTION_INDEXABLE:
            return AINewsItem.objects.none()
        return AINewsItem.objects.filter(status='published').order_by('-reviewed_at', '-published_at')

    def lastmod(self, obj):
        return obj.reviewed_at or obj.published_at


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return [
            'home',
            'about',
            'editorial',
            'salary_reality',
            'salary_calculator',
            'escape_plan',
            'privacy_policy',
            'contact',
            'terms',
            'topic_clusters',
            'career_reality_index',
        ]

    def location(self, item):
        return reverse(item)
