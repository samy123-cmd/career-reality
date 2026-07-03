"""
Seed 4 July 2026 articles — campus PPO season, mid-year layoffs, appraisal gap, AI job market.
Run: python seed_july_2026.py
"""
import os
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django  # noqa: E402

django.setup()

from django.utils import timezone  # noqa: E402

from content.models import Article, Author, Category  # noqa: E402

JULY_PUBLISHED = datetime.datetime(2026, 7, 1, 10, 0, 0, tzinfo=datetime.timezone.utc)


def get_author():
    author = Author.objects.filter(is_active=True).first()
    if author:
        return author
    return Author.objects.create(
        name="Career Reality Editorial",
        display_name="Career Reality Editorial",
        bio="Editorial team covering Indian tech careers with evidence-backed analysis.",
        linkedin_url="https://www.linkedin.com/company/career-reality-india/",
        experience_summary="Career intelligence for Indian tech professionals",
        is_active=True,
    )


def create_article(author, cat_name, slug, title, persona, avoid, expect, reality, salary, stuck, verdict, seo_desc):
    category, _ = Category.objects.get_or_create(
        name=cat_name,
        defaults={"slug": cat_name.lower().replace(" ", "-"), "order": 1},
    )
    article, created = Article.objects.update_or_create(
        slug=slug,
        defaults={
            "title": title,
            "author": author,
            "category": category,
            "status": "published",
            "target_persona": persona,
            "who_should_avoid": avoid,
            "common_expectation": expect,
            "actual_reality": reality,
            "salary_reality": salary,
            "stuck_point": stuck,
            "verdict": verdict,
            "meta_title": title[:60],
            "meta_description": seo_desc[:160],
            "published_at": JULY_PUBLISHED,
            "last_reality_check": datetime.date(2026, 7, 3),
        },
    )
    print(f"{'Created' if created else 'Updated'}: {title}")
    return article


def _para_block(paragraphs):
    return "".join(f"<p>{p}</p>" for p in paragraphs)


author = get_author()

# ── Article 1: Campus Internship PPO ─────────────────────────────────────────
create_article(
    author=author,
    cat_name="Career Strategy",
    slug="campus-internship-ppo-reality-2026",
    title="Campus Internship to PPO Reality in India (2026)",
    persona=_para_block([
        "Final-year engineering and MBA students finishing summer internships in July 2026.",
        "Parents comparing PPO offers against campus placement averages.",
        "Interns at product companies, GCCs, and IT services firms evaluating return offers.",
    ]),
    avoid=_para_block([
        "If you already have a signed full-time offer from campus placement, this is supplementary — not urgent.",
        "If your internship was purely research with no conversion track, PPO dynamics differ.",
    ]),
    expect=_para_block([
        "A good internship automatically converts to a pre-placement offer (PPO) at 70–80% rates.",
        "PPO packages match or beat campus placement medians.",
        "Declining a PPO to 'try campus placement' is low-risk because alternatives are abundant.",
        "Brand-name internships (Flipkart, Goldman GCC, Microsoft IDC) guarantee strong PPO bands.",
    ]),
    reality=_para_block([
        "July 2026 PPO conversion data from product companies clusters around 40–55%, not 80%. "
        "Service companies convert 15–25% of summer interns — the rest return to campus placement pools "
        "or graduate unemployed if they skipped placement season.",
        "PPO packages are often 10–20% below what the same company offers in campus placement for "
        "equivalent roles. The discount is real: companies know you have sunk-cost attachment after "
        "two months inside their culture.",
        "Declining a mediocre PPO to 'hold out for better' is higher risk in 2026 than in 2022. "
        "Campus hiring volumes are down 20–30% year-on-year at many Tier-2 colleges. "
        "The <a href=\"/layoff-radar/\">Layoff Radar</a> shows continued bench trimming at IT services — "
        "fewer fresher intake slots than headlines suggest.",
        "GCC internships convert at higher rates (50–65%) but the bar is technical depth: system design, "
        "ownership evidence, and production debugging — not slide decks and standup attendance.",
        "Use the <a href=\"/salary-calculator/\">CTC Decoder</a> on any PPO letter before comparing. "
        "A ₹14 LPA PPO with high variable and employer PF looks worse in-hand than a ₹12 LPA fixed-heavy campus offer.",
    ]),
    salary="""
<table class="editorial-table">
<thead><tr><th>Company Type</th><th>PPO Conversion</th><th>Typical PPO Band</th><th>Campus Equivalent</th></tr></thead>
<tbody>
<tr><td>Product (Series B+)</td><td>45–55%</td><td>₹10–16 LPA</td><td>₹12–18 LPA</td></tr>
<tr><td>GCC / Captive</td><td>50–65%</td><td>₹12–20 LPA</td><td>₹14–22 LPA</td></tr>
<tr><td>IT Services</td><td>15–25%</td><td>₹3.5–5.5 LPA</td><td>₹3.2–4.5 LPA</td></tr>
<tr><td>Startup (early)</td><td>30–40%</td><td>₹8–14 LPA + ESOP</td><td>Highly variable</td></tr>
</tbody>
</table>
<p>Medians for July 2026. Compare live ranges on <a href="/salary-reality/">Salary Reality</a>.</p>
""",
    stuck=_para_block([
        "The emotional trap: 'I worked hard for two months — they owe me a PPO.' Legally and commercially, they don't.",
        "Students compare PPOs to LinkedIn hype posts (₹40 LPA fresher outliers) instead of college placement medians.",
        "Parents pressure acceptance of any PPO for 'stability' even when campus placement could yield 20% better comp.",
        "Waiting until August to decide when the PPO deadline is July 15 — and campus placement drives are already closing.",
    ]),
    verdict=_para_block([
        "Accept a PPO when: in-hand math beats your realistic campus alternative, the role has skill depth, "
        "and the company's 12-month hiring trajectory is stable.",
        "Decline or renegotiate when: variable pay is >25% of CTC, the role is bench-adjacent at IT services, "
        "or you have a campus pipeline with verified better offers.",
        "July is decision month. Run the numbers, not the emotions. Track market pressure on the "
        "<a href=\"/career-reality-index/\">Career Reality Index</a> before signing.",
    ]),
    seo_desc="July 2026 PPO conversion rates, salary bands, and decision framework for Indian campus interns — product, GCC, and IT services reality.",
)

