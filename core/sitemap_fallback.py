"""Minimal sitemap XML when live generation or cache fails."""

from __future__ import annotations

from django.conf import settings
from django.urls import reverse


def minimal_sitemap_xml() -> bytes:
    """Return a small but valid sitemap with core public URLs."""
    base = settings.CANONICAL_BASE_URL.rstrip("/")
    paths = [
        reverse("home"),
        reverse("about"),
        reverse("editorial"),
        reverse("contact"),
        reverse("privacy_policy"),
        reverse("terms"),
        reverse("salary_calculator"),
        reverse("salary_reality"),
        reverse("analyzer_home"),
        reverse("layoff_radar"),
        reverse("career_reality_index"),
        reverse("topic_clusters"),
        reverse("company_directory"),
        reverse("escape_plan"),
    ]
    urls = "\n".join(
        f"  <url><loc>{base}{path}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>"
        for path in paths
    )
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n"
        "</urlset>\n"
    )
    return body.encode("utf-8")
