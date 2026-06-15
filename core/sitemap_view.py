"""Cached sitemap.xml view — avoids 5s+ regeneration on every Google crawl."""

from django.contrib.sitemaps.views import sitemap as django_sitemap
from django.http import HttpResponse
from django.views.decorators.http import require_GET

from core.cache_utils import get_cached_sitemap, sitemap_cache_timeout
from core.sitemaps import SITEMAPS


@require_GET
def cached_sitemap(request):
    def _generate() -> bytes:
        response = django_sitemap(request, sitemaps=SITEMAPS)
        if hasattr(response, "render"):
            response.render()
        return response.content

    body = get_cached_sitemap(_generate)
    response = HttpResponse(body, content_type="application/xml")
    response["Cache-Control"] = (
        f"public, s-maxage=3600, stale-while-revalidate={min(sitemap_cache_timeout(), 86400)}"
    )
    return response
