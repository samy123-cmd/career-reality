"""
Central market intelligence for article refresh cycles.

Update MARKET_PERIOD and band tables when running monthly/daily article refreshes.
Keep numbers aligned with templates/core/salary.html and crowdsourced site data.
"""

from __future__ import annotations

from dataclasses import dataclass

# Bump this when running a site-wide refresh (e.g. "2026-06").
MARKET_PERIOD = "2026-06"
MARKET_LABEL = "June 2026"

# Shared macro context for Indian tech (Q2 2026 appraisal season aftermath).
MACRO_BULLETS = (
    "Appraisal season (March–April 2026) compressed offers for general engineering; "
    "counter-offers rose for mid-senior backend and platform roles.",
    "AI/GenAI roles (RAG, agents, eval pipelines) still command 15–35% premiums over "
    "general SWE bands in Bengaluru and Hyderabad.",
    "Junior service-company fresher anchors remain 3.2–4.5 LPA despite inflation; "
    "product-company fresher median is 8–12 LPA.",
    "Layoff signals remain elevated in IT services and mid-tier SaaS; GCC hiring "
    "continues but bar is rising (system design + ownership expected at 4–6 YOE).",
    "Remote US/EU roles pay more on paper but TDS, forex, and contract instability "
    "reduce effective take-home — validate with the CTC Decoder before comparing.",
)

EXTERNAL_SOURCES_HTML = """
<section class="art-source-refs">
<h3>Primary sources referenced in this refresh</h3>
<ul>
  <li><a href="https://www.ambitionbox.com/salaries" rel="noopener noreferrer" target="_blank">AmbitionBox Salary Insights (India)</a></li>
  <li><a href="https://www.glassdoor.co.in/Salaries/index.htm" rel="noopener noreferrer" target="_blank">Glassdoor India Salaries</a></li>
  <li><a href="https://www.naukri.com/jobSpeak" rel="noopener noreferrer" target="_blank">Naukri JobSpeak Index</a></li>
  <li><a href="https://labour.gov.in/" rel="noopener noreferrer" target="_blank">Ministry of Labour &amp; Employment (India)</a></li>
</ul>
<p class="art-source-note">Salary bands are medians from multiple employer-reported and crowdsourced datasets — not unicorn outliers.</p>
</section>
""".strip()


@dataclass(frozen=True)
class SalaryBand:
    role: str
    experience: str
    bengaluru: str
    hyderabad: str
    remote_india: str


SALARY_CLUSTERS: dict[str, tuple[SalaryBand, ...]] = {
    "engineering": (
        SalaryBand("Backend / Platform", "3–5 YOE", "14–22 LPA", "12–19 LPA", "16–24 LPA"),
        SalaryBand("Backend / Platform", "6–9 YOE", "22–32 LPA", "20–28 LPA", "24–36 LPA"),
        SalaryBand("Frontend", "3–5 YOE", "10–16 LPA", "9–14 LPA", "12–18 LPA"),
        SalaryBand("DevOps / SRE", "4–7 YOE", "16–26 LPA", "14–22 LPA", "18–28 LPA"),
        SalaryBand("Tech Lead", "8–12 YOE", "28–42 LPA", "25–38 LPA", "30–45 LPA"),
    ),
    "data": (
        SalaryBand("Data Analyst", "1–3 YOE", "6–10 LPA", "5–9 LPA", "7–11 LPA"),
        SalaryBand("Data Engineer", "3–6 YOE", "14–22 LPA", "12–19 LPA", "15–24 LPA"),
        SalaryBand("ML Engineer", "4–8 YOE", "18–30 LPA", "16–26 LPA", "20–32 LPA"),
        SalaryBand("Senior Data / ML", "7–10 YOE", "26–40 LPA", "22–34 LPA", "28–42 LPA"),
    ),
    "product": (
        SalaryBand("Associate PM", "2–4 YOE", "12–18 LPA", "10–16 LPA", "14–20 LPA"),
        SalaryBand("Product Manager", "5–8 YOE", "22–35 LPA", "18–28 LPA", "24–38 LPA"),
        SalaryBand("Senior PM / GPM", "8–12 YOE", "32–50 LPA", "28–42 LPA", "35–55 LPA"),
    ),
    "design": (
        SalaryBand("UI Designer", "2–4 YOE", "8–14 LPA", "7–12 LPA", "9–15 LPA"),
        SalaryBand("Product Designer", "4–7 YOE", "14–22 LPA", "12–18 LPA", "15–24 LPA"),
        SalaryBand("Senior UX", "6–10 YOE", "20–32 LPA", "18–26 LPA", "22–34 LPA"),
    ),
    "marketing": (
        SalaryBand("Digital Marketing Exec", "1–3 YOE", "4–7 LPA", "3.5–6 LPA", "4–8 LPA"),
        SalaryBand("Performance / Growth", "3–6 YOE", "10–18 LPA", "8–14 LPA", "11–20 LPA"),
        SalaryBand("Marketing Manager", "6–9 YOE", "16–26 LPA", "14–22 LPA", "18–28 LPA"),
    ),
    "general": (
        SalaryBand("IT Services (Dev)", "2–5 YOE", "6–12 LPA", "5–10 LPA", "N/A"),
        SalaryBand("GCC / Captive", "4–8 YOE", "18–32 LPA", "16–28 LPA", "20–34 LPA"),
        SalaryBand("Startup (Series A–C)", "3–7 YOE", "14–28 LPA", "12–24 LPA", "15–30 LPA"),
        SalaryBand("MBA (Tier-1 campus)", "0–2 YOE post-MBA", "22–32 LPA", "20–28 LPA", "N/A"),
    ),
}

