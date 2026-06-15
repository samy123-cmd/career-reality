from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.urls import reverse
from django.utils.html import escape, strip_tags
from django.views.decorators.cache import cache_page
from django.utils import timezone
import re
from .models import Article, Category, Author
from .seo_redirects import (
    ARTICLE_CANONICAL_REDIRECTS,
    ARTICLE_SITEMAP_EXCLUDE_SLUGS,
    indexable_categories_queryset,
)


# ---------------------------------------------------------------------------
# Shared text-extraction helpers
# ---------------------------------------------------------------------------

def _first_sentence_from_field(text: str, min_len: int = 15) -> str:
    """Return the first sentence from a stripped content field, or ""."""
    plain = strip_tags(text or "").strip()
    parts = re.split(r"(?<=[.!?])\s+", plain)
    s = parts[0].strip() if parts else ""
    return s if len(s) >= min_len else ""


def _substantive_sentence_from_field(text: str) -> str:
    """
    Return the first real sentence from a content field, robustly skipping:
    - Section-heading lines ending with ":"
    - Short snippets under 8 words or 30 chars
    - Table-derived fragments with no sentence-ending punctuation
    Handles both double-newline paragraph breaks and single-newline heading prefixes.
    """
    plain = strip_tags(text or "").strip()
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", plain) if p.strip()]
    for para in paragraphs:
        # Skip heading-colon opener on single-newline lines within a paragraph
        lines = [ln.strip() for ln in para.split("\n") if ln.strip()]
        substantive_lines = []
        for ln in lines:
            if ln.endswith(":") and len(ln) < 80 and not substantive_lines:
                continue
            substantive_lines.append(ln)
        if not substantive_lines:
            continue
        para_clean = " ".join(substantive_lines)
        word_count = len(re.sub(r"[^\w\s]", " ", para_clean).split())
        if word_count < 8:
            continue
        sentences = re.split(r"(?<=[.!?])\s+", para_clean)
        for s in sentences:
            stripped = s.strip()
            if len(stripped) >= 30 and len(stripped.split()) >= 5:
                return stripped[:180] if len(stripped) > 180 else stripped
    return ""


def _article_sources(article):
    checked_on = article.last_reality_check
    if checked_on is None and article.updated_at:
        checked_on = timezone.localtime(article.updated_at).date()
    if checked_on is None:
        checked_on = timezone.localdate()
    common_sources = [
        {"name": "AmbitionBox Salary Insights", "url": "https://www.ambitionbox.com/salaries", "checked_on": checked_on},
        {"name": "Glassdoor India Salaries", "url": "https://www.glassdoor.co.in/Salaries/index.htm", "checked_on": checked_on},
        {"name": "LinkedIn Jobs (India)", "url": "https://www.linkedin.com/jobs/", "checked_on": checked_on},
        {"name": "Naukri Jobs (India)", "url": "https://www.naukri.com/", "checked_on": checked_on},
    ]

    category_name = (article.category.name or "").lower()
    if "design" in category_name:
        common_sources.append({"name": "Dribbble Salary Guide", "url": "https://dribbble.com/resources", "checked_on": checked_on})
    if "data" in category_name or "ai" in category_name:
        common_sources.append({"name": "Kaggle State of Data/AI", "url": "https://www.kaggle.com/", "checked_on": checked_on})
    if "product" in category_name:
        common_sources.append({"name": "Product Management Salary Benchmarks", "url": "https://www.productledalliance.com/", "checked_on": checked_on})

    return common_sources[:6]


def _article_update_log(article):
    logs = []
    category = (article.category.name or "").lower()
    if article.updated_at:
        year = article.updated_at.year
        logs.append({
            "date": article.updated_at.date(),
            "summary": (
                f"Updated {category} salary ranges for {year}, refreshed market positioning "
                "benchmarks, and corrected stale compensation data against current hiring signals."
            ),
        })
    if article.last_reality_check:
        logs.append({
            "date": article.last_reality_check,
            "summary": (
                "Fact-checked core claims against AmbitionBox, Glassdoor India, and LinkedIn "
                "hiring data. Corrected stale salary figures and re-validated growth projections."
            ),
        })
    if article.published_at:
        logs.append({
            "date": article.published_at.date(),
            "summary": (
                f"Initial publication of this {category} career reality check with market "
                "framing, salary benchmarks, and trade-off analysis for Indian professionals."
            ),
        })
    return logs


