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
        if not settings.DEBUG and os.environ.get("VERCEL_ENV", "").lower() == "production":
            host = request.get_host().split(":")[0].lower()
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
        vercel_env = os.environ.get("VERCEL_ENV", "").lower()

        # Keep preview deployments out of indexation.
        if host.endswith(".vercel.app") and vercel_env != "production":
            response["X-Robots-Tag"] = "noindex, nofollow"

        # Block /hi/ duplicate pages — no Hindi translations exist.
        if request.path.startswith("/hi/"):
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
