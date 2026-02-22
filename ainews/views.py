from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils.html import strip_tags
from django.utils import timezone
from django.views.decorators.cache import cache_page
from datetime import timezone as dt_timezone

from .models import AINewsItem, AITag


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


@cache_page(300)
def ai_news_hub(request):
    items = AINewsItem.objects.filter(status="published").prefetch_related("tags")
    tags = AITag.objects.all()

    active_tag_slug = request.GET.get("tag")
    active_tag = None
    if active_tag_slug:
        active_tag = AITag.objects.filter(slug=active_tag_slug).first()
        if active_tag:
            items = items.filter(tags=active_tag)

    paginator = Paginator(items, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    title = "AI Pulse - Latest AI Developments for Your Career"
    description = "Track AI model releases, industry shifts, and career-impacting developments. Curated for Indian tech professionals."

    return render(
        request,
        "ainews/ai_news_hub.html",
        {
            "page_obj": page_obj,
            "tags": tags,
            "active_tag": active_tag,
            "ai_evolution_timeline": _ai_evolution_timeline(),
            **_seo(title, description),
        },
    )


@cache_page(300)
def ai_news_detail(request, slug):
    item = get_object_or_404(AINewsItem, slug=slug, status="published")
    related_items = (
        AINewsItem.objects.filter(status="published").exclude(id=item.id).order_by("-published_at")[:4]
    )

    title = f"{item.title} - AI Pulse | Career Reality"
    description = strip_tags(item.summary)[:160] if item.summary else title

    return render(
        request,
        "ainews/ai_news_detail.html",
        {
            "item": item,
            "related_items": related_items,
            "ai_evolution_timeline": _ai_evolution_timeline(),
            "timeline_position": _timeline_position_for_item(item.event_date or item.published_at),
            **_seo(title, description),
        },
    )


@cache_page(300)
def ai_news_by_tag(request, slug):
    tag = get_object_or_404(AITag, slug=slug)
    items = (
        AINewsItem.objects.filter(status="published", tags=tag).prefetch_related("tags").order_by("-published_at")
    )

    paginator = Paginator(items, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    title = f"{tag.name} - AI Pulse | Career Reality"
    description = f"AI developments tagged '{tag.name}' - curated for career-aware tech professionals in India."

    return render(
        request,
        "ainews/ai_news_by_tag.html",
        {
            "tag": tag,
            "page_obj": page_obj,
            **_seo(title, description),
        },
    )
