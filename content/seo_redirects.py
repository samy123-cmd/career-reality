"""
Central SEO configuration for article canonicalization and sitemap hygiene.

Duplicate topic clusters compete for the same search intent. Loser slugs 301 to
the canonical winner and are excluded from the sitemap so Google consolidates signals.
"""

from django.db.models import Count, Q

# Minimum published articles before a category page is indexable (matches category_detail).
MIN_INDEXABLE_CATEGORY_ARTICLES = 3

# Loser slug -> canonical slug (permanent 301).
ARTICLE_CANONICAL_REDIRECTS = {
    # Junior Data Scientist — keep the shorter, homepage-featured slug (Apr 2026).
    "junior-data-scientist-reality-india-sql-janitor": "junior-data-scientist-reality-india",
    # Digital Marketing — keep the deeper agency-vs-B2B analysis.
    "digital-marketing-illusion-instagram-ads-burning-money": "digital-marketing-reality-agency-burnout",
    "digital-marketing-reality-india": "digital-marketing-reality-agency-burnout",
    # Networking — keep the introvert-focused, natural-title article.
    "networking-myth-professional-relationships-worthless": "networking-reality-india-introverts",
    # Product Management — keep the Jira-janitor deep dive (stronger E-E-A-T signals).
    "the-product-manager-reality-coordinator-not-ceo": "product-manager-reality-india-jira-janitor",
    # UX / Design — keep the strategy-focused long-form piece.
    "the-ux-design-reality-india-ui-factory": "the-design-reality-beautiful-screens-do-not-save-bad-strategy",
    # Upskilling — keep the career-trap narrative (featured in topic clusters).
    "the-learning-reality-upskilling-is-not-a-guarantee": "why-upskilling-stops-working-career-trap",
}

ARTICLE_SITEMAP_EXCLUDE_SLUGS = frozenset(ARTICLE_CANONICAL_REDIRECTS.keys())


def published_article_q() -> Q:
    """Published articles that are not redirect losers."""
    return Q(status="published") & ~Q(slug__in=ARTICLE_SITEMAP_EXCLUDE_SLUGS)


def category_published_article_filter() -> Q:
    """Category annotation filter — excludes redirect loser articles from counts."""
    return Q(article__status="published") & ~Q(article__slug__in=ARTICLE_SITEMAP_EXCLUDE_SLUGS)


def indexable_categories_queryset():
    """Categories with enough canonical published articles to be indexable."""
    from content.models import Category

    return (
        Category.objects.annotate(
            pub_count=Count("article", filter=category_published_article_filter())
        )
        .filter(pub_count__gte=MIN_INDEXABLE_CATEGORY_ARTICLES)
        .order_by("order", "name")
    )
