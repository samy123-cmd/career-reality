"""
SEO metadata for high-traffic landing pages.

Centralizes title/description/keyword targets so templates and views stay aligned.
Tune these when Search Console query data shifts.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PageSEO:
    title: str
    description: str
    h1: str | None = None
    keywords: tuple[str, ...] = ()


# ── Tool pages (traffic engine — target high-volume Indian career queries) ──

CTC_CALCULATOR = PageSEO(
    title="CTC Calculator India 2026 — CTC to In-Hand Salary (Free)",
    description=(
        "Free CTC calculator and CTC salary calculator for India. Calculate CTC to "
        "in-hand salary instantly with PF, gratuity, variable pay, and new vs old tax "
        "regime deductions."
    ),
    h1="CTC Calculator India — CTC to In-Hand Salary",
    keywords=(
        "ctc to in hand salary calculator india",
        "in hand salary calculator",
        "ctc decoder",
        "salary calculator india 2026",
    ),
)

RESIGNATION_ANALYZER = PageSEO(
    title="Resignation Risk Analyzer India — Notice Period & Bond Calculator (Free)",
    description=(
        "Free resignation risk calculator for Indian employees. Assess notice period "
        "pressure, service bonds, and HR escalation risk before you put in papers."
    ),
    h1="Resignation Risk Analyzer",
    keywords=(
        "resignation notice period india",
        "resignation risk calculator",
        "service bond india",
        "relieving letter india",
    ),
)

LAYOFF_RADAR = PageSEO(
    title="IT Layoffs India 2026 Tracker — Hiring Freeze & Layoff Alerts",
    description=(
        "Live crowdsourced layoff and hiring freeze tracker for Indian IT and tech "
        "companies. Check company stability signals and report anonymously."
    ),
    h1="Indian Tech Layoff Radar",
    keywords=(
        "it layoffs india 2026",
        "hiring freeze india",
        "tech layoff tracker india",
        "infosys layoff",
        "tcs layoff news",
    ),
)

SALARY_REALITY = PageSEO(
    title="Software Engineer Salary India 2026 — Median Pay by Role & City",
    description=(
        "Median software engineer, data, and product salaries in India — not inflated "
        "outliers. Role-wise pay bands for Bengaluru, Hyderabad, Pune, and remote."
    ),
    h1="Indian Tech Salary Reality",
    keywords=(
        "software engineer salary india 2026",
        "median salary india",
        "developer salary bangalore",
        "data engineer salary india",
    ),
)

HOME = PageSEO(
    title="Career Reality India — Salary Truths, CTC Calculator & Layoff Tracker",
    description=(
        "Salary truths and career reality checks for Indian tech professionals. "
        "Free CTC calculator, layoff radar, resignation risk tool, and honest analysis."
    ),
    keywords=(
        "career reality india",
        "salary reality check india",
        "indian tech career advice",
        "ctc calculator india",
    ),
)

# Internal linking hub — shown on articles and data pages.
# icon: CSS mark key (not emoji) — see .hp-tool-mark--* in tool-hub.css
SEO_TOOL_HUB = (
    {
        "label": "CTC to In-Hand Calculator",
        "description": "Decode your offer letter into real monthly take-home.",
        "url_name": "salary_calculator",
        "icon": "ctc",
    },
    {
        "label": "Resignation Risk Analyzer",
        "description": "Notice period, bonds, and HR pressure — before you resign.",
        "url_name": "analyzer_home",
        "icon": "risk",
    },
    {
        "label": "IT Layoff Radar",
        "description": "Hiring freeze and layoff signals across Indian tech.",
        "url_name": "layoff_radar",
        "icon": "radar",
    },
    {
        "label": "Salary Reality Data",
        "description": "Median pay by role — not unicorn outliers.",
        "url_name": "salary_reality",
        "icon": "salary",
    },
)

# Pillar articles to cross-link from tool pages (high intent ↔ content loop).
# Includes several URLs Google has crawled but not indexed so internal PageRank
# concentrates on the canonical article set we want in the index.
SEO_PILLAR_ARTICLES = (
    {
        "label": "Layoff Recovery Timeline India",
        "url_name": "article_detail",
        "slug": "layoff-recovery-timeline-india",
    },
    {
        "label": "What 20 LPA Actually Feels Like",
        "url_name": "article_detail",
        "slug": "what-20-lpa-actually-feels-like-india-purchasing-power",
    },
    {
        "label": "Manager vs IC: Which Path Pays",
        "url_name": "article_detail",
        "slug": "manager-vs-ic-career-path-india",
    },
    {
        "label": "Work-Life Balance Myth for High Performers",
        "url_name": "article_detail",
        "slug": "work-life-balance-myth-high-performers",
    },
    {
        "label": "DevOps / SRE On-Call Reality",
        "url_name": "article_detail",
        "slug": "devops-sre-reality-india-oncall",
    },
    {
        "label": "Why Upskilling Stops Working",
        "url_name": "article_detail",
        "slug": "why-upskilling-stops-working-career-trap",
    },
    {
        "label": "MBA Reality India 2026",
        "url_name": "article_detail",
        "slug": "mba-reality-india-worth-it-2026",
    },
    {
        "label": "Networking Reality for Introverts",
        "url_name": "article_detail",
        "slug": "networking-reality-india-introverts",
    },
    {
        "label": "Relieving Letter & Notice Period Traps",
        "url_name": "article_detail",
        "slug": "relieving-letter-hostage-notice-period-india-2026",
    },
    {
        "label": "Cybersecurity & Privacy Beyond Tech",
        "url_name": "article_detail",
        "slug": "cybersecurity-privacy-careers-beyond-tech-india-2026",
    },
    {
        "label": "Green Careers: ESG & Renewables",
        "url_name": "article_detail",
        "slug": "green-careers-esg-renewable-sustainability-india-2026",
    },
    {
        "label": "Portfolio-First Hiring & Gig Careers",
        "url_name": "article_detail",
        "slug": "portfolio-first-hiring-gig-economy-careers-india-2026",
    },
)