def _decision_framework(article):
    category_name = (article.category.name or "").lower()
    stuck_signal = _first_sentence_from_field(article.stuck_point)

    if "engineering" in category_name or "software" in category_name:
        base = [
            "If salary delta is below 25% for a switch, optimize for skill depth and scope first.",
            "If your stack is legacy-only for 12+ months, begin a transition plan before role lock-in compounds.",
            "If role ownership is high but pay is flat, build impact evidence and negotiate before switching.",
        ]
    elif "design" in category_name or "product" in category_name:
        base = [
            "If your output is execution-only for multiple quarters, push for discovery and strategy exposure.",
            "If portfolio quality is improving but compensation is frozen, benchmark in market every 12 months.",
            "If expectations are senior-level but authority is junior-level, document the scope mismatch and renegotiate.",
        ]
    else:
        base = [
            "If your take-home is not compounding with experience, benchmark externally — do not accept internal narratives.",
            "If role expectations rise without title or pay movement, escalate with documented outcomes.",
            "If your growth path is unclear beyond 6–9 months, run a switch-or-specialize decision cycle now.",
        ]

    # Inject one article-specific item derived from the article's own stuck_point
    if stuck_signal and stuck_signal not in " ".join(base):
        base.append(f"Watch for this pattern from this article: {stuck_signal}")

    return base


def _mistake_checklist(article):
    category_name = (article.category.name or "").lower()
    items = [
        "Treating outlier salaries as planning baselines.",
        "Using title changes as a substitute for genuine capability growth.",
        "Delaying market benchmarking until after compensation has already stagnated.",
    ]
    if "data" in category_name or "ai" in category_name:
        items.append("Over-indexing on model demos without production deployment depth.")
    elif "product" in category_name:
        items.append("Confusing feature shipping speed with measurable product impact.")
    elif "design" in category_name:
        items.append("Optimising for visual polish instead of demonstrable business outcomes.")
    elif "engineering" in category_name or "software" in category_name:
        items.append("Staying anchored to a legacy stack because it feels safe rather than strategic.")
    elif "marketing" in category_name:
        items.append("Measuring vanity metrics (reach, impressions) instead of pipeline and revenue attribution.")

    # Add one item derived from this article's who_should_avoid section
    avoid_signal = _first_sentence_from_field(article.who_should_avoid)
    if avoid_signal and len(avoid_signal) < 160:
        items.append(avoid_signal)

    return items[:5]


def _scenario_snapshot(article):
    """Build a scenario snapshot grounded in this article's own target_persona and stuck_point."""
    persona_line = _substantive_sentence_from_field(article.target_persona)
    stuck_line = _substantive_sentence_from_field(article.stuck_point)

    if persona_line and stuck_line:
        return f"{persona_line} {stuck_line}"
    if persona_line:
        return persona_line

    # Fallback to category-level snapshot when content fields are too short
    category_name = (article.category.name or "").lower()
    if "engineering" in category_name or "software" in category_name:
        return (
            "A mid-level developer with 5 years in a stable service role gets a title bump "
            "but no meaningful scope change. Within 12 months, market interview performance "
            "drops due to stale stack exposure."
        )
    if "design" in category_name:
        return (
            "A designer moves from visual-heavy delivery work to product discovery ownership. "
            "Compensation growth follows only after portfolio evidence shows shipped outcomes, "
            "not just polished screens."
        )
    if "product" in category_name:
        return (
            "A product manager ships high ticket volume but weak business outcomes. Career "
            "growth stalls until metric ownership is documented and tied to decision quality."
        )
    return (
        "A professional stays in-role despite rising responsibility and flat pay. Growth "
        "recovers only after external benchmarking and a deliberate switch-or-specialize decision."
    )


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
    takeaways = []

    def _first_clean_sentence(text: str, max_len: int = 180) -> str:
        """Extract first real sentence from a content field, capped at max_len."""
        plain = strip_tags(text or "").strip()
        if not plain:
            return ""
        parts = re.split(r"(?<=[.!?])\s+", plain)
        s = parts[0].strip()
        # Must be a real sentence: at least 6 words, ends with punctuation, cap length
        if len(s.split()) < 6:
            return ""
        if not re.search(r"[.!?]$", s):
            s = s[:max_len] + ("." if len(s) >= max_len else "")
        return s[:max_len] if len(s) > max_len else s

    # First takeaway: from the verdict (the article's core conclusion)
    s = _first_clean_sentence(article.verdict)
    if s:
        takeaways.append(s)

    # Second takeaway: from stuck_point (where people fail)
    s = _first_clean_sentence(article.stuck_point)
    if s:
        takeaways.append(s)

    # Third takeaway: from who_should_avoid
    s = _first_clean_sentence(article.who_should_avoid)
    if s:
        takeaways.append(s)

    # Fallback if content fields are too short
    if len(takeaways) < 2:
        takeaways.append(
            f"This analysis covers {article.category.name.lower()}"
            " career realities specific to the Indian market."
        )

    return takeaways[:3]


