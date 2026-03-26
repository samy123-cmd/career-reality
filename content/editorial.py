from collections import Counter
import re

from django.utils.html import strip_tags


SOURCE_LIBRARY = {
    "ambitionbox": {
        "name": "AmbitionBox Salary Insights",
        "url": "https://www.ambitionbox.com/salaries",
        "note": "Used to benchmark Indian salary bands across company types.",
        "sections": ("salary-growth", "reality"),
    },
    "glassdoor": {
        "name": "Glassdoor India Salaries",
        "url": "https://www.glassdoor.co.in/Salaries/index.htm",
        "note": "Cross-checks compensation ranges and role-level variance.",
        "sections": ("salary-growth", "reality"),
    },
    "linkedin_jobs": {
        "name": "LinkedIn Jobs India",
        "url": "https://www.linkedin.com/jobs/",
        "note": "Tracks hiring language, scope expectations, and current demand.",
        "sections": ("expectation", "reality", "stuck-point"),
    },
    "naukri_jobs": {
        "name": "Naukri Jobs",
        "url": "https://www.naukri.com/",
        "note": "Used to compare market demand across Indian employers and cities.",
        "sections": ("expectation", "reality", "stuck-point"),
    },
    "stack_overflow": {
        "name": "Stack Overflow Developer Survey",
        "url": "https://survey.stackoverflow.co/",
        "note": "Useful for skill-demand and tool-adoption baselines in engineering work.",
        "sections": ("reality", "stuck-point"),
    },
    "github_octoverse": {
        "name": "GitHub Octoverse",
        "url": "https://octoverse.github.com/",
        "note": "Adds context on ecosystem momentum and durable tooling trends.",
        "sections": ("reality", "stuck-point"),
    },
    "nasscom": {
        "name": "NASSCOM Insights",
        "url": "https://nasscom.in/knowledge-center",
        "note": "Adds India-specific services, outsourcing, and hiring-cycle context.",
        "sections": ("reality", "stuck-point"),
    },
    "kaggle": {
        "name": "Kaggle State of AI and ML",
        "url": "https://www.kaggle.com/",
        "note": "Helps separate analytics work from true ML or AI production depth.",
        "sections": ("expectation", "reality", "stuck-point"),
    },
    "aicte": {
        "name": "AICTE",
        "url": "https://www.aicte-india.org/",
        "note": "Used for program-level and institution-level education context.",
        "sections": ("expectation", "reality"),
    },
    "nirf": {
        "name": "NIRF Rankings",
        "url": "https://www.nirfindia.org/",
        "note": "Adds outcome context when education branding is part of the career bet.",
        "sections": ("expectation", "reality", "salary-growth"),
    },
    "uscis": {
        "name": "USCIS",
        "url": "https://www.uscis.gov/",
        "note": "Used for immigration-process and work-authorization context.",
        "sections": ("reality", "stuck-point"),
    },
    "travel_state": {
        "name": "U.S. Visa Bulletin",
        "url": "https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin.html",
        "note": "Adds wait-time and visa-friction context for US relocation paths.",
        "sections": ("reality", "stuck-point"),
    },
    "startup_india": {
        "name": "Startup India",
        "url": "https://www.startupindia.gov.in/",
        "note": "Adds company-formation and startup ecosystem context to equity bets.",
        "sections": ("expectation", "reality"),
    },
    "sebi": {
        "name": "SEBI",
        "url": "https://www.sebi.gov.in/",
        "note": "Adds regulatory context when equity, liquidity, or investor outcomes matter.",
        "sections": ("salary-growth", "reality"),
    },
    "rbi": {
        "name": "Reserve Bank of India",
        "url": "https://www.rbi.org.in/",
        "note": "Used for inflation, purchasing-power, and financial-condition context.",
        "sections": ("salary-growth", "reality"),
    },
}

CATEGORY_TOPIC_MAP = {
    "career-reality-checks": ("career",),
    "career-strategy": ("career",),
    "data-science": ("data",),
    "education": ("education",),
    "engineering": ("engineering",),
    "financial-reality": ("money",),
    "learning": ("career",),
    "marketing": ("marketing",),
    "money-reality": ("money",),
    "product-management": ("product",),
    "software-engineering": ("engineering",),
    "design": ("design",),
}

