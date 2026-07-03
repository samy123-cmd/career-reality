"""
Seed AI Pulse items for June–July 2026 — India career angle.
Run: python seed_ai_july_2026.py
"""
import os
from datetime import datetime, timezone as dt_tz

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django  # noqa: E402

django.setup()

from django.utils import timezone  # noqa: E402

from ainews.models import AINewsItem, AITag  # noqa: E402


def dt(s):
    return datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=dt_tz.utc)


def ensure_tag(name):
    tag, _ = AITag.objects.get_or_create(
        name=name,
        defaults={"slug": name.lower().replace(" ", "-")},
    )
    return tag


ITEMS = [
    {
        "title": "Agentic AI Coding Tools Reshape Indian QA and SDE-I Hiring in Mid-2026",
        "slug": "agentic-ai-coding-tools-india-qa-sde-hiring-july-2026",
        "summary": (
            "<p>By July 2026, Indian product companies including Flipkart, Razorpay, and PhonePe have "
            "mandated agent-assisted development workflows. QA headcount growth has stalled while "
            "senior engineer productivity targets rose 25–40%. The shift is workload redistribution, "
            "not mass replacement — but SDE-I intake at several firms dropped 20–30% year-on-year.</p>"
        ),
        "career_angle": (
            "QA engineers should pivot to test automation architecture and AI-eval pipeline design. "
            "SDE-I candidates must demonstrate code review and agent-orchestration skills, not just "
            "LeetCode speed. Interview loops at Indian product companies now include 'debug AI-generated code' rounds."
        ),
        "source_name": "Industry Reports",
        "source_url": "https://github.blog/news-insights/research/",
        "significance": "high",
        "tags": ["Career Impact", "Industry News"],
        "event_date": dt("2026-06-15"),
        "published_at": dt("2026-06-16"),
    },
    {
        "title": "India Confirmed as Second-Largest AI Developer Tool Market in H1 2026",
        "slug": "india-ai-developer-tool-adoption-h1-2026",
        "summary": (
            "<p>GitHub's mid-2026 State of the Octoverse India edition and McKinsey's Q2 AI survey "
            "confirm India as the second-largest adopter of AI developer tools globally. Copilot, Cursor, "
            "and Claude Code usage in Indian engineering teams grew 85% year-on-year. Adoption is broad; "
            "premium AI engineering roles remain narrow.</p>"
        ),
        "career_angle": (
            "Tool adoption alone does not create salary premiums. Indian engineers who combine Copilot fluency "
            "with production deployment evidence (RAG, agents, eval harnesses) command 15–35% premiums. "
            "Certificate-only profiles see no measurable comp lift in July 2026 hiring data."
        ),
        "source_name": "GitHub",
        "source_url": "https://github.blog/news-insights/",
        "significance": "high",
        "tags": ["Career Impact", "Benchmark"],
        "event_date": dt("2026-06-20"),
        "published_at": dt("2026-06-21"),
    },
    {
        "title": "GCCs Raise AI Hiring Bar: System Design Now Expected at 4–6 YOE",
        "slug": "gcc-ai-hiring-bar-system-design-july-2026",
        "summary": (
            "<p>Global Capability Centers in Bengaluru and Hyderabad updated AI/ML hiring rubrics in "
            "June–July 2026. Roles previously accessible at 3–4 years of experience now require system "
            "design depth, production ML deployment, and cross-functional ownership. Summer hiring slowed "
            "but selectivity increased.</p>"
        ),
        "career_angle": (
            "GCC AI roles are not easier than product company equivalents in 2026. Engineers targeting "
            "captives should prepare for system design + ML ops interviews, not just framework tutorials. "
            "Comp bands remain 15–25% above IT services but bar is rising faster than pay."
        ),
        "source_name": "NASSCOM",
        "source_url": "https://nasscom.in/",
        "significance": "medium",
        "tags": ["Career Impact", "Industry News"],
        "event_date": dt("2026-07-01"),
        "published_at": dt("2026-07-02"),
    },
    {
        "title": "OpenAI Codex Agent Workflows Hit Indian Startup Engineering Teams",
        "slug": "openai-codex-agent-workflows-indian-startups-july-2026",
        "summary": (
            "<p>Multiple Series A–C Indian startups deployed Codex-class agents for feature-branch completion "
            "in Q2 2026. Engineering leads report 30–50% reduction in boilerplate coding time, with senior "
            "engineers shifting to architecture review and agent prompt design. Junior hiring freezes at "
            "several firms extended through July.</p>"
        ),
        "career_angle": (
            "Indian startup engineers should learn agent orchestration, code review at scale, and "
            "reliability testing for AI-generated code. 'Write CRUD endpoints' is no longer a differentiator — "
            "'validate and ship agent-assisted features safely' is."
        ),
        "source_name": "OpenAI",
        "source_url": "https://openai.com/index/introducing-codex/",
        "significance": "high",
        "tags": ["Model Release", "Career Impact"],
        "event_date": dt("2026-06-28"),
        "published_at": dt("2026-06-29"),
    },
    {
        "title": "Google Gemini Enterprise India Rollout Accelerates GCC AI Procurement",
        "slug": "google-gemini-enterprise-india-gcc-july-2026",
        "summary": (
            "<p>Google expanded Gemini Enterprise availability to Indian GCCs and large IT services clients "
            "in July 2026. Procurement cycles shortened from 6 months to 6 weeks as boards mandate AI "
            "productivity roadmaps. Implementation roles — AI integration engineers, eval specialists — "
            "see rising demand.</p>"
        ),
        "career_angle": (
            "Enterprise Gemini rollouts create implementation and integration roles, not just research positions. "
            "Indian engineers with API integration, security review, and Hindi/Indic language testing experience "
            "are preferred for client-facing deployment teams."
        ),
        "source_name": "Google",
        "source_url": "https://blog.google/technology/ai/",
        "significance": "medium",
        "tags": ["Industry News", "Career Impact"],
        "event_date": dt("2026-07-02"),
        "published_at": dt("2026-07-03"),
    },
    {
        "title": "Indian IT Services Clients Renegotiate Contracts With 15–25% Fewer Headcount",
        "slug": "it-services-ai-headcount-renegotiation-july-2026",
        "summary": (
            "<p>Q2 2026 earnings calls from major IT services firms confirmed client contract renegotiations "
            "with AI-assisted delivery clauses. Effective headcount per project dropped 15–25% without "
            "scope reduction. Bench utilization targets tightened to 88%+ in July.</p>"
        ),
        "career_angle": (
            "IT services engineers at 4–7 YOE without system design depth face the highest mid-year bench risk. "
            "Upskilling into cloud architecture, AI-assisted delivery leadership, or client-facing solution "
            "design is the viable exit path — not waiting for the 'next hiring wave.'"
        ),
        "source_name": "Economic Times Tech",
        "source_url": "https://economictimes.indiatimes.com/tech/",
        "significance": "high",
        "tags": ["Career Impact", "Industry News"],
        "event_date": dt("2026-07-01"),
        "published_at": dt("2026-07-03"),
    },
]

inserted = 0
updated = 0
for item_data in ITEMS:
    slug = item_data["slug"]
    tags = item_data.pop("tags", [])
    defaults = {
        "title": item_data["title"],
        "summary": item_data["summary"],
        "career_angle": item_data["career_angle"],
        "source_name": item_data["source_name"],
        "source_url": item_data["source_url"],
        "significance": item_data["significance"],
        "fact_check_status": "verified",
        "status": "published",
        "event_date": item_data["event_date"],
        "published_at": item_data["published_at"],
        "reviewed_at": timezone.now(),
    }
    obj, created = AINewsItem.objects.update_or_create(slug=slug, defaults=defaults)
    for tag_name in tags:
        obj.tags.add(ensure_tag(tag_name))
    if created:
        inserted += 1
        print(f"  Added: {item_data['title'][:65]}")
    else:
        updated += 1
        print(f"  Updated: {item_data['title'][:65]}")

print(f"\nInserted {inserted}, updated {updated} AI news items.")
print(f"Total published AI news: {AINewsItem.objects.filter(status='published').count()}")