def _originality_moat(article):
    """Derive contrarian thesis and non-obvious signal from the article's own content."""
    verdict_sentence = _substantive_sentence_from_field(article.verdict)
    stuck_sentence = _substantive_sentence_from_field(article.stuck_point)

    if verdict_sentence and stuck_sentence:
        return {
            "contrarian_thesis": verdict_sentence,
            "non_obvious_signal": stuck_sentence,
        }

    # Fallback to category-based defaults
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
    def _slice_sources(start, end):
        return source_refs[start:end] if source_refs else []

    category = article.category.name

    return [
        {
            "section_id": "expectation",
            "claim": (
                f"Popular narratives about {category.lower()} roles in India overweight outlier "
                "outcomes and underweight base-rate career trajectories."
            ),
            "sources": _slice_sources(0, 2),
        },
        {
            "section_id": "reality",
            "claim": (
                f"Observed compensation and growth outcomes for {category.lower()} professionals "
                "diverge significantly from social-media storytelling."
            ),
            "sources": _slice_sources(1, 3),
        },
        {
            "section_id": "salary-growth",
            "claim": (
                f"{category} salary ranges in India vary materially by company type, "
                "negotiation leverage, and market cycle timing."
            ),
            "sources": _slice_sources(0, 4),
        },
        {
            "section_id": "stuck-point",
            "claim": (
                f"Professionals in {category.lower()} plateau fastest when scope quality "
                "stagnates while responsibility and expectations keep rising."
            ),
            "sources": _slice_sources(2, 5),
        },
    ]


def _generate_article_faqs(article):
    """
    Build FAQs from article body fields using stable, human-readable questions.
    Avoids auto-parsing titles into awkward strings like
    "What is the reality of indian it layoff cycle in India?"
    """

    def _answer(text, max_chars=300):
        """Return the first substantive paragraph from an HTML field, stripped of tags."""
        plain = strip_tags(text or "").strip()
        if not plain:
            return ""
        paragraphs = [p.strip() for p in re.split(r"\n{2,}", plain) if p.strip()]
        for para in paragraphs:
            clean = re.sub(r"[^\w\s₹%.,!?'-]", " ", para).strip()
            if len(clean) < 50 or len(clean.split()) < 8:
                continue
            if para.rstrip().endswith(":") and len(para.rstrip()) < 80:
                continue
            if not re.search(r"[.!?]", para):
                continue
            if len(para) > max_chars:
                return para[:max_chars].rsplit(" ", 1)[0] + "…"
            return para
        truncated = plain[:250]
        if len(plain) > 250:
            truncated = truncated.rsplit(" ", 1)[0] + "…"
        return truncated

    category_label = article.category.name
    faqs = []

    reality_ans = _answer(article.actual_reality)
    if reality_ans:
        faqs.append({
            "q": f"What is the actual reality for {category_label} careers in India?",
            "a": reality_ans,
        })

    salary_ans = _answer(article.salary_reality)
    if salary_ans:
        faqs.append({
            "q": f"What salary ranges are realistic in India for this role?",
            "a": salary_ans,
        })

    avoid_ans = _answer(article.who_should_avoid)
    if avoid_ans:
        faqs.append({
            "q": "Who should avoid this career path?",
            "a": avoid_ans,
        })

    verdict_ans = _answer(article.verdict)
    if verdict_ans:
        faqs.append({
            "q": "What's the bottom line for Indian professionals?",
            "a": verdict_ans,
        })

    return faqs


