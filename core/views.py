from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.urls import reverse
from content.models import Article, Category
from django.utils import timezone
from django.conf import settings


def _topic_clusters():
    return [
        {
            "name": "Salary Reality Cluster",
            "description": "Compensation truth, in-hand math, and negotiation leverage.",
            "pillar_url_name": "salary_reality",
            "supporting_urls": [
                {"label": "CTC Decoder", "url_name": "salary_calculator"},
                {"label": "Salary Drop", "url_name": "submit_salary"},
            ],
        },
        {
            "name": "Career Risk Cluster",
            "description": "Stagnation, switching risk, and timing decisions under uncertainty.",
            "pillar_url_name": "analyzer_home",
            "supporting_urls": [
                {"label": "Resignation Risk Analyzer", "url_name": "wizard_start"},
                {"label": "Layoff Radar", "url_name": "layoff_radar"},
            ],
        },
        {
            "name": "Role Reality Cluster",
            "description": "Role-specific realities across engineering, product, design, data, and marketing.",
            "pillar_url_name": "home",
            "supporting_urls": [
                {"label": "Editorial Standards", "url_name": "editorial"},
                {"label": "Topic Clusters", "url_name": "topic_clusters"},
            ],
        },
        {
            "name": "AI Intelligence Cluster",
            "description": "AI model releases, career impact, and India-specific developments.",
            "pillar_url_name": "ai_news_hub",
            "supporting_urls": [],
        },
    ]


def _career_reality_index_rows():
    return [
        {"month": "February 2026", "salary_pressure": 72, "switch_difficulty": 68, "layoff_risk": 54, "overall": 65},
        {"month": "January 2026", "salary_pressure": 71, "switch_difficulty": 66, "layoff_risk": 56, "overall": 64},
        {"month": "December 2025", "salary_pressure": 69, "switch_difficulty": 63, "layoff_risk": 58, "overall": 63},
        {"month": "November 2025", "salary_pressure": 67, "switch_difficulty": 61, "layoff_risk": 57, "overall": 62},
    ]


def _index_band(score):
    if score >= 75:
        return "Severe Pressure"
    if score >= 65:
        return "High Pressure"
    if score >= 55:
        return "Elevated Pressure"
    if score >= 45:
        return "Moderate Pressure"
    return "Stable Window"

def robots_txt(request):
    """
    Serves the robots.txt file dynamically.
    """
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /resignation-risk/step/",
        "Disallow: /resignation-risk/result/",
        "Disallow: /salary-drop/",
        "Disallow: /salary-drop/success/",
        "Disallow: /layoff-radar/",
        "",
        f"Sitemap: {settings.CANONICAL_BASE_URL}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

@cache_page(60 * 15)
def home(request):
    """
    Home page view.
    - Shows mission statement.
    - Lists only PUBLISHED articles.
    """
    article_qs = Article.objects.filter(status='published').select_related('author', 'category').order_by('-published_at')
    articles = article_qs[:10]
    categories = Category.objects.all()
    recent_updates = article_qs.order_by('-updated_at')[:5]
    index_rows = _career_reality_index_rows()
    
    title = "Career Reality India - Salary Truths and Career Reality Checks"
    description = "Data-backed reality checks on Indian tech careers: salary stagnation, skill decay, and the real trade-offs you need to plan for."
    home_faq = [
        {
            "q": "What makes Career Reality different from generic career blogs?",
            "a": "We prioritize evidence-backed analysis, role-level trade-offs, and correction logs over motivational narratives."
        },
        {
            "q": "How often is content updated?",
            "a": "Core market pages are reviewed monthly, with additional updates when salary or hiring conditions shift materially."
        },
        {
            "q": "Does advertising influence editorial conclusions?",
            "a": "No. Editorial and commercial decisions are separated under published standards and sponsorship policy."
        },
    ]

    return render(request, 'core/home.html', {
        'articles': articles,
        'categories': categories,
        'recent_updates': recent_updates,
        'topic_clusters': _topic_clusters(),
        'latest_index_row': index_rows[0],
        'latest_band': _index_band(index_rows[0]['overall']),
        'home_faq': home_faq,
        **_seo(title, description),
    })

def _seo(title, description):
    return {
        'og_title': title,
        'og_description': description,
        'twitter_title': title,
        'twitter_description': description,
    }

