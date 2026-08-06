import os
import time
import uuid
import logging

from django.conf import settings
from django.http import HttpResponsePermanentRedirect


logger = logging.getLogger(__name__)


class CanonicalHostRedirectMiddleware:
    """
    Enforce one canonical host in production deployments.
    Keeps redirects permanent so search engines consolidate signals.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG:
            return self.get_response(request)

        host = request.get_host().split(":")[0].lower()
        # Django test client + local loopback must never 301.
        if host in {"testserver", "localhost", "127.0.0.1"}:
            return self.get_response(request)

        explicit = os.environ.get("ENFORCE_CANONICAL_HOST", "").lower()
        if explicit in ("0", "false", "no"):
            return self.get_response(request)

        deploy_env = (
            os.environ.get("DEPLOY_ENV") or os.environ.get("VERCEL_ENV") or ""
        ).lower()
        on_managed_host = bool(
            os.environ.get("FLY_APP_NAME")
            or os.environ.get("RAILWAY_ENVIRONMENT")
            or os.environ.get("RENDER")
        )
        should_enforce = (
            explicit in ("1", "true", "yes")
            or deploy_env == "production"
            or on_managed_host
        )
        if not should_enforce:
            return self.get_response(request)

        # Allow platform preview hosts without 301 loop during cutover.
        preview_suffixes = (
            ".fly.dev",
            ".onrender.com",
            ".up.railway.app",
            ".vercel.app",
        )
        if any(host.endswith(sfx) for sfx in preview_suffixes):
            return self.get_response(request)
        if host and host != settings.CANONICAL_HOST:
            return HttpResponsePermanentRedirect(
                f"{settings.CANONICAL_BASE_URL}{request.get_full_path()}"
            )
        return self.get_response(request)


class SecurityHeadersMiddleware:
    """
    Adds a conservative baseline of browser security headers.
    Designed to be safe for this content site without breaking existing pages.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        host = request.get_host().split(":")[0].lower()
        deploy_env = (
            os.environ.get("DEPLOY_ENV")
            or os.environ.get("VERCEL_ENV")
            or ("production" if not settings.DEBUG else "development")
        ).lower()

        # Keep platform preview hosts out of indexation.
        preview_host = host.endswith(
            (".vercel.app", ".fly.dev", ".onrender.com", ".up.railway.app")
        )
        if preview_host and deploy_env != "production":
            response["X-Robots-Tag"] = "noindex, nofollow"

        # Block /hi/ duplicate pages — no Hindi translations exist.
        if request.path.startswith("/hi/") or request.path == "/hi":
            response["X-Robots-Tag"] = "noindex, nofollow"

        # JSON/API endpoints must never appear as search documents.
        if request.path.startswith("/api/"):
            response["X-Robots-Tag"] = "noindex, nofollow"

        response.setdefault("X-Content-Type-Options", "nosniff")
        response.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.setdefault("X-Frame-Options", "DENY")
        response.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")

        # Conservative CSP tuned for current templates/assets.
        if "Content-Security-Policy" not in response:
            response["Content-Security-Policy"] = (
                "default-src 'self'; "
                "img-src 'self' data: https:; "
                "style-src 'self' 'unsafe-inline' https:; "
                "script-src 'self' 'unsafe-inline' https:; "
                "font-src 'self' data: https:; "
                "connect-src 'self' https:; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self';"
            )

        return response


class EdgeCacheHeadersMiddleware:
    """
    Attach CDN/proxy cache hints for anonymous public pages.
    Works alongside Django Redis cache_page — any edge (Fly proxy, Cloudflare,
    former Vercel CDN) can honor Cache-Control on full HTML responses.

    Also strips Set-Cookie on public cacheable GETs for anonymous users so the
    CDN can actually store the response (Set-Cookie forces cache bypass).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method != "GET":
            return response
        from core.cache_utils import apply_edge_cache_headers, edge_cache_ttl_for_path

        is_authenticated = bool(
            getattr(request, "user", None) and request.user.is_authenticated
        )
        apply_edge_cache_headers(
            response,
            request.path,
            is_authenticated=is_authenticated,
        )

        # Public article/tool HTML must be cookie-free for Googlebot + CDN.
        # Session/CSRF cookies on every hit force cache bypass and inflate TTFB.
        if (
            not is_authenticated
            and response.status_code in (200, 301, 308)
            and edge_cache_ttl_for_path(request.path) is not None
        ):
            if hasattr(response, "cookies"):
                response.cookies.clear()
            if "Set-Cookie" in response:
                try:
                    del response["Set-Cookie"]
                except KeyError:
                    pass

        return response


class RequestObservabilityMiddleware:
    """
    Adds lightweight request observability for production troubleshooting.
    - Assigns/propagates X-Request-ID.
    - Emits X-Response-Time-ms.
    - Logs slow requests above threshold.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.slow_request_threshold_ms = int(os.environ.get("SLOW_REQUEST_THRESHOLD_MS", "800"))

    def __call__(self, request):
        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
        request.request_id = request_id

        start = time.perf_counter()
        response = self.get_response(request)
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

        response["X-Request-ID"] = request_id
        response["X-Response-Time-ms"] = str(elapsed_ms)

        if elapsed_ms >= self.slow_request_threshold_ms:
            logger.warning(
                "Slow request | id=%s method=%s path=%s status=%s elapsed_ms=%s",
                request_id,
                request.method,
                request.path,
                getattr(response, "status_code", "?"),
                elapsed_ms,
            )

        return response