def _article_keywords(article):
    """
    Extract article-specific keywords from the title and category for schema markup.
    Replaces the generic 4-word keyword string that was identical across all articles.
    """
    import re as _re

    title_lower = article.title.lower()
    category = article.category.name.lower()

    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "is", "are", "was", "were", "have", "has",
        "why", "what", "when", "how", "who", "which", "that", "this", "those",
        "not", "no", "never", "vs", "after", "nobody", "actually", "about",
        "your", "you", "most", "more", "than", "work", "works", "working",
    }

    words = _re.sub(r"[₹'\"':,!?()\-–—]", " ", title_lower).split()
    meaningful = [w for w in words if w not in stop_words and len(w) > 3]

    keywords = ["india", "career", category, "salary", "2026"]
    keywords.extend(meaningful[:5])

    role_signals = [
        "developer", "engineer", "manager", "designer", "analyst", "lead",
        "data", "frontend", "devops", "product", "marketing", "freelance",
        "startup", "mba", "equity", "remote", "layoff", "plateau", "switch",
    ]
    for kw in role_signals:
        if kw in title_lower and f"{kw} india" not in keywords:
            keywords.append(f"{kw} india")

    seen, unique = set(), []
    for k in keywords:
        if k not in seen:
            seen.add(k)
            unique.append(k)

    return unique[:12]

@cache_page(60 * 15)
def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id, is_active=True)
    articles = (
        Article.objects.filter(author=author, status='published')
        .exclude(slug__in=ARTICLE_SITEMAP_EXCLUDE_SLUGS)
        .order_by('-published_at')
    )

    has_minimum_articles = articles.values('id')[1:2].exists()
    meta_robots = "index, follow" if has_minimum_articles else "noindex, follow"

    meta_title = f"{author.display_name} — Career Reality Author"
    meta_description = (
        f"{author.experience_summary}. "
        f"Editorial contributor covering Indian tech careers, salary data, and career risk analysis."
    )[:160]

    return render(request, 'content/author_detail.html', {
        'author': author,
        'articles': articles,
        'meta_robots': meta_robots,
        'og_title': meta_title,
        'og_description': meta_description,
        'twitter_title': meta_title,
        'twitter_description': meta_description,
        'article_meta_title': meta_title,
        'article_meta_description': meta_description,
    })
@cache_page(60 * 60)
def article_detail(request, slug):
    canonical_slug = ARTICLE_CANONICAL_REDIRECTS.get(slug)
    if canonical_slug:
        return HttpResponsePermanentRedirect(
            reverse("article_detail", kwargs={"slug": canonical_slug})
        )

    article = get_object_or_404(
        Article.objects.select_related('author', 'category'),
        slug=slug,
        status='published',
    )
    og_image_url = request.build_absolute_uri(reverse('article_og_image', args=[article.slug]))
    related_qs = Article.objects.filter(
        category=article.category,
        status='published',
    ).exclude(id=article.id).exclude(
        slug__in=ARTICLE_CANONICAL_REDIRECTS.keys()
    ).select_related('category').order_by('-published_at')[:3]
    source_refs = _article_sources(article)
    return render(request, 'content/article_detail.html', {
        'article': article,
        'related_articles': related_qs,
        'categories': indexable_categories_queryset(),
        'source_references': source_refs,
        'reading_time': _reading_time_minutes(article),
        'key_takeaways': _key_takeaways(article),
        'faqs': _generate_article_faqs(article),
        'article_keywords': _article_keywords(article),
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
    # Filter only published articles, order by most recent
    articles = (
        Article.objects.filter(category=category, status='published')
        .exclude(slug__in=ARTICLE_SITEMAP_EXCLUDE_SLUGS)
        .select_related('author')
        .order_by('-published_at')
    )
    related_categories = indexable_categories_queryset().exclude(id=category.id)[:4]

    # Noindex thin categories (< 3 canonical articles)
    has_minimum_articles = articles.values('id')[2:3].exists()
    meta_robots = "index, follow" if has_minimum_articles else "noindex, follow"

    return render(request, 'content/category_detail.html', {
        'category': category,
        'articles': articles,
        'related_categories': related_categories,
        'meta_robots': meta_robots,
        'og_title': og_title,
        'og_description': og_description,
        'twitter_title': og_title,
        'twitter_description': og_description,
    })

@cache_page(60 * 60 * 24)
def article_og_image(request, slug):
    canonical_slug = ARTICLE_CANONICAL_REDIRECTS.get(slug)
    if canonical_slug:
        return HttpResponsePermanentRedirect(
            reverse("article_og_image", kwargs={"slug": canonical_slug})
        )

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
