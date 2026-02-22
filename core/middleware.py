import os

from django.conf import settings
from django.http import HttpResponsePermanentRedirect


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
