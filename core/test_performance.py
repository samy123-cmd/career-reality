from django.core.cache import cache
from django.test import TestCase, RequestFactory, override_settings

from core.cache_utils import (
    SITEMAP_CACHE_KEY,
    apply_edge_cache_headers,
    edge_cache_ttl_for_path,
    fmt_count,
    get_cached_sitemap,
    invalidate_sitemap_cache,
    warm_page_cache,
)
from core.middleware import EdgeCacheHeadersMiddleware


class CacheUtilsTests(TestCase):
    def test_fmt_count_formats_large_numbers(self):
        self.assertEqual(fmt_count(12483), "12K+")
        self.assertEqual(fmt_count(847), "840+")

    def test_edge_cache_ttl_for_public_paths(self):
        self.assertEqual(edge_cache_ttl_for_path("/sitemap.xml"), 3600)
        self.assertEqual(edge_cache_ttl_for_path("/article/foo/"), 900)
        self.assertIsNone(edge_cache_ttl_for_path("/accounts/login/"))

    def test_apply_edge_cache_headers_skips_authenticated(self):
        from django.http import HttpResponse

        response = HttpResponse("ok")
        apply_edge_cache_headers(response, "/", is_authenticated=True)
        self.assertNotIn("s-maxage", response.get("Cache-Control", ""))

    def test_apply_edge_cache_headers_sets_smaxage_for_anonymous(self):
        from django.http import HttpResponse

        response = HttpResponse("ok")
        apply_edge_cache_headers(response, "/", is_authenticated=False)
        self.assertIn("s-maxage=60", response["Cache-Control"])

    def test_sitemap_cache_stores_xml(self):
        invalidate_sitemap_cache()
        calls = {"n": 0}

        def _gen():
            calls["n"] += 1
            return b"<urlset></urlset>"

        body1 = get_cached_sitemap(_gen)
        body2 = get_cached_sitemap(_gen)
        self.assertEqual(body1, body2)
        self.assertEqual(calls["n"], 1)
        self.assertIsNotNone(cache.get(SITEMAP_CACHE_KEY))


class EdgeCacheMiddlewareTests(TestCase):
    def test_middleware_adds_cache_control_on_home(self):
        def get_response(request):
            from django.http import HttpResponse
            return HttpResponse("home")

        middleware = EdgeCacheHeadersMiddleware(get_response)
        factory = RequestFactory()
        request = factory.get("/")
        request.user = type("U", (), {"is_authenticated": False})()
        response = middleware(request)
        self.assertIn("s-maxage", response.get("Cache-Control", ""))

    def test_middleware_strips_cookies_on_public_pages(self):
        def get_response(request):
            from django.http import HttpResponse
            response = HttpResponse("home")
            response.set_cookie("sessionid", "abc")
            response.set_cookie("csrftoken", "xyz")
            return response

        middleware = EdgeCacheHeadersMiddleware(get_response)
        factory = RequestFactory()
        request = factory.get("/article/example/")
        request.user = type("U", (), {"is_authenticated": False})()
        response = middleware(request)
        self.assertEqual(len(response.cookies), 0)
        self.assertIn("s-maxage", response.get("Cache-Control", ""))

    def test_apply_edge_cache_headers_drops_cookie_vary(self):
        from django.http import HttpResponse

        response = HttpResponse("ok")
        response["Vary"] = "Accept-Language, Cookie"
        apply_edge_cache_headers(response, "/article/foo/", is_authenticated=False)
        self.assertNotIn("Cookie", response["Vary"])
        self.assertIn("s-maxage=900", response["Cache-Control"])


class WarmPageCacheTests(TestCase):
    def test_warm_page_cache_hits_core_paths(self):
        summary = warm_page_cache(article_limit=0)
        self.assertGreaterEqual(summary["warmed"], 5)

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["www.careerreality.in"])
    def test_warm_page_cache_works_in_production_allowed_hosts(self):
        summary = warm_page_cache(article_limit=0)
        self.assertGreaterEqual(summary["warmed"], 5, msg=summary.get("failed"))