@cache_page(60 * 60)
def about(request):
    title = "About Career Reality - India Career Truths"
    description = "Why Career Reality exists, who it serves, and how we cover Indian tech careers with independent, data-backed analysis."
    return render(request, 'core/about.html', _seo(title, description))

@cache_page(60 * 60)
def editorial_standards(request):
    title = "Editorial Standards - Career Reality India"
    description = "Editorial principles for Career Reality: accuracy over comfort, no sponsored influence, and transparent updates to reflect market shifts."
    return render(request, 'core/editorial.html', _seo(title, description))

@cache_page(60 * 15)
def salary_reality(request):
    title = "Salary Reality (India) - Career Reality"
    description = "Real, uninflated salary data for Indian tech roles with context and median ranges."
    return render(request, 'core/salary.html', _seo(title, description))

@cache_page(60 * 60)
def salary_calculator(request):
    """In-hand salary calculator for Indian professionals."""
    categories = Category.objects.all()
    title = "CTC Decoder: Calculate In-Hand Salary India (2026)"
    description = "Decode CTC into real in-hand salary with PF, gratuity, variable pay, and tax regime logic."
    context = {'categories': categories}
    context.update(_seo(title, description))
    return render(request, 'core/salary_calculator.html', context)

@cache_page(60 * 60)
def escape_plan(request):
    """
    The Service Company Escape Plan.
    Contains the "Rot Check" quiz and the roadmap.
    """
    return render(request, 'content/escape_plan.html')

def privacy_policy(request):
    title = "Privacy Policy - Career Reality India"
    description = "Privacy Policy for Career Reality India. Covers cookies, data collection, and ad network compliance."
    return render(request, 'core/privacy_policy.html', _seo(title, description))

def contact(request):
    title = "Contact Career Reality - Editorial Inquiries"
    description = "Contact Career Reality for editorial inquiries, corrections, or feedback on our India career analysis."
    return render(request, 'core/contact.html', _seo(title, description))

def terms(request):
    title = "Terms of Service - Career Reality India"
    description = "Terms of Service for Career Reality India. Read before using the site and its career content."
    return render(request, 'core/terms.html', _seo(title, description))


@cache_page(60 * 15)
def topic_clusters(request):
    title = "Topic Clusters - Career Reality India"
    description = "Explore Career Reality authority clusters: salary, career risk, and role-specific market realities."
    categories = Category.objects.all().order_by('order', 'name')
    return render(request, 'core/topic_clusters.html', {
        "categories": categories,
        "clusters": _topic_clusters(),
        **_seo(title, description),
    })


