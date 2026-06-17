from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from content.models import Article
from content.seo_redirects import (
    ARTICLE_SITEMAP_EXCLUDE_SLUGS,
    category_published_article_filter,
    indexable_categories_queryset,
)
from ainews.models import AINewsItem
from companies.models import Company
from companies.indexing import indexable_companies_queryset


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # Keep deterministic ordering so sitemap pagination is stable.
        # Exclude duplicate-topic slugs that 301 to a canonical article.
        return (
            Article.objects.filter(status='published')
            .exclude(slug__in=ARTICLE_SITEMAP_EXCLUDE_SLUGS)
            .order_by('-updated_at', '-id')
        )

    def lastmod(self, obj):
        return obj.last_reality_check or (obj.updated_at.date() if obj.updated_at else None)


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        # Match category_detail: only index categories with 3+ canonical articles.
        return indexable_categories_queryset()


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
        static = [
            'home',
            'about',
            'editorial',
            'escape_plan',
            'privacy_policy',
            'contact',
            'terms',
            'topic_clusters',
            'career_reality_index',
            'company_directory',
        ]
        # Only list AI Pulse hub when published items exist (matches view noindex gate).
        if AINewsItem.objects.filter(status='published').exists():
            static.append('ai_news_hub')
        return static

    def location(self, item):
        return reverse(item)


class ToolSitemap(Sitemap):
    """High-intent free tools — primary traffic acquisition pages."""
    changefreq = "weekly"
    priority = 0.85

    def items(self):
        return [
            'salary_calculator',
            'analyzer_home',
            'layoff_radar',
            'salary_reality',
        ]

    def location(self, item):
        return reverse(item)


class CompanySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        # Only companies with community data (reviews or salaries) — matches detail-page index gate.
        return indexable_companies_queryset().order_by("-salary_count", "name")

    def lastmod(self, obj):
        return obj.updated_at


SITEMAPS = {
    "tools": ToolSitemap,
    "articles": ArticleSitemap,
    "categories": CategorySitemap,
    "static": StaticViewSitemap,
    "ainews": AINewsSitemap,
    "companies": CompanySitemap,
}
