from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import escape
from django.views.decorators.cache import cache_page
from django.utils import timezone
import re
from .models import Article, Category, Author
from .editorial import (
    author_profile_is_indexable,
    build_article_sources,
    build_article_update_log,
    build_author_focus_areas,
    build_author_page_intro,
    build_category_profile,
    build_evidence_map,
)
from core.publishing import INDEXABLE_CATEGORY_MIN_ARTICLES


def _article_sources(article):
    return build_article_sources(article)


def _article_update_log(article):
    return build_article_update_log(article)


def _decision_framework(article):
    category_name = (article.category.name or "").lower()
    if "engineering" in category_name or "software" in category_name:
        return [
            "If salary delta is below 25 percent for a switch, optimize for skill depth and scope, not title.",
            "If your stack is legacy-only for 12+ months, schedule a transition plan before role lock-in compounds.",
            "If role ownership is high but pay is flat, use impact evidence to negotiate before switching."
        ]
    if "design" in category_name or "product" in category_name:
        return [
            "If your output is execution-only for multiple quarters, prioritize exposure to discovery and strategy work.",
            "If portfolio quality is improving but compensation is frozen, reprice in market every 12 months.",
            "If expectations are senior-level but authority is junior-level, document scope mismatch and renegotiate."
        ]
    return [
        "If your take-home is not compounding with experience, benchmark externally before accepting internal narratives.",
        "If role expectations keep rising without title/pay movement, escalate with documented outcomes.",
        "If growth path is unclear beyond 6-9 months, run a switch-or-specialize decision cycle."
    ]


def _mistake_checklist(article):
    category_name = (article.category.name or "").lower()
    items = [
        "Treating outlier salaries as planning baselines.",
        "Using title changes as a substitute for capability changes.",
        "Delaying market benchmarking until after compensation stagnates.",
    ]
    if "data" in category_name or "ai" in category_name:
        items.append("Over-indexing on model demos without production deployment depth.")
    if "product" in category_name:
        items.append("Confusing feature shipping speed with product impact.")
    return items


def _scenario_snapshot(article):
    category_name = (article.category.name or "").lower()
    if "engineering" in category_name or "software" in category_name:
        return "A mid-level developer with 5 years in a stable service role gets a title bump but no meaningful scope change. Within 12 months, market interview performance drops due to stale stack exposure."
    if "design" in category_name:
        return "A designer moves from visual-heavy delivery work to product discovery ownership. Compensation growth follows only after portfolio evidence shows shipped outcomes, not just polished screens."
    if "product" in category_name:
        return "A product manager ships high ticket volume but weak business outcomes. Career growth stalls until metric ownership is documented and tied to decision quality."
    return "A professional stays in-role despite rising responsibility and flat pay. Growth recovers only after external benchmarking and a deliberate switch-or-specialize decision."


def _reading_time_minutes(article):
    words = " ".join([
        article.target_persona or "",
        article.common_expectation or "",
        article.actual_reality or "",
        article.salary_reality or "",
        article.stuck_point or "",
        article.who_should_avoid or "",
        article.verdict or "",
    ])
    plain_words = len(re.sub(r"<[^>]+>", " ", words).split())
    minutes = max(4, round(plain_words / 220))
    return minutes


def _key_takeaways(article):
    """Generate article-specific takeaways from the article's own content
    instead of identical generic text across all articles (AdSense quality signal)."""
    from django.utils.html import strip_tags
    takeaways = []

    # First takeaway: from the verdict (the article's core conclusion)
    verdict_text = strip_tags(article.verdict).strip()
    if verdict_text:
        first_sentence = verdict_text.split('.')[0].strip()
        if first_sentence:
            takeaways.append(first_sentence + '.')

    # Second takeaway: from stuck_point (where people fail)
    stuck_text = strip_tags(article.stuck_point).strip()
    if stuck_text:
        first_sentence = stuck_text.split('.')[0].strip()
        if first_sentence:
            takeaways.append(first_sentence + '.')

    # Third takeaway: from who_should_avoid
    avoid_text = strip_tags(article.who_should_avoid).strip()
    if avoid_text:
        first_sentence = avoid_text.split('.')[0].strip()
        if first_sentence:
            takeaways.append(first_sentence + '.')

    # Fallback if content fields are too short
    if len(takeaways) < 2:
        takeaways.append(
            f"This analysis covers {article.category.name.lower()}"
            " career realities specific to the Indian market."
        )

    return takeaways[:3]


def _originality_moat(article):
    category = (article.category.name or "").lower()
    if "design" in category:
        return {
            "contrarian_thesis": "Visual polish is rarely the main bottleneck; strategic ownership is.",
            "non_obvious_signal": "When design reviews discuss output more than outcomes for multiple quarters, pay compression follows.",
        }
    if "product" in category:
        return {
            "contrarian_thesis": "Feature velocity without metric ownership weakens long-term career leverage.",
            "non_obvious_signal": "PM profiles with high ticket closure and low business impact evidence plateau fastest.",
        }
    if "engineering" in category or "software" in category:
        return {
            "contrarian_thesis": "Scope quality compounds career value faster than raw coding volume.",
            "non_obvious_signal": "Engineers anchored to legacy stacks lose negotiation leverage before they notice compensation drag.",
        }
    return {
        "contrarian_thesis": "Career outcomes usually degrade from quiet trade-offs, not sudden failures.",
        "non_obvious_signal": "When responsibility rises but decision rights stay flat, stagnation risk rises even before pay slows.",
    }