@cache_page(60 * 15)
def career_reality_index(request):
    title = "Career Reality Index (India) - Monthly Career Pressure Tracker"
    description = "Monthly index tracking salary pressure, switching difficulty, and layoff risk in Indian tech careers."
    rows = _career_reality_index_rows()
    latest = rows[0]
    previous = rows[1] if len(rows) > 1 else rows[0]
    delta_overall = latest["overall"] - previous["overall"]

    methodology_components = [
        {
            "name": "Salary Pressure",
            "weight": "40%",
            "what_it_uses": "Median compensation movement, offer compression by experience band, and fixed-vs-variable pay drift.",
            "why_it_matters": "Most career planning fails when people optimize for headline CTC and miss actual leverage quality."
        },
        {
            "name": "Switch Difficulty",
            "weight": "35%",
            "what_it_uses": "Interview loop depth, role competition ratio, and time-to-offer friction.",
            "why_it_matters": "A role can look attractive on paper but still be hard to enter due to cycle timing and market crowding."
        },
        {
            "name": "Layoff Risk",
            "weight": "25%",
            "what_it_uses": "Freeze/layoff signal density, report confidence, and persistence over recent weeks.",
            "why_it_matters": "Downside risk compounds quietly and affects negotiation power long before formal announcements."
        },
    ]

    interpretation_bands = [
        {"range": "75-100", "label": "Severe Pressure", "note": "Protect downside first. Avoid high-risk role jumps without contingency."},
        {"range": "65-74", "label": "High Pressure", "note": "Prioritize leverage upgrades and preserve optionality."},
        {"range": "55-64", "label": "Elevated Pressure", "note": "Selective opportunities exist, but decision quality matters more."},
        {"range": "45-54", "label": "Moderate Pressure", "note": "Balanced window for planned moves with clear rationale."},
        {"range": "0-44", "label": "Stable Window", "note": "Lower friction environment, still validate role quality."},
    ]

    how_to_use = [
        {
            "persona": "Early Career (0-3 years)",
            "guidance": "Use the index to choose skill depth over title optics. In high-pressure months, avoid shallow switches that only rename your role."
        },
        {
            "persona": "Mid Career (4-10 years)",
            "guidance": "Treat index moves as leverage signals. If pressure rises, tighten negotiation evidence and reassess switching timelines."
        },
        {
            "persona": "Senior/Leadership (10+ years)",
            "guidance": "Monitor downside asymmetry. High pressure means org-risk and team-stability checks should be explicit before transitions."
        },
    ]

    faq_items = [
        {
            "q": "Is the index predictive?",
            "a": "No. It is directional and designed for decision hygiene, not certainty."
        },
        {
            "q": "How often is it refreshed?",
            "a": "Monthly baseline updates, plus ad-hoc revisions during major market shocks."
        },
        {
            "q": "Can one metric override the overall score?",
            "a": "Yes. In individual cases, a sharp move in one component can matter more than the aggregate."
        },
    ]

    change_log = [
        {"date": "March 8, 2026", "note": "March 2026 scores published. Salary pressure ticks up on appraisal-cycle compression; layoff risk eases slightly as Q1 hiring stabilises."},
        {"date": "February 17, 2026", "note": "Expanded methodology transparency, interpretation bands, and persona-specific playbooks."},
        {"date": "February 1, 2026", "note": "Refreshed monthly scores and revised layoff signal weighting checks."},
        {"date": "January 2, 2026", "note": "Added switch difficulty component to reduce headline-bias decisions."},
    ]

    return render(request, 'core/career_reality_index.html', {
        "index_rows": rows,
        "latest_row": latest,
        "latest_band": _index_band(latest["overall"]),
        "delta_overall": delta_overall,
        "methodology_components": methodology_components,
        "interpretation_bands": interpretation_bands,
        "how_to_use": how_to_use,
        "faq_items": faq_items,
        "change_log": change_log,
        "published_on": timezone.localdate(),
        **_seo(title, description),
    })


def revenue_model(request):
    title = "Revenue Model - Career Reality India"
    description = "How Career Reality earns revenue while protecting editorial independence and quality."
    return render(request, 'core/revenue_model.html', {
        **_seo(title, description),
        'meta_robots': 'noindex, follow',
    })


def sponsorship_policy(request):
    title = "Sponsorship Policy - Career Reality India"
    description = "Rules for sponsorships and commercial partnerships at Career Reality with strict editorial separation."
    return render(request, 'core/sponsorship_policy.html', {
        **_seo(title, description),
        'meta_robots': 'noindex, follow',
    })

def newsletter_signup(request):
    """Handle newsletter signup form submission."""
    if request.method != 'POST':
        return redirect(request.META.get('HTTP_REFERER') or reverse('home'))

    # Basic rate-limit: max 3 signups per IP per hour via cache counter.
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
    rate_key = f"newsletter_signup_ip_{ip}"
    from django.core.cache import cache
    count = cache.get(rate_key, 0)
    if count >= 3:
        messages.error(request, 'Too many requests. Please try again later.')
        return redirect(request.META.get('HTTP_REFERER') or reverse('home'))
    cache.set(rate_key, count + 1, timeout=3600)

    email = request.POST.get('email', '').strip()
    if email:
        from core.models import NewsletterSubscriber
        try:
            NewsletterSubscriber.objects.get_or_create(email=email)
            messages.success(request, 'Thanks for subscribing! You\'ll get our weekly reality checks.')
        except Exception as exc:
            import logging
            logging.getLogger(__name__).exception("Newsletter signup failed for %s: %s", email, exc)
            messages.info(request, 'Thanks for your interest!')
    else:
        messages.error(request, 'Please enter a valid email address.')

    return redirect(request.META.get('HTTP_REFERER') or reverse('home'))


def custom_404(request, exception):
    """Branded 404 — keeps users in the funnel with helpful navigation links."""
    return render(request, '404.html', {'meta_robots': 'noindex, follow'}, status=404)


def custom_500(request):
    """Minimal 500 — self-contained HTML to avoid cascade template failures."""
    return render(request, '500.html', status=500)