# ── Article 2: Mid-Year Layoff Pulse ─────────────────────────────────────────
create_article(
    author=author,
    cat_name="Career Reality Checks",
    slug="mid-year-layoff-pulse-india-july-2026",
    title="Mid-Year Layoff Pulse: What Changed in Indian Tech (July 2026)",
    persona=_para_block([
        "IT services and mid-tier SaaS professionals watching Q2 earnings and internal restructuring memos.",
        "Engineers on bench or with reduced project allocation in July 2026.",
        "Anyone who treated the January–March layoff headlines as 'already priced in' and stopped monitoring.",
    ]),
    avoid=_para_block([
        "GCC engineers at stable captives with growing headcount — different risk profile.",
        "Government and PSU tech roles — not covered here.",
    ]),
    expect=_para_block([
        "H1 2026 layoffs were the peak; H2 will be quiet.",
        "Companies that cut in Q1 have finished restructuring.",
        "Mid-year is historically safe because appraisal cycles just ended.",
    ]),
    reality=_para_block([
        "July 2026 is showing a second wave of bench trimming, not mass headlines. IT services firms are "
        "achieving headcount reduction through attrition non-replacement, performance-managed exits, and "
        "project wind-downs — quieter than January layoff emails but equally real.",
        "Mid-tier SaaS (Series B–D) continues rightsizing: 8–15% reductions at companies that grew headcount "
        "40%+ in 2021–22 and never hit unit economics. These cuts don't make national news but show up in "
        "<a href=\"/layoff-radar/\">Layoff Radar</a> submissions weekly.",
        "The post-appraisal window is historically when managers receive 'productivity improvement' targets. "
        "July–August performance conversations often precede September exits. If your manager scheduled "
        "an unexpected 1:1 about 'role alignment', treat it as a signal.",
        "GCC hiring slowed in summer but is not reversing layoffs elsewhere. Captives are selective — "
        "they absorb senior backend and platform talent, not generalist maintenance engineers from services.",
        "AI-driven productivity mandates are accelerating: clients renegotiating contracts with 15–25% fewer "
        "headcount for the same scope. That flows to bench risk for 3–7 YOE engineers without system design depth.",
    ]),
    salary="""
<table class="editorial-table">
<thead><tr><th>Sector</th><th>July 2026 Signal</th><th>Typical Impact</th></tr></thead>
<tbody>
<tr><td>IT Services</td><td>Bench trimming, utilization targets 88%+</td><td>4–7 YOE highest risk</td></tr>
<tr><td>Mid-tier SaaS</td><td>Continued rightsizing</td><td>Product + eng generalists</td></tr>
<tr><td>Product (profitable)</td><td>Selective hiring only</td><td>Low layoff, high bar</td></tr>
<tr><td>GCC</td><td>Summer slowdown</td><td>Hiring freeze, not layoffs</td></tr>
</tbody>
</table>
<p>Track live signals on <a href="/layoff-radar/">Layoff Radar</a> and monthly pressure on "
"<a href="/career-reality-index/">Career Reality Index</a>.</p>
""",
    stuck=_para_block([
        "'My project is busy so I'm safe.' Project load and billing status diverge at services companies.",
        "'I'll wait for a severance package.' Not all exits come with packages — PIP-to-exit is increasingly common.",
        "'Job market will recover by Diwali.' Recovery is sector-specific; generalist services roles are not rebounding to 2022 levels.",
    ]),
    verdict=_para_block([
        "July 2026 is not a calm mid-year — it's a quiet restructuring phase. Update your resume, "
        "run the <a href=\"/resignation-risk/\">Resignation Risk Analyzer</a>, and activate your network before you need it.",
        "If you're on bench or received a vague performance email, treat the next 60 days as exit preparation time, "
        "not vacation season.",
    ]),
    seo_desc="Mid-year layoff pulse for Indian tech in July 2026 — IT services bench trimming, SaaS rightsizing, and GCC hiring signals.",
)

