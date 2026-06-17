#!/usr/bin/env python3
"""One-off generator: build content/expansions/articles.py from publish scripts + extensions."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _exec_publish(path: str, start_marker: str, end_marker: str | None = None) -> dict:
    text = (ROOT / path).read_text()
    chunk = text[text.index(start_marker) :]
    if end_marker and end_marker in chunk:
        chunk = chunk[: chunk.index(end_marker)]
    elif "Article.objects.update_or_create" in chunk:
        chunk = chunk[: chunk.index("Article.objects.update_or_create")]
    ns: dict = {}
    exec(chunk, ns)  # noqa: S102
    return ns


def _link_footer() -> str:
    return """
<p>Cross-check your numbers with our <a href="/salary-calculator/">CTC Decoder</a> and
<a href="/salary-reality/">Salary Reality</a> guides before negotiating.</p>
"""


def _source_footer() -> str:
    return """
<p class="art-source-note">Bands reference employer-reported medians from
<a href="https://www.ambitionbox.com/salaries" rel="noopener noreferrer" target="_blank">AmbitionBox India</a>,
<a href="https://www.glassdoor.co.in/Salaries/index.htm" rel="noopener noreferrer" target="_blank">Glassdoor India</a>, and hiring velocity from the
<a href="https://www.naukri.com/jobSpeak" rel="noopener noreferrer" target="_blank">Naukri JobSpeak Index</a> (June 2026).</p>
"""


def _plateau() -> dict:
    ns = _exec_publish(
        "publish_article_1.py",
        "# 3. ARTICLE DATA",
        "# 5. PUBLISH WITH FINAL METADATA",
    )
    return {
        "aliases": ["7-year-career-plateau-india"],
        "title": ns["title"],
        "meta_title": "The 7-Year Career Plateau Nobody Warns You About",
        "meta_description": (
            "Why Indian tech careers stall after 6–10 years: salary compression, "
            "promotion theatre, and how to break the mid-career plateau in 2026."
        ),
        "target_persona": ns["target_persona"],
        "who_should_avoid": ns["who_should_avoid"],
        "common_expectation": ns["common_expectation"],
        "actual_reality": ns["actual_reality"]
        + """
<p>Before you accept another incremental hike, model your in-hand against current Bengaluru and Hyderabad bands using the
<a href="/salary-calculator/">CTC Decoder</a>. If your title changed but your take-home did not, you are likely in maintenance mode — not growth mode.
Compare broader compensation trends on our <a href="/salary-reality/">Salary Reality</a> pillar and the
<a href="/layoff-radar/">Layoff Radar</a> before deciding whether to stay for "stability."</p>
""",
        "salary_reality": ns["salary_reality"] + _source_footer(),
        "stuck_point": ns["stuck_point"],
        "verdict": ns["verdict"]
        + """
<p>Breaking a plateau is rarely about one more certification. It is about choosing leverage: either depth in a scarce skill cluster
or a visible move into ownership (people, revenue, or platform). Use the
<a href="/resignation-risk/">Resignation Risk Analyzer</a> if you are weighing an external switch against loyalty optics.</p>
""",
    }


def _twenty_lpa() -> dict:
    ns = _exec_publish(
        "publish_article_20lpa.py",
        "# VISUAL DATA",
        "# 5. PUBLISH",
    )
    extra_reality = """
<p>Family obligations compress savings further. Supporting parents, sibling education, or wedding contributions are culturally expected
but rarely appear in LinkedIn posts about "20 LPA life." A ₹50,000 annual transfer to family is normal — and invisible in CTC bragging.</p>
<p>Tax regime choice matters: the new regime simplifies slabs but removes many deductions. Rent in metro cities rarely qualifies for meaningful relief.
Many professionals discover their effective tax rate is higher than spreadsheet models because bonus payouts, RSU vesting, and variable pay
are taxed in the year they hit — creating surprise March shortfalls.</p>
<p>₹20 LPA in Pune or Ahmedabad feels different from Bengaluru. The same CTC in a tier-2 city can leave ₹15,000–20,000 more monthly after rent,
which is why "remote from hometown" became the stealth upgrade path after 2023. Location arbitrage is real; lifestyle inflation erases it when
you insist on metro amenities at hometown salaries.</p>
"""
    extra_salary = """
