from django.conf import settings


def seo_defaults(request):
    # Build canonical URL without query parameters to prevent duplicate indexing.
    path = request.path
    canonical_url = f"{settings.CANONICAL_BASE_URL}{path}"

    # Keep header category navigation populated across all templates.
    # Only show categories that have at least one published article.
    # Cached for 1 hour to avoid a DB hit on every uncached page request.
    from django.core.cache import cache
    categories = cache.get('nav_categories')
    if categories is None:
        try:
            from django.db.models import Count, Q
            from content.models import Category
            categories = list(Category.objects.annotate(
                article_count=Count('article', filter=Q(article__status='published'))
            ).filter(article_count__gt=0).order_by('order', 'name'))
            cache.set('nav_categories', categories, 3600)
        except Exception:
            categories = []

    return {
        "article_meta_title": "",
        "article_meta_description": "",
        "og_type": "",
        "og_title": "",
        "og_description": "",
        "og_image": "",
        "twitter_title": "",
        "twitter_description": "",
        "twitter_image": "",
        "meta_robots": "index, follow",
        "site_base_url": settings.CANONICAL_BASE_URL,
        "canonical_url": canonical_url,
        "categories": categories,
    }