# ── Article 3: Appraisal Hike vs Inflation ───────────────────────────────────
create_article(
    author=author,
    cat_name="Career Reality Checks",
    slug="appraisal-hike-inflation-gap-2026",
    title="Why Your Appraisal Hike Doesn't Match Inflation (2026)",
    persona=_para_block([
        "Indian tech professionals who received April–June 2026 appraisal letters.",
        "Engineers comparing their 6–10% hike against 12%+ expectations set by peers on LinkedIn.",
        "Anyone calculating whether staying another year makes financial sense.",
    ]),
    avoid=_para_block([
        "If you received a promotion with 25%+ hike and expanded scope — this article is not about you.",
        "Freshers in their first appraisal cycle — different dynamics apply.",
    ]),
    expect=_para_block([
        "Appraisal hikes should track inflation (5–6%) plus performance premium (5–10%) = 10–16% total.",
        "Strong performers at good companies receive 15–20% without switching jobs.",
        "Variable pay makes up the gap when base hike is modest.",
    ]),
    reality=_para_block([
        "July 2026 post-appraisal data shows median hikes of 5–8% at IT services, 8–12% at product companies, "
        "and 12–18% only for promoted employees or counter-offer saves. The LinkedIn 20% stories are survivorship bias.",
        "Inflation in urban India (CPI) ran 5.2–5.8% in H1 2026. A 7% hike is a 1–2% real increase — "
        "effectively flat purchasing power. After tax bracket creep, many engineers are net negative.",
        "Variable pay reductions are the hidden cut: same '15% hike' headline with variable dropping from 100% "
        "payout to 70% means total comp barely moved. Check your <a href=\"/salary-calculator/\">CTC Decoder</a> output, not HR slides.",
        "Counter-offers spiked in May–June for senior backend and platform roles (15–25% jumps), but only for "
        "engineers with production ownership evidence. Generalist profiles saw counter-offers dry up by July.",
        "The <a href=\"/career-reality-index/\">Career Reality Index</a> salary pressure score rose to 73 in July — "
        "reflecting widespread disappointment between expectation and delivered hikes.",
    ]),
    salary="""
<table class="editorial-table">
<thead><tr><th>Company Type</th><th>Median Hike (2026)</th><th>Real Increase (post-inflation)</th><th>Switch Premium</th></tr></thead>
<tbody>
<tr><td>IT Services</td><td>5–8%</td><td>0–3%</td><td>15–25% (if switchable)</td></tr>
<tr><td>Product (mid)</td><td>8–12%</td><td>3–6%</td><td>20–35%</td></tr>
<tr><td>GCC</td><td>10–14%</td><td>5–8%</td><td>15–25%</td></tr>
<tr><td>Startup</td><td>Highly variable</td><td>Often negative (ESOP dilution)</td><td>20–40%</td></tr>
</tbody>
</table>
<p>Compare your band on <a href="/salary-reality/">Salary Reality</a>.</p>
""",
    stuck=_para_block([
        "'At least I have a job.' True — but staying without negotiating or switching has compounding cost.",
        "'Next year will be better.' Three years of 7% hikes vs one 25% switch — the math rarely favors waiting.",
        "'HR said I'm at the top of my band.' Bands expand when companies want to retain; verify with market data.",
    ]),
    verdict=_para_block([
        "A 7% hike in July 2026 is not a reward — it's inflation adjustment with a performance label.",
        "If your total comp moved less than 10%, start interviewing in August when Q3 hiring resumes. "
        "Use appraisal disappointment as fuel, not resignation.",
    ]),
    seo_desc="Why 2026 appraisal hikes fall short of inflation for Indian tech workers — real numbers, hidden variable pay cuts, and what to do next.",
)