<p><strong>City reality check (June 2026, 1BHK decent society, single earner):</strong></p>
<ul>
<li><strong>Bengaluru / Mumbai / Gurugram:</strong> rent ₹32,000–45,000; comfortable savings often under ₹25,000/month unless sharing</li>
<li><strong>Hyderabad / Pune:</strong> rent ₹22,000–32,000; savings potential ₹30,000–40,000 with discipline</li>
<li><strong>Ahmedabad / Jaipur / Kochi:</strong> rent ₹14,000–22,000; ₹20 LPA can feel genuinely upper-middle if lifestyle held flat</li>
</ul>
<p>Employer data from <a href="https://labour.gov.in/" rel="noopener noreferrer" target="_blank">Ministry of Labour &amp; Employment</a>
reports and private salary surveys consistently show metro cost-of-living growth outpacing median IT hikes since 2022.</p>
"""
    extra_verdict = """
<p>Build a 12-month runway before upgrading lifestyle. Track savings rate monthly — not CTC annually.
If you are evaluating whether a new offer actually improves life, run the numbers in the
<a href="/salary-calculator/">CTC Decoder</a> and read purchasing-power context on
<a href="/salary-reality/">Salary Reality</a>.</p>
"""
    return {
        "aliases": ["what-20-LPA-feels-like-india"],
        "title": "What ₹20 LPA Actually Feels Like in India",
        "meta_title": "What ₹20 LPA Actually Feels Like in India (2026)",
        "meta_description": (
            "₹20 LPA in-hand math for metro India: rent, tax, EMIs, and why it feels middle-class — "
            "plus city-by-city purchasing power in June 2026."
        ),
        "target_persona": ns["target_persona"],
        "who_should_avoid": ns["who_should_avoid"],
        "common_expectation": ns["common_expectation"],
        "actual_reality": ns["actual_reality"] + extra_reality,
        "salary_reality": ns["salary_reality"] + extra_salary + _source_footer(),
        "stuck_point": ns["stuck_point"],
        "verdict": ns["verdict"] + extra_verdict,
    }


def _upskilling() -> dict:
    ns = _exec_publish("publish_gold_batch.py", "table_1 = ")
    extra = """
<p>By year five, interview loops shift from "can you implement X?" to "tell me about a production incident you owned."
Hiring managers discount certificates because they correlate poorly with incident response, stakeholder management, and trade-off judgment under ambiguity.</p>
<p>EdTech marketing exploits fear of obsolescence. The rational response at mid-career is selective depth: one domain (payments, data platforms, search ranking)
plus proof of outcomes — latency reduced, cost saved, revenue unlocked — not a portfolio of half-finished courses.</p>
<p>Internal mobility follows the same rule. Promotions go to people who de-risk launches, not people who know the newest framework.
If your learning is invisible to P&amp;L, it will not move compensation.</p>
<p>Performance reviews at 7+ YOE rarely ask "what course did you finish?" They ask: What revenue did you protect?
What outage did you prevent? What team did you unblock? Certificates answer none of those questions.</p>
<p>A practical test: list three production outcomes from the last 12 months. If you cannot, more courses will not fix the gap —
scope and ownership will.</p>
<p>Indian GCC and product firms increasingly score candidates on incident stories and business impact slides in loop rounds.
Prepare those narratives instead of adding another badge to LinkedIn Learning.</p>
"""
    salary_extra = """
