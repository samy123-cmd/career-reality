"""Cached sitemap.xml view — avoids 5s+ regeneration on every Google crawl."""

import logging

from django.contrib.sitemaps.views import sitemap as django_sitemap
from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.http import require_GET

from core.cache_utils import (
    SITEMAP_CACHE_KEY,
    SITEMAP_STALE_CACHE_KEY,
    get_cached_sitemap,
    sitemap_cache_timeout,
)
from core.sitemap_fallback import minimal_sitemap_xml
from core.sitemaps import SITEMAPS

logger = logging.getLogger(__name__)


@require_GET
def cached_sitemap(request):
    def _generate() -> bytes:
        response = django_sitemap(request, sitemaps=SITEMAPS)
        if hasattr(response, "render"):
            response.render()
        return response.content

    try:
        body = get_cached_sitemap(_generate)
    except Exception:
        logger.exception("Sitemap cache/generation failed")
        body = cache.get(SITEMAP_STALE_CACHE_KEY) or minimal_sitemap_xml()

    if not body or not body.strip():
        body = cache.get(SITEMAP_STALE_CACHE_KEY) or minimal_sitemap_xml()

    response = HttpResponse(body, content_type="application/xml")
    response["Cache-Control"] = (
        f"public, s-maxage=3600, stale-while-revalidate={min(sitemap_cache_timeout(), 86400)}"
    )
    return response