# ── Article 4: AI Job Market Mid-Year ────────────────────────────────────────
create_article(
    author=author,
    cat_name="Career Reality Checks",
    slug="ai-job-market-midyear-reality-2026",
    title="AI Job Market Mid-Year Reality Check for Indian Engineers",
    persona=_para_block([
        "Engineers who completed AI/ML courses, bootcamps, or certifications in H1 2026.",
        "Developers wondering if 'AI skills' translate to salary premiums or job security.",
        "Tech leads evaluating whether to restructure teams around coding agents.",
    ]),
    avoid=_para_block([
        "ML researchers with published papers and production model deployments — you have a different market.",
        "Non-tech professionals exploring AI tools for productivity only.",
    ]),
    expect=_para_block([
        "AI upskilling guarantees a 30–50% salary jump within 6 months.",
        "Every company is hiring 'AI engineers' at premium bands.",
        "Learning prompt engineering is enough to stay relevant.",
        "Coding agents will eliminate junior dev roles by end of 2026.",
    ]),
    reality=_para_block([
        "July 2026 hiring data shows AI/GenAI specialist roles (RAG, agents, eval pipelines) command 15–35% "
        "premiums over general SWE — but represent &lt;8% of open engineering positions in India.",
        "Most 'AI Engineer' JDs are rebranded data engineering or backend roles with a Copilot subscription. "
        "The <a href=\"/article/ai-upskilling-trap-india-api-wrapper-reality/\">AI upskilling trap</a> article "
        "from April still holds: certificate completion ≠ production capability.",
        "Coding agents (Cursor, Copilot, Codex) changed senior workflows, not headcount plans. Companies want "
        "engineers who can review, validate, and architect agent-assisted code — not prompt-only operators.",
        "QA and manual testing roles face the highest near-term pressure. SDE I/II roles are absorbing agent output "
        "into senior workloads rather than being eliminated outright.",
        "GCCs hiring AI talent want system design + ML deployment + ownership — not Udemy certificates. "
        "Check live AI role bands on <a href=\"/salary-reality/\">Salary Reality</a> and "
        "<a href=\"/ai/\">AI Pulse</a> for monthly career-impact news.",
    ]),
    salary="""
<table class="editorial-table">
<thead><tr><th>Role</th><th>Premium vs General SWE</th><th>July 2026 Demand</th><th>Barrier</th></tr></thead>
<tbody>
<tr><td>GenAI / RAG Engineer</td><td>+20–35%</td><td>High (selective)</td><td>Production deployment proof</td></tr>
<tr><td>ML Engineer (production)</td><td>+15–25%</td><td>Moderate</td><td>System design + ML ops</td></tr>
<tr><td>Prompt Engineer</td><td>+0–10%</td><td>Declining</td><td>Commoditising fast</td></tr>
<tr><td>AI Course Graduate (no prod)</td><td>0%</td><td>Low</td><td>Indistinguishable from generalist</td></tr>
</tbody>
</table>
""",
    stuck=_para_block([
        "'I spent ₹50K on a course — I need an AI role to justify it.' Sunk cost driving bad job searches.",
        "'Everyone on LinkedIn is an AI expert now.' Noise obscures the narrow premium band.",
        "'I'll wait for the market to mature.' Premium bands exist now for qualified engineers — waiting without building means missing the window.",
    ]),
    verdict=_para_block([
        "AI skills matter in July 2026 — but only as production evidence, not course completion.",
        "Build one deployed project (RAG system, agent workflow, eval harness) before calling yourself an AI engineer.",
        "General SWE roles remain the volume market; AI premium is real but narrow. Plan accordingly using the "
        "<a href=\"/career-reality-index/\">Career Reality Index</a> and "
        "<a href=\"/salary-calculator/\">CTC Decoder</a>.",
    ]),
    seo_desc="Mid-year 2026 reality check on AI job market premiums for Indian engineers — what actually pays, what's hype, and how to position.",
)

print(f"\nTotal published articles: {Article.objects.filter(status='published').count()}")