KEYWORD_TOPIC_MAP = {
    "react": ("engineering",),
    "frontend": ("engineering",),
    "backend": ("engineering",),
    "manager": ("management",),
    "management": ("management",),
    "equity": ("startup",),
    "esop": ("startup",),
    "startup": ("startup",),
    "remote": ("remote",),
    "american": ("immigration",),
    "visa": ("immigration",),
    "green card": ("immigration",),
    "mba": ("education",),
    "salary": ("money",),
    "lpa": ("money",),
    "purchasing": ("money",),
    "money": ("money",),
    "data": ("data",),
    "machine learning": ("data",),
    "ai": ("data",),
    "ux": ("design",),
    "design": ("design",),
    "product": ("product",),
    "marketing": ("marketing",),
    "service": ("services",),
    "it services": ("services",),
    "switch": ("career",),
    "side hustle": ("career", "money"),
}

TOPIC_SOURCE_KEYS = {
    "career": ("linkedin_jobs", "naukri_jobs"),
    "data": ("kaggle", "stack_overflow"),
    "design": ("linkedin_jobs", "glassdoor"),
    "education": ("aicte", "nirf"),
    "engineering": ("stack_overflow", "github_octoverse"),
    "immigration": ("uscis", "travel_state"),
    "management": ("linkedin_jobs", "glassdoor"),
    "marketing": ("linkedin_jobs", "naukri_jobs"),
    "money": ("rbi", "ambitionbox", "glassdoor"),
    "product": ("linkedin_jobs", "glassdoor"),
    "remote": ("linkedin_jobs", "naukri_jobs"),
    "services": ("nasscom", "linkedin_jobs"),
    "startup": ("startup_india", "sebi"),
}

TOPIC_SIGNAL_TEXT = {
    "career": "role scope, switching friction, and demand language",
    "data": "analytics-vs-ML role split, hiring demand, and compensation spread",
    "design": "portfolio expectations, discovery ownership, and pay compression",
    "education": "fee-to-outcome math, placement quality, and opportunity cost",
    "engineering": "stack demand, framework churn, and scope depth",
    "immigration": "visa timing, relocation friction, and compensation trade-offs",
    "management": "people-management scope, org leverage, and title inflation",
    "marketing": "agency-vs-brand trade-offs, execution load, and pay ceilings",
    "money": "take-home math, inflation pressure, and leverage quality",
    "product": "metric ownership, stakeholder load, and compensation variance",
    "remote": "timezone costs, communication load, and downside risk",
    "services": "bench risk, client dependency, and stale-skill exposure",
    "startup": "cash-equity mix, dilution risk, and exit uncertainty",
}