<p><strong>What actually moves pay after year 4 (India product/GCC market, 2026):</strong></p>
<ul>
<li>Shipping a measurable business outcome (conversion, retention, infra cost)</li>
<li>Owning a production system with on-call credibility</li>
<li>Cross-functional trust: eng + product + sales alignment</li>
<li>Narrow reputation: "the person who fixed billing" beats "knows 12 languages"</li>
</ul>
"""
    return {
        "aliases": ["why-upskilling-stops-working"],
        "title": "Why 'Upskilling' Stops Working After a Point",
        "meta_title": "Why Upskilling Stops Working After Year 4",
        "meta_description": (
            "Certificates plateau after 3 years in Indian tech. Why judgment, outcomes, and politics "
            "replace courses — and what to do instead in 2026."
        ),
        "target_persona": ns["persona_1"],
        "who_should_avoid": ns["avoid_1"],
        "common_expectation": ns["expectation_1"],
        "actual_reality": ns["reality_1"] + extra,
        "salary_reality": ns["salary_reality_1"] + salary_extra + _source_footer(),
        "stuck_point": ns["stuck_1"],
        "verdict": ns["verdict_1"]
        + _link_footer()
        + """<p>Explore role-specific salary bands in our <a href="/category/data-science/">Data Science</a> and
<a href="/category/engineering/">Engineering</a> categories before buying another course bundle.</p>""",
    }


def _it_services() -> dict:
    ns = _exec_publish("publish_gold_batch.py", "table_2 = ")
    extra = """
<p>WITCH firms optimize utilization rates. Your learning budget is billable hours. Greenfield stacks appear in internal demos;
client delivery stays on stable, boring versions because change orders are expensive. After six years, your résumé lists "12 years Java"
but the market wanted cloud-native, event-driven, or data-platform experience you never billed for.</p>
<p>Product companies filter résumés with keyword screens. "Infosys — banking maintenance" often lands in the same bucket as "legacy support"
unless you can show ownership metrics. The exit window is years 3–6: enough experience to be credible, not so much tenure that switching
requires a title downgrade and 40% pay cut.</p>
<p>On-site promises are retention tools, not career plans. Visa allocation is political. Many engineers defer product switches for a US trip
that arrives after their skills aged out of local product hiring loops.</p>
<p>Internal "digital transformation" projects rarely translate to résumé-worthy stack depth. You may demo Kubernetes in a lab while billing
hours on ticket queues. Recruiters outside services recognize the pattern quickly.</p>
<p>If you are in year 4–5, treat the next 12 months as an exit sprint: one product-style project on nights/weekends, one OSS or Kaggle-style
portfolio piece is not enough — ship something with metrics, document it, and interview before year 7.</p>
"""
    salary_extra = """
<p><strong>Illustrative compensation divergence (same YOE, June 2026 medians):</strong></p>
<ul>
<li><strong>IT services (5–8 YOE):</strong> ₹9–14 LPA in-hand with 5–8% annual hikes</li>
<li><strong>Product / GCC (5–8 YOE):</strong> ₹18–28 LPA with switch-driven 20–35% jumps</li>
<li><strong>After 10 YOE in services:</strong> switching often requires accepting "Senior" titles at mid-band pay to relearn stack</li>
</ul>
<p>Retention bonuses (₹1–3 LPA paid over 24 months) look generous but lock you through another appraisal cycle while product peers compound equity and refresh grants.</p>
"""
    return {
        "aliases": ["hidden-cost-it-services-india"],
        "title": "The Hidden Cost of Staying in IT Services Too Long",
        "meta_title": "Hidden Cost of Staying in IT Services Too Long",
        "meta_description": (
            "Why WITCH tenure past year 6 hurts product hiring, legacy tech traps, and salary "
            "compression vs product companies in India (2026)."
        ),
        "target_persona": ns["persona_2"],
        "who_should_avoid": ns["avoid_2"]
        + """
<p>If you have already crossed eight years in the same service account with no internal transfer to a modern stack, the honest default is to
optimize for stability and side income — not pretend a product switch will be frictionless.</p>
""",
        "common_expectation": ns["expectation_2"],
        "actual_reality": ns["reality_2"] + extra,
        "salary_reality": ns["salary_reality_2"] + salary_extra + _source_footer(),
        "stuck_point": ns["stuck_2"]
        + """
