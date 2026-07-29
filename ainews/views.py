import re

from django.core.paginator import Paginator
from django.core.cache import cache
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render
from django.utils.html import strip_tags
from django.utils import timezone
from django.views.decorators.cache import cache_page
from datetime import timezone as dt_timezone
from datetime import timedelta

from .models import AINewsItem, AITag
from .indexing import indexable_ai_news_queryset, item_is_indexable


TAG_PREFETCH = Prefetch("tags", queryset=AITag.objects.only("id", "name", "slug").order_by("name"))


def _extract_faqs(html):
    """Pull FAQ question/answer pairs from article summary HTML.

    Looks for the pattern: <h2>Frequently Asked Questions</h2>
    followed by <h3>question</h3><p>answer</p> pairs.
    Returns list of (question, answer) tuples.
    """
    faq_section = re.split(r'<h2[^>]*>\s*Frequently Asked Questions\s*</h2>', html, flags=re.IGNORECASE)
    if len(faq_section) < 2:
        return []
    faq_block = faq_section[1]
    questions = re.findall(r'<h3[^>]*>(.*?)</h3>', faq_block, flags=re.DOTALL)
    answers = re.findall(r'<p[^>]*>(.*?)</p>', faq_block, flags=re.DOTALL)
    return list(zip(questions, answers))


def _seo(title, description):
    return {
        "og_title": title,
        "og_description": description,
        "twitter_title": title,
        "twitter_description": description,
    }


def _ai_evolution_timeline():
    return [
        {
            "date": timezone.datetime(2017, 6, 12, tzinfo=dt_timezone.utc),
            "label": "2017",
            "title": "Transformer Era Begins",
            "note": "The transformer architecture became the base layer for modern language models.",
        },
        {
            "date": timezone.datetime(2020, 6, 11, tzinfo=dt_timezone.utc),
            "label": "2020",
            "title": "Foundation Models Expand",
            "note": "Large pretrained models proved one base model can support many downstream tasks.",
        },
        {
            "date": timezone.datetime(2022, 11, 30, tzinfo=dt_timezone.utc),
            "label": "Late 2022",
            "title": "Chat UX Breakout",
            "note": "Conversational AI moved from niche tooling into mainstream daily usage.",
        },
        {
            "date": timezone.datetime(2023, 1, 1, tzinfo=dt_timezone.utc),
            "label": "2023",
            "title": "Copilot Adoption Wave",
            "note": "Coding, support, and productivity copilots entered enterprise workflows.",
        },
        {
            "date": timezone.datetime(2024, 1, 1, tzinfo=dt_timezone.utc),
            "label": "2024",
            "title": "Multimodal + Open Models",
            "note": "Text, image, audio, and open-model ecosystems accelerated in parallel.",
        },
        {
            "date": timezone.datetime(2025, 1, 1, tzinfo=dt_timezone.utc),
            "label": "2025",
            "title": "Reasoning + Agent Systems",
            "note": "Teams shifted from prompt demos to orchestrated, evaluation-driven AI systems.",
        },
        {
            "date": timezone.datetime(2026, 1, 1, tzinfo=dt_timezone.utc),
            "label": "Now (2026)",
            "title": "AI as Core Operating Layer",
            "note": "Business edge now depends on reliability, governance, and workflow integration.",
        },
    ]


def _timeline_position_for_item(item_dt):
    timeline = _ai_evolution_timeline()
    position = timeline[0]
    for milestone in timeline:
        if item_dt >= milestone["date"]:
            position = milestone
        else:
            break
    return position
