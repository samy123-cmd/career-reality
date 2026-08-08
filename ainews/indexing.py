"""Indexability rules for AI Pulse — aligned across views, sitemap, search."""

from __future__ import annotations

from datetime import timedelta

from django.db.models import Q, QuerySet
from django.utils import timezone
from django.utils.html import strip_tags

from ainews.impact_filters import has_it_workplace_impact, is_research_noise
from ainews.models import AINewsItem

STALE_DAYS = 21
MIN_CAREER_ANGLE_CHARS = 80
# Thin AI briefs are classic GSC "Crawled - currently not indexed" bait.
MIN_INDEXABLE_BODY_WORDS = 450


def _body_word_count(item: AINewsItem) -> int:
    text = f"{strip_tags(item.summary or '')} {strip_tags(item.career_angle or '')}"
    return len(text.split())


def indexable_ai_news_queryset() -> QuerySet[AINewsItem]:
    """
    Published AI items safe to index: IT workplace impact + editorial career_angle.
    """
    cutoff = timezone.now() - timedelta(days=STALE_DAYS)
    return (
        AINewsItem.objects.filter(status="published")
        .exclude(career_angle="")
        .filter(
            Q(last_verified_at__gte=cutoff)
            | Q(reviewed_at__gte=cutoff)
            | Q(published_at__gte=cutoff)
        )
        .order_by("-event_date", "-published_at")
    )


def item_is_indexable(item: AINewsItem) -> bool:
    if item.status != "published":
        return False
    career = (item.career_angle or "").strip()
    if len(career) < MIN_CAREER_ANGLE_CHARS:
        return False
    if _body_word_count(item) < MIN_INDEXABLE_BODY_WORDS:
        return False
    if is_research_noise(item.title, item.summary or "", item.source_name or ""):
        return False
    if not has_it_workplace_impact(
        item.title,
        item.summary or "",
        item.source_name or "",
        career,
    ):
        return False
    effective = item.last_verified_at or item.reviewed_at or item.published_at
    if effective and effective < timezone.now() - timedelta(days=STALE_DAYS):
        return False
    return True
