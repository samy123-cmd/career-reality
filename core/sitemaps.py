from django.contrib.sitemaps import Sitemap
from django.db.models import Count, Q
from django.urls import reverse
from content.models import Article, Category
from ainews.models import AINewsItem
from companies.models import Company


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
        # Include all categories with at least 1 published article.
        # Google values category/topic pages as long as they have real content —
        # even a single well-written article is better than a 404 exclusion.
        return Category.objects.annotate(
            pub_count=Count('article', filter=Q(article__status='published'))
        ).filter(pub_count__gte=1).order_by('order', 'name')


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
        # Exclude internal-facing pages (revenue_model, sponsorship_policy)
        # and near-empty tool pages (analyzer_home) that dilute content ratio.
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
            'ai_news_hub',
            'company_directory',
        ]

    def location(self, item):
        return reverse(item)


class CompanySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        # Only include companies with actual user-generated content (reviews)
        # or substantial descriptions (>200 chars) to avoid thin pages.
        return Company.objects.filter(
            is_verified=True,
            review_count__gte=1,
        ).order_by("-salary_count", "name")

    def lastmod(self, obj):
        return obj.updated_at