CATEGORY_PROFILES = {
    "career-reality-checks": {
        "overview": "This cluster holds broad market resets: pages for readers who need one honest frame before they choose a role, course, or next move.",
        "what_people_miss": [
            "The viral story is rarely the base-rate outcome.",
            "A better title can hide worse long-term leverage.",
            "Decision quality matters more when the market is noisy.",
        ],
        "questions": [
            "Which narratives sound attractive but break under real constraints?",
            "What trade-offs show up only after 12 to 24 months?",
            "Which decisions protect downside before optimizing upside?",
        ],
    },
    "career-strategy": {
        "overview": "Career strategy pages focus on timing, leverage, and downside protection for Indian professionals who are deciding whether to switch, specialize, wait, or step back.",
        "what_people_miss": [
            "You can make a bad move while still getting a salary bump.",
            "Comfort often hides slow skill decay and weaker optionality.",
            "The right move depends on what you are protecting, not just what you want.",
        ],
        "questions": [
            "Is the current role improving leverage or just preserving comfort?",
            "Should you switch now, stay and deepen, or reset expectations first?",
            "What evidence would make a move rational instead of emotional?",
        ],
    },
    "data-science": {
        "overview": "Data pages separate analytics, reporting, platform, and ML work so readers do not confuse the title with the actual operating reality.",
        "what_people_miss": [
            "Most junior data roles are closer to analytics support than frontier ML.",
            "SQL and stakeholder clarity matter earlier than model sophistication.",
            "The title says 'data science' long before the work truly does.",
        ],
        "questions": [
            "How much of the role is dashboards, pipelines, or model deployment?",
            "Where does salary growth come from after the first title bump?",
            "What signals show a team is serious about production AI work?",
        ],
    },
    "design": {
        "overview": "Design coverage focuses on the difference between visual output, product thinking, and real business influence in Indian teams.",
        "what_people_miss": [
            "Polished UI work does not guarantee better strategic ownership.",
            "Portfolio depth matters more than surface-level motion trends.",
            "Growth stalls when designers ship pixels without owning outcomes.",
        ],
        "questions": [
            "How much discovery or research authority does the role actually hold?",
            "What separates execution-heavy design work from career-compounding work?",
            "When does a portfolio show taste versus shipped impact?",
        ],
    },
    "education": {
        "overview": "Education pages audit expensive bets like degrees, bootcamps, and certificates through the lens of ROI, signal value, and opportunity cost.",
        "what_people_miss": [
            "Brand, peer group, and timing often matter more than curriculum decks.",
            "A credential does not erase bad market timing or weak execution.",
            "The real cost is tuition plus lost earnings plus delayed leverage.",
        ],
        "questions": [
            "What outcome justifies the total cost of the credential?",
            "Which education bets actually change access to better roles?",
            "When is self-study or on-the-job depth the better route?",
        ],
    },
    "engineering": {
        "overview": "Engineering pages look at scope quality, stack durability, and the difference between staying busy and becoming more valuable in the market.",
        "what_people_miss": [
            "Coding volume and career value are not the same thing.",
            "Legacy comfort compounds into negotiation weakness.",
            "The best projects are the ones that create reusable leverage, not just tickets closed.",
        ],
        "questions": [
            "What kind of engineering work compounds beyond the current employer?",
            "How do stack choices affect mobility over the next two years?",
            "What signals show that title growth is outrunning capability growth?",
        ],
    },
    "financial-reality": {
        "overview": "Financial reality pages translate salary headlines into usable decision quality: what actually hits your account, what inflation erodes, and what risk-adjusted progress looks like.",
        "what_people_miss": [
            "Headline CTC and real take-home can point to very different conclusions.",
            "Lifestyle creep can erase supposedly premium compensation fast.",
            "A richer package is not always a better financial decision.",
        ],
        "questions": [
            "How much does the offer really improve after tax and structure?",
            "What trade-offs matter more than the top-line number?",
            "Which compensation stories ignore inflation or city cost pressure?",
        ],
    },
    "learning": {
        "overview": "Learning pages ask whether courses, certificates, and upskilling plans are building real leverage or just producing the feeling of progress.",
        "what_people_miss": [
            "Learning can become procrastination with better branding.",
            "Courses rarely fix a weak portfolio of shipped work.",
            "Depth compounds only when the market can observe it.",
        ],
        "questions": [
            "What proof of work should follow the learning plan?",
            "When does another course stop improving career outcomes?",
            "How do you tell whether skill growth is actually market-visible?",
        ],
    },
    "marketing": {
        "overview": "Marketing pages separate channel busywork from leverage-building work across agencies, in-house teams, and B2B growth roles.",
        "what_people_miss": [
            "More campaigns do not automatically mean more career capital.",
            "Client chaos and strategy ownership are very different things.",
            "Execution-heavy growth roles can hide flat salary trajectories.",
        ],
        "questions": [
            "Where does strategic authority start in this path?",
            "How much of the role is reporting versus real decision influence?",
            "Which environment builds stronger case studies and pay growth?",
        ],
    },
    "money-reality": {
        "overview": "Money reality pages focus on compounding, purchasing power, and how seemingly strong compensation choices can still produce weak life outcomes.",
        "what_people_miss": [
            "A higher salary can still be a bad trade after stress, instability, or city costs.",
            "Variable pay and upside stories need to survive base-case math.",
            "Personal finance outcomes depend on behavior and structure, not just earnings.",
        ],
        "questions": [
            "How does this income decision feel after tax, rent, and inflation?",
            "What risks are hidden behind a glamorous compensation story?",
            "Which money choices improve flexibility instead of just status?",
        ],
    },
    "product-management": {
        "overview": "Product management coverage separates genuine business ownership from coordination-heavy PM work that looks senior but compounds poorly.",
        "what_people_miss": [
            "Owning Jira is not the same thing as owning outcomes.",
            "PM salary upside depends on decision authority, not ticket throughput.",
            "The fastest career stalls happen when execution hides missing strategy depth.",
        ],
        "questions": [
            "How much authority does the PM actually hold in this environment?",
            "What mix of discovery, prioritization, and metrics ownership exists?",
            "Which PM experiences make future roles easier to win?",
        ],
    },
    "software-engineering": {
        "overview": "Software engineering pages go deeper into coding roles, stack positioning, and the long-term difference between framework familiarity and durable engineering leverage.",
        "what_people_miss": [
            "Framework fluency is easier to replace than systems judgment.",
            "Many engineering careers stall because the work stays narrow for too long.",
            "Pay growth follows scope and business value, not tool fandom.",
        ],
        "questions": [
            "What kind of engineering work ages well in the Indian market?",
            "How do frontend, backend, and platform roles diverge over time?",
            "When does specialization deepen value versus trap mobility?",
        ],
    },
}