CLUSTER_KEYWORDS: dict[str, tuple[str, ...]] = {
    "engineering": (
        "frontend", "devops", "sre", "developer", "engineering", "tech-lead",
        "plateau", "it-services", "performance-review", "job-hopping", "senior-developer",
    ),
    "data": ("data-scientist", "data-science", "sql-janitor"),
    "product": ("product-manager", "product-manager-reality", "coordinator-not-ceo"),
    "design": ("design-reality", "ux-design", "beautiful-screens"),
    "marketing": ("digital-marketing", "marketing", "agency"),
    "general": (
        "mba", "layoff", "remote", "freelanc", "side-hustle", "equity", "esop",
        "networking", "passion", "education", "learning", "upskill", "career-switch",
        "american-dream", "culture-fit", "hr-conversation", "work-life", "manager-vs-ic",
        "hidden-cost", "7-year", "plateau",
    ),
}


def role_cluster_for_article(slug: str, category_name: str = "") -> str:
    """Map an article to a salary/market cluster from slug + category."""
    haystack = f"{slug} {category_name}".lower()
    for cluster, keywords in CLUSTER_KEYWORDS.items():
        if any(kw in haystack for kw in keywords):
            return cluster
    return "general"


def salary_table_html(cluster: str) -> str:
    bands = SALARY_CLUSTERS.get(cluster, SALARY_CLUSTERS["general"])
    rows = "".join(
        f"<tr><td>{b.role}</td><td>{b.experience}</td>"
        f"<td>{b.bengaluru}</td><td>{b.hyderabad}</td><td>{b.remote_india}</td></tr>"
        for b in bands
    )
    return f"""
<table class="editorial-table">
  <thead>
    <tr>
      <th>Role</th><th>Experience</th><th>Bengaluru</th><th>Hyderabad</th><th>Remote (India)</th>
    </tr>
  </thead>
  <tbody>{rows}</tbody>
</table>
<p><em>Medians for {MARKET_LABEL}. Use the <a href="/salary-calculator/">CTC Decoder</a> for in-hand estimates.</em></p>
""".strip()


def market_update_html(cluster: str) -> str:
    cluster_notes = {
        "engineering": "Platform and backend hiring picked up in GCCs; IT services bench strength remains a risk for 4–7 YOE engineers without system design depth.",
        "data": "Most 'data scientist' postings still map to analytics or pipeline work; true ML roles require production deployment evidence, not notebook Kaggle wins.",
        "product": "PM hiring is selective — execution and metrics ownership matter more than MBA pedigree in product-first companies.",
        "design": "UI-only roles are commoditising; product design with research + metrics commands better bands.",
        "marketing": "Performance marketing and marketing ops roles hold up; pure 'creative' agency roles remain low-leverage for long-term comp growth.",
        "general": "Cross-role switching costs rise after 30; financial planning beats motivational pivots.",
    }
    bullets = "".join(f"<li>{b}</li>" for b in MACRO_BULLETS)
    note = cluster_notes.get(cluster, cluster_notes["general"])
    return f"""
<section class="art-market-update">
  <h3>Market update — {MARKET_LABEL}</h3>
  <p><strong>Cluster read ({cluster.replace('_', ' ').title()}):</strong> {note}</p>
  <ul>{bullets}</ul>
  <p>Compare live ranges on <a href="/salary-reality/">Salary Reality</a> and track employer signals on <a href="/layoff-radar/">Layoff Radar</a>.</p>
</section>
""".strip()
