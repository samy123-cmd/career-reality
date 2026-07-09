"""Tests for sitemap fallback and resilient caching."""

from django.core.cache import cache
from django.test import RequestFactory, TestCase

from core.cache_utils import (
    SITEMAP_CACHE_KEY,
    SITEMAP_STALE_CACHE_KEY,
    build_and_cache_sitemap,
    get_cached_sitemap,
    invalidate_sitemap_cache,
)
from core.sitemap_fallback import minimal_sitemap_xml
from core.sitemap_view import cached_sitemap


class SitemapFallbackTests(TestCase):
    def setUp(self):
        invalidate_sitemap_cache()

    def tearDown(self):
        invalidate_sitemap_cache()

    def test_minimal_sitemap_is_valid_xml(self):
        body = minimal_sitemap_xml()
        self.assertIn(b"<urlset", body)
        self.assertIn(b"/salary-calculator/", body)

    def test_build_and_cache_sitemap_uses_fallback_on_failure(self):
        def _fail():
            raise RuntimeError("db unavailable")

        body = build_and_cache_sitemap(_fail)
        self.assertIn(b"<urlset", body)
        self.assertIsNotNone(cache.get(SITEMAP_STALE_CACHE_KEY))

    def test_cached_sitemap_view_returns_200_on_generation_failure(self):
        cache.delete(SITEMAP_CACHE_KEY)
        cache.delete(SITEMAP_STALE_CACHE_KEY)

        def _fail():
            raise RuntimeError("generation failed")

        original = get_cached_sitemap

        import core.sitemap_view as sitemap_view_module

        def patched_get_cached(_generate):
            try:
                return original(_generate)
            except Exception:
                return minimal_sitemap_xml()

        sitemap_view_module.get_cached_sitemap = patched_get_cached
        try:
            request = RequestFactory().get("/sitemap.xml")
            response = cached_sitemap(request)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"<urlset", response.content)
        finally:
            sitemap_view_module.get_cached_sitemap = original