CASUAL_BIO_MARKERS = (
    "thought leader",
    "linkedin influencer",
    "content calendar",
    "bullshit",
    "bored",
    "frustrated",
)


def _clean_text(value):
    text = strip_tags(value or "")
    return re.sub(r"\s+", " ", text).strip()


def _truncate_words(text, max_words=28):
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]).rstrip(",;:") + "..."


def _first_sentence(value, fallback, max_words=28):
    text = _clean_text(value)
    if not text:
        return fallback
    sentences = re.split(r"(?<=[.!?])\s+", text)
    candidate = next((s.strip() for s in sentences if len(s.split()) >= 7), text)
    candidate = _truncate_words(candidate, max_words=max_words)
    if candidate.endswith((".", "!", "?")):
        return candidate
    return candidate + "."


def _article_topics(article):
    title = _clean_text(getattr(article, "title", ""))
    category_slug = getattr(getattr(article, "category", None), "slug", "")
    haystack = " ".join(
        [
            title,
            _clean_text(getattr(article, "common_expectation", "")),
            _clean_text(getattr(article, "actual_reality", "")),
            _clean_text(getattr(article, "salary_reality", "")),
            _clean_text(getattr(article, "stuck_point", "")),
            _clean_text(getattr(article, "verdict", "")),
        ]
    ).lower()

    topics = set(CATEGORY_TOPIC_MAP.get(category_slug, ()))
    for keyword, mapped_topics in KEYWORD_TOPIC_MAP.items():
        if keyword in haystack:
            topics.update(mapped_topics)
    if not topics:
        topics.add("career")
    return topics


def _topic_signal_summary(article):
    for topic in sorted(_article_topics(article)):
        if topic in TOPIC_SIGNAL_TEXT:
            return TOPIC_SIGNAL_TEXT[topic]
    return TOPIC_SIGNAL_TEXT["career"]


def build_article_sources(article):
    checked_on = getattr(article, "last_reality_check", None)
    if checked_on is None and getattr(article, "updated_at", None):
        checked_on = article.updated_at.date()

    source_keys = ["ambitionbox", "glassdoor", "linkedin_jobs", "naukri_jobs"]
    for topic in sorted(_article_topics(article)):
        source_keys.extend(TOPIC_SOURCE_KEYS.get(topic, ()))

    unique_keys = []
    for key in source_keys:
        if key not in unique_keys and key in SOURCE_LIBRARY:
            unique_keys.append(key)

    return [{**SOURCE_LIBRARY[key], "checked_on": checked_on} for key in unique_keys[:6]]