<p>Many engineers confuse employer loyalty programs (retention bonuses, grade promotions) with market competitiveness.
A 7% hike on a below-market base still leaves you underpaid relative to product peers — but feels like progress because the letter arrived on time.</p>
""",
        "verdict": ns["verdict_2"]
        + _link_footer()
        + """<p>Stress-test a switch timing with the <a href="/resignation-risk/">Resignation Risk Analyzer</a> and
<a href="/layoff-radar/">Layoff Radar</a> before signing another "safe" retention bonus.</p>""",
    }


def _career_switch() -> dict:
    ns = _exec_publish("publish_gold_batch.py", "table_3 = ")
    extra = """
<p>Bootcamps sell velocity; employers hire for production proof. At 32, you compete with 24-year-olds who treat ₹8 LPA as runway money
while you have ₹80,000 in fixed obligations. The math is brutal: a 40% pay cut on ₹18 LPA removes ₹7.2 LPA — roughly ₹45,000 monthly —
before you learn enough to recover.</p>
<p>Transferable skills matter <em>after</em> technical credibility. Communication helps you lead squads once you can ship.
It does not exempt you from junior technical loops. Many career switchers fail interviews not on coding alone but on system thinking:
APIs, databases, debugging, reading unfamiliar codebases under time pressure.</p>
<p>The 24-month recovery model is realistic: 6 months learning, 6 months junior role, 12 months to mid-level if you outperform.
Family buy-in matters as much as curriculum. Partners who expected lifestyle continuity will experience the switch as regression even if
long-term trajectory improves.</p>
<p>Network effects reset too. Your sales contacts do not help in backend interviews. Your MBA batchmates hire from familiar pipelines.
You must rebuild credibility from zero — referrals, GitHub, take-home assignments, and cold applications with lower response rates.</p>
<p>Part-time switching rarely works for deep technical pivots. "Evenings and weekends" competing against 22-year-olds who study full-time
extends the valley of death to 36+ months. Savings buffers should assume 18 months, not 6.</p>
"""
    salary_extra = """
<p><strong>Sample switch economics (₹18 LPA → product track, tier-1 city):</strong></p>
<ul>
<li><strong>Year 0:</strong> ₹18 LPA in-hand ~₹1.05L/month; obligations often ₹75k+</li>
<li><strong>Year 1 (junior offer):</strong> ₹8–10 LPA → in-hand ~₹55–65k; gap funded by 12-month savings buffer</li>
<li><strong>Year 3 (mid-level):</strong> ₹16–22 LPA if performance proves; still below peers who never switched</li>
<li><strong>Year 5+:</strong> upside if you compound; many exit earlier due to financial pressure</li>
</ul>
<p>Include health insurance, parental support, and school fees in the model — switchers often underestimate fixed costs when in-hand drops 40%.</p>
"""
    return {
        "aliases": ["career-switching-after-30-india"],
        "title": "Career Switching After 30: The Trade-Offs Nobody Posts About",
        "meta_title": "Career Switching After 30 in India: Real Costs",
        "meta_description": (
            "Salary cuts, ego reset, and 24-month recovery math for career changers after 30 in Indian tech — "
            "what bootcamps do not show."
        ),
        "target_persona": ns["persona_3"]
        + """
<p>You may also be a parent or primary earner — which makes the ego reset harder than bootcamp marketing ever acknowledges.</p>
""",
        "who_should_avoid": ns["avoid_3"],
        "common_expectation": ns["expectation_3"]
        + """
<p>Social media amplifies survivor bias: you see the 35-year-old who became a PM after a bootcamp, not the hundred who returned to B2B sales
after 14 months of unemployment. Plan for the median outcome, not the highlight reel.</p>
""",
        "actual_reality": ns["reality_3"] + extra,
        "salary_reality": ns["salary_reality_3"] + salary_extra + _source_footer(),
        "stuck_point": ns["stuck_3"]
        + """
<p>Another trap is hybrid titles — "Technical Product Manager" or "Business Analyst with Python" — that sound senior but pay analyst bands.
Read the job description for IC coding expectations before celebrating a title that sounds like a level skip.</p>
""",
        "verdict": ns["verdict_3"] + _link_footer()
        + """