def _evidence_map(article, source_refs):
    return build_evidence_map(article, source_refs)

def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id, is_active=True)
    articles = list(
        Article.objects.filter(author=author, status='published')
        .select_related('category')
        .order_by('-published_at')
    )
    article_count = len(articles)
    coverage_areas = build_author_focus_areas(articles)
    meta_robots = "index, follow" if author_profile_is_indexable(author, article_count) else "noindex, follow"

    return render(request, 'content/author_detail.html', {
        'author': author,
        'articles': articles,
        'article_count': article_count,
        'coverage_areas': coverage_areas,
        'author_page_intro': build_author_page_intro(author, article_count, coverage_areas),
        'meta_robots': meta_robots,
    })
@cache_page(60 * 15)
def article_detail(request, slug):
    article = get_object_or_404(
        Article.objects.select_related('author', 'category'),
        slug=slug,
        status='published',
    )
    og_image_url = request.build_absolute_uri(reverse('article_og_image', args=[article.slug]))
    # Get related articles from the same category, excluding the current article
    related_articles = Article.objects.filter(
        category=article.category,
        status='published'
    ).exclude(id=article.id).select_related('category').order_by('-published_at')[:3]
    # Get all categories for internal linking
    categories = Category.objects.only('id', 'name', 'slug', 'order').order_by('order', 'name')
    source_refs = _article_sources(article)
    return render(request, 'content/article_detail.html', {
        'article': article,
        'related_articles': related_articles,
        'categories': categories,
        'source_references': source_refs,
        'update_log_items': _article_update_log(article),
        'decision_framework': _decision_framework(article),
        'mistake_checklist': _mistake_checklist(article),
        'scenario_snapshot': _scenario_snapshot(article),
        'reading_time': _reading_time_minutes(article),
        'key_takeaways': _key_takeaways(article),
        'originality': _originality_moat(article),
        'evidence_map': _evidence_map(article, source_refs),
        'article_meta_title': article.meta_title,
        'article_meta_description': article.meta_description,
        'og_type': 'article',
        'og_title': article.meta_title,
        'og_description': article.meta_description,
        'og_image': og_image_url,
        'twitter_title': article.meta_title,
        'twitter_description': article.meta_description,
        'twitter_image': og_image_url,
    })
@cache_page(60 * 15)
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    og_title = f"{category.name} Careers in India - Career Reality"
    og_description = f"Reality checks and insights about {category.name.lower()} careers in India. Salary expectations, trade-offs, and growth risks."
    articles = list(
        Article.objects.filter(category=category, status='published')
        .select_related('author')
        .order_by('-published_at')
    )
    article_count = len(articles)
    related_categories = Category.objects.exclude(id=category.id).order_by('order', 'name')[:4]
    meta_robots = "index, follow" if article_count >= INDEXABLE_CATEGORY_MIN_ARTICLES else "noindex, follow"

    return render(request, 'content/category_detail.html', {
        'category': category,
        'articles': articles,
        'article_count': article_count,
        'category_profile': build_category_profile(category, article_count),
        'related_categories': related_categories,
        'meta_robots': meta_robots,
        'og_title': og_title,
        'og_description': og_description,
        'twitter_title': og_title,
        'twitter_description': og_description,
    })

def article_og_image(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')

    def wrap_text(text, max_chars=34, max_lines=3):
        words = text.split()
        lines = []
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
            if len(lines) == max_lines:
                break
        if len(lines) < max_lines and current:
            lines.append(current)
        if len(lines) > max_lines:
            lines = lines[:max_lines]
        if len(lines) == max_lines and words and " ".join(lines) != text:
            lines[-1] = (lines[-1][: max_chars - 3] + "...") if len(lines[-1]) > 3 else "..."
        return lines

    title_lines = wrap_text(article.title)
    category = escape(article.category.name)

    y_start = 210
    line_height = 64
    title_svg = "\n".join(
        f'<text x="140" y="{y_start + i * line_height}" fill="#ffffff" '
        f'font-family="Inter, Segoe UI, Arial, sans-serif" font-size="54" '
        f'font-weight="700" letter-spacing="-0.5">{escape(line)}</text>'
        for i, line in enumerate(title_lines)
    )

    svg = f"""<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Career Reality article preview">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0d0d0d"/>
      <stop offset="100%" stop-color="#1c1c1c"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#d93025"/>
      <stop offset="100%" stop-color="#ff6f61"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect x="88" y="88" width="10" height="454" fill="url(#accent)"/>
  {title_svg}
  <text x="140" y="470" fill="#d8d8d8" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="30" font-weight="500">
    {category}
  </text>
  <rect x="140" y="505" width="430" height="56" rx="8" fill="#111111" stroke="#3a3a3a"/>
  <text x="164" y="542" fill="#ffffff" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="24" font-weight="600">
    careerreality.in
  </text>
</svg>"""

    response = HttpResponse(svg, content_type="image/svg+xml")
    response["Cache-Control"] = "public, max-age=86400"
    return response