def build_article_update_log(article):
    title = _clean_text(getattr(article, "title", "this analysis"))
    category_name = _clean_text(getattr(getattr(article, "category", None), "name", "career"))
    signals = _topic_signal_summary(article)
    logs = []
    if getattr(article, "updated_at", None):
        logs.append(
            {
                "date": article.updated_at.date(),
                "summary": f"Updated the benchmarks, downside notes, and decision guidance for {title}.",
            }
        )
    if getattr(article, "last_reality_check", None):
        logs.append(
            {
                "date": article.last_reality_check,
                "summary": f"Rechecked {signals} for this {category_name.lower()} page against current reference points.",
            }
        )
    if getattr(article, "published_at", None):
        logs.append(
            {
                "date": article.published_at.date(),
                "summary": f"Published the first edition of this India-focused reality check on {title}.",
            }
        )
    return logs


def _sources_for_section(section_id, source_refs):
    matching = [
        source
        for source in source_refs
        if section_id in source.get("sections", ()) or "all" in source.get("sections", ())
    ]
    return matching or source_refs[:2]


def build_evidence_map(article, source_refs):
    title = _clean_text(getattr(article, "title", "this path"))
    return [
        {
            "section_id": "expectation",
            "claim": _first_sentence(
                getattr(article, "common_expectation", ""),
                f"The public story around {title} usually sounds cleaner than the actual trade-offs.",
            ),
            "sources": _sources_for_section("expectation", source_refs),
        },
        {
            "section_id": "reality",
            "claim": _first_sentence(
                getattr(article, "actual_reality", ""),
                "Real outcomes depend on company quality, timing, and the actual work behind the title.",
            ),
            "sources": _sources_for_section("reality", source_refs),
        },
        {
            "section_id": "salary-growth",
            "claim": _first_sentence(
                getattr(article, "salary_reality", ""),
                "Compensation diverges once role scope, city, and company type are separated.",
            ),
            "sources": _sources_for_section("salary-growth", source_refs),
        },
        {
            "section_id": "stuck-point",
            "claim": _first_sentence(
                getattr(article, "stuck_point", ""),
                "The real plateau usually appears when responsibilities rise without matching leverage growth.",
            ),
            "sources": _sources_for_section("stuck-point", source_refs),
        },
    ]


def build_category_profile(category, article_count):
    category_name = _clean_text(getattr(category, "name", "This topic"))
    slug = getattr(category, "slug", "")
    fallback = {
        "overview": f"{category_name} pages on Career Reality focus on the delta between the marketed version of the path and the version that actually affects salary, scope, and downside risk in India.",
        "what_people_miss": [
            "Titles alone do not tell you how durable the role is.",
            "The best-looking option can still be weak on leverage quality.",
            "You need base-rate signals, not only exceptional success stories.",
        ],
        "questions": [
            f"What does {category_name.lower()} work really look like after the first year?",
            "Which trade-offs stay hidden in job descriptions?",
            "What evidence should you check before betting time or money here?",
        ],
    }
    profile = dict(fallback)
    profile.update(CATEGORY_PROFILES.get(slug, {}))
    profile["reader_fit"] = (
        f"Read this cluster if you are evaluating {category_name.lower()} roles and want evidence before committing to a switch, course, or compensation story."
    )
    profile["article_count_label"] = f"{article_count} published article" if article_count == 1 else f"{article_count} published articles"
    return profile


def build_author_focus_areas(articles):
    counts = Counter(article.category.name for article in articles if getattr(article, "category", None))
    return [name for name, _ in counts.most_common(3)]


def build_author_page_intro(author, article_count, coverage_areas):
    bio = _clean_text(getattr(author, "bio", ""))
    if bio and len(bio.split()) >= 60 and not any(marker in bio.lower() for marker in CASUAL_BIO_MARKERS):
        return bio

    coverage = ", ".join(coverage_areas[:3]) if coverage_areas else "salary reality, role trade-offs, and career risk"
    experience = _clean_text(getattr(author, "experience_summary", "")) or "Coverage is grounded in Indian tech hiring, compensation, and decision trade-offs."
    return (
        f"{author.display_name} contributes {coverage} coverage for Career Reality. "
        f"{experience} This page aggregates {article_count} published pieces under this byline and keeps the correction path visible."
    )


def author_profile_is_indexable(author, article_count):
    return bool(
        article_count >= 10
        and getattr(author, "linkedin_url", "")
        and getattr(author, "experience_summary", "")
    )
