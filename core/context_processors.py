from django.conf import settings

from core.seo_pages import SEO_PILLAR_ARTICLES, SEO_TOOL_HUB


def seo_defaults(request):
    path = request.path
    canonical_url = f"{settings.CANONICAL_BASE_URL}{path}"

    if path.startswith('/hi/'):
        en_path = path[3:]
        hi_path = path
    elif path == '/hi':
        en_path = '/'
        hi_path = path
    else:
        en_path = path
        hi_path = '/hi' + path

    en_canonical_url = f"{settings.CANONICAL_BASE_URL}{en_path}"
    hi_canonical_url = f"{settings.CANONICAL_BASE_URL}{hi_path}"

    from django.core.cache import cache
    from core.cache_utils import NAV_CATEGORIES_CACHE_KEY

    categories = cache.get(NAV_CATEGORIES_CACHE_KEY)
    if categories is None:
        try:
            from core.cache_utils import refresh_nav_categories_cache
            refresh_nav_categories_cache()
            categories = cache.get(NAV_CATEGORIES_CACHE_KEY) or []
        except Exception:
            categories = []

    is_hindi_duplicate = path.startswith('/hi/') or path == '/hi'
    meta_robots = "noindex, nofollow" if is_hindi_duplicate else "index, follow"
    canonical_url = en_canonical_url

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
        "meta_robots": meta_robots,
        "site_base_url": settings.CANONICAL_BASE_URL,
        "canonical_url": canonical_url,
        "en_canonical_url": en_canonical_url,
        "hi_canonical_url": hi_canonical_url,
        "categories": categories,
        "site_social_profiles": getattr(settings, "SITE_SOCIAL_PROFILES", []),
    }


def seo_internal_links(request):
    return {
        "seo_tool_hub": SEO_TOOL_HUB,
        "seo_pillar_articles": SEO_PILLAR_ARTICLES,
    }