@cache_page(60 * 10)
def ai_news_hub(request):
    items = indexable_ai_news_queryset().prefetch_related(TAG_PREFETCH)
    tags = cache.get("ainews_hub_tags")
    if tags is None:
        tags = list(AITag.objects.only("id", "name", "slug").order_by("name"))
        cache.set("ainews_hub_tags", tags, 900)

    active_tag_slug = request.GET.get("tag")
    active_tag = None
    if active_tag_slug:
        active_tag = next((tag for tag in tags if tag.slug == active_tag_slug), None)
        if active_tag:
            items = items.filter(tags__slug=active_tag.slug)

    paginator = Paginator(items, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    title = "AI at Work — IT Workplace Impact | Career Reality"
    description = (
        "Curated AI developments that affect Indian IT teams: hiring, security, "
        "productivity tools, and policy — not research paper noise."
    )

    # Noindex if hub has zero items OR the view is query-param filtered (to avoid
    # duplicate content against the canonical /ai/tag/<slug>/ pages).
    meta_robots = "noindex, follow" if (paginator.count == 0 or active_tag_slug) else "index, follow"

    return render(
        request,
        "ainews/ai_news_hub.html",
        {
            "page_obj": page_obj,
            "tags": tags,
            "active_tag": active_tag,
            "ai_evolution_timeline": _ai_evolution_timeline(),
            "meta_robots": meta_robots,
            **_seo(title, description),
        },
    )
@cache_page(60 * 10)
def ai_news_detail(request, slug):
    from django.http import HttpResponsePermanentRedirect
    from django.urls import reverse

    item = (
        AINewsItem.objects.prefetch_related(TAG_PREFETCH)
        .filter(slug=slug)
        .first()
    )
    # Draft / pruned / stale items used to 404 with noindex and clutter GSC.
    # Consolidate crawl signals onto the hub instead.
    if item is None or item.status != "published" or not item_is_indexable(item):
        return HttpResponsePermanentRedirect(reverse("ai_news_hub"))

    related_items = indexable_ai_news_queryset().exclude(id=item.id)[:4]
    effective_reviewed_at = item.last_verified_at or item.reviewed_at or item.published_at
    stale_cutoff = timezone.now() - timedelta(days=21)
    content_is_stale = bool(effective_reviewed_at and effective_reviewed_at < stale_cutoff)

    title = f"{item.title} - AI Pulse | Career Reality"
    # Use career_angle for meta description (career-first), fall back to stripped summary
    if item.career_angle:
        description = strip_tags(item.career_angle)[:160]
    else:
        description = strip_tags(item.summary)[:160] if item.summary else title

    faqs = _extract_faqs(item.summary) if item.summary else []
    timeline = _ai_evolution_timeline()
    meta_robots = "noindex, follow" if content_is_stale else "index, follow"

    return render(
        request,
        "ainews/ai_news_detail.html",
        {
            "item": item,
            "related_items": related_items,
            "faqs": faqs,
            "effective_reviewed_at": effective_reviewed_at,
            "content_is_stale": content_is_stale,
            "ai_evolution_timeline": timeline,
            "timeline_position": _timeline_position_for_item(item.event_date or item.published_at),
            "meta_robots": meta_robots,
            **_seo(title, description),
        },
    )
@cache_page(60 * 10)
def ai_news_by_tag(request, slug):
    tag = get_object_or_404(AITag, slug=slug)
    items = indexable_ai_news_queryset().filter(tags=tag).prefetch_related(TAG_PREFETCH)

    paginator = Paginator(items, 15)
    # Empty tag archives are soft-404 bait in GSC ("Crawled - currently not indexed").
    # Hard 404 so Google drops them instead of keeping thin shells in the crawl queue.
    if paginator.count == 0:
        from django.http import Http404
        raise Http404("No AI updates for this tag.")

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    title = f"{tag.name} - AI Pulse | Career Reality"
    description = f"AI developments tagged '{tag.name}' - curated for career-aware tech professionals in India."

    # Noindex thin tag pages to avoid AdSense "low value content" flag
    meta_robots = "noindex, follow" if paginator.count < 3 else "index, follow"

    response = render(
        request,
        "ainews/ai_news_by_tag.html",
        {
            "tag": tag,
            "page_obj": page_obj,
            "meta_robots": meta_robots,
            **_seo(title, description),
        },
    )
    if meta_robots.startswith("noindex"):
        response["X-Robots-Tag"] = "noindex, follow"
    return response