<p>Build a written 24-month budget before enrolling anywhere. If the plan requires magic (instant senior role, no pay cut, no evening study),
the plan is fantasy — not a career strategy. Write the numbers down; optimism is not a spreadsheet.</p>
""",
    }


def _junior_ds() -> dict:
    ns = _exec_publish("publish_job_batch.py", "table_1 = ")
    extra = """
<p>Title inflation is rampant: "Junior Data Scientist" often means Excel + SQL + Power BI with Python sprinkled in job descriptions.
LLM hype accelerated mislabeling — founders want "AI" on the org chart before they have a warehouse worth modeling.</p>
<p>Hiring in 2026 favors data engineers who can ship pipelines over notebook experimenters. GenAI teams still need clean feature stores,
eval datasets, and cost-controlled inference — all janitorial work at scale. Freshers who resist SQL spend months unemployed while
bootcamp peers with DBT + Airflow land ₹10–14 LPA analyst roles that actually exist.</p>
<p>Interview loops expose the gap quickly: take-home assignments ask for reproducible ETL, not Kaggle leaderboard scores.
Production means idempotent jobs, monitoring, and explaining null rates to a CFO — not tuning learning rates.</p>
"""
    salary_extra = """
<p><strong>Role clarity vs pay (India, June 2026):</strong></p>
<ul>
<li><strong>Mislabelled "Data Scientist" (analyst):</strong> ₹5–9 LPA; SQL, dashboards, ad-hoc requests</li>
<li><strong>Data Engineer (0–3 YOE):</strong> ₹8–14 LPA; pipelines, warehouse modeling, on-call rotation</li>
<li><strong>Applied ML (rare, strong pedigree):</strong> ₹14–22 LPA; requires portfolio + systems depth</li>
<li><strong>Research / LLM lab roles:</strong> ₹18–30 LPA; tiny hiring pool, MS/PhD or exceptional OSS</li>
</ul>
"""
    return {
        "aliases": [],
        "title": "The Brutal Reality of Junior Data Scientist Jobs in India (2026)",
        "meta_title": "Junior Data Scientist Jobs India: Reality 2026",
        "meta_description": (
            "Why most junior data scientist roles are SQL janitor work, real 2026 salary bands, "
            "and how to escape the Kaggle trap in India."
        ),
        "target_persona": ns["persona_1"],
        "who_should_avoid": ns["avoid_1"],
        "common_expectation": ns["expectation_1"],
        "actual_reality": ns["reality_1"] + extra,
        "salary_reality": ns["salary_reality_1"] + salary_extra + _source_footer(),
        "stuck_point": ns["stuck_1"],
        "verdict": ns["verdict_1"]
        + """<p>Compare data-role bands in our <a href="/category/data-science/">Data Science category</a> and validate offers with the
<a href="/salary-calculator/">CTC Decoder</a> before accepting a flashy title.</p>""",
    }


def main() -> None:
    expansions = {
        "the-7-year-career-plateau-nobody-warns-you-about": _plateau(),
        "what-20-lpa-actually-feels-like-india-purchasing-power": _twenty_lpa(),
        "why-upskilling-stops-working-career-trap": _upskilling(),
        "hidden-cost-of-staying-in-it-services-too-long": _it_services(),
        "career-switching-after-30-the-brutal-truth": _career_switch(),
        "junior-data-scientist-reality-india": _junior_ds(),
    }

    out = ROOT / "content" / "expansions" / "articles.py"
    lines = [
        '"""Editorial body copy for six thin core articles (900+ words each)."""',
        "",
        "from __future__ import annotations",
        "",
        "CORE_ARTICLE_EXPANSIONS: dict[str, dict] = ",
    ]
    import pprint

    body = pprint.pformat(expansions, width=100, sort_dicts=False)
    out.write_text("\n".join(lines) + body + "\n")
    print(f"Wrote {out} ({len(expansions)} articles)")


if __name__ == "__main__":
    main()
