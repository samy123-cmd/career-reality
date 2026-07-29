"""
Seed 4 late-July 2026 articles (published ~29 Jul 2026).
Same editorial structure as existing Career Reality pieces.

Run locally with DATABASE_URL:
  python seed_late_july_29_2026.py

Or import ARTICLES and apply via SQL / management command.
"""
from __future__ import annotations

import datetime
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

PUBLISHED = datetime.datetime(2026, 7, 29, 9, 0, 0, tzinfo=datetime.timezone.utc)
REALITY_CHECK = datetime.date(2026, 7, 29)


def _p(*paragraphs: str) -> str:
    return "".join(f"<p>{p}</p>" for p in paragraphs)


ARTICLES = [
    {
        "slug": "relieving-letter-hostage-notice-period-india-2026",
        "title": "The Relieving Letter Hostage: Why Notice Periods Still Trap Indian Engineers in 2026",
        "category_slug": "career-strategy",
        "category_name": "Career Strategy",
        "meta_title": "Relieving Letter Hostage India 2026 — Notice Period Reality",
        "meta_description": (
            "July 2026 reality check on notice periods, relieving letters, and bond pressure "
            "for Indian tech professionals — what HR can delay and how to protect yourself."
        ),
        "target_persona": _p(
            "IT services and mid-tier product engineers with 30–90 day notice periods who are mid-offer in July–August 2026.",
            "Anyone whose last employer is delaying a relieving letter, experience letter, or Form 16 handoff.",
            "Candidates stuck between a signed offer and a manager who 'needs two more months of transition.'",
        ),
        "who_should_avoid": _p(
            "If you already have your relieving letter and full & final settlement completed — this is archival.",
            "Government / PSU exits follow different statutes; this article covers private tech employers.",
        ),
        "common_expectation": _p(
            "Once you resign, the company must issue a relieving letter on your last working day.",
            "New employers will wait indefinitely for paperwork if you are otherwise strong.",
            "A long notice period (60–90 days) is 'industry standard' and non-negotiable.",
            "Bond clauses are rarely enforced if you negotiate politely.",
        ),
        "actual_reality": _p(
            "In July 2026, relieving-letter delays remain one of the top offer-breakers reported to "
            "<a href=\"/layoff-radar/\">Layoff Radar</a> adjacent community threads — not layoffs, but "
            "exit friction. HR can hold the letter while 'clearance' loops through IT asset return, "
            "knowledge transfer sign-off, and manager approval. None of that is always malicious; "
            "all of it is leverage.",
            "New employers increasingly set hard start-date cutoffs. A 90-day notice plus a two-week "
            "relieving delay means your August offer becomes a September problem — and many GCCs will "
            "cancel rather than re-open a requisition.",
            "Buyouts are real but uneven: product companies and GCCs often accept notice buyouts "
            "(you or they pay for remaining days). IT services firms still treat 90-day notice as a "
            "bench-protection tool. Run the <a href=\"/resignation-risk/\">Resignation Risk Analyzer</a> "
            "before you resign — bond + notice + variable clawback stack differently by employer type.",
            "WhatsApp 'HR will ruin you' folklore is mostly wrong. What is true: incomplete relieving "
            "documentation blocks background verification at banks, captives, and larger product firms. "
            "Email trails matter more than hallway conversations.",
            "July–August is peak lateral movement after appraisal disappointment. That means HR teams "
            "are overloaded and clearance queues are slower — plan paperwork 2–3 weeks earlier than "
            "you think you need.",
        ),
        "salary_reality": """
<table class="editorial-table">
<thead><tr><th>Employer Type</th><th>Typical Notice</th><th>Buyout Likelihood</th><th>Relieving Delay Risk</th></tr></thead>
<tbody>
<tr><td>IT Services</td><td>60–90 days</td><td>Low–Medium</td><td>High if manager blocks KT</td></tr>
<tr><td>Mid-tier SaaS</td><td>30–60 days</td><td>Medium</td><td>Medium</td></tr>
<tr><td>Product (profitable)</td><td>30–60 days</td><td>High</td><td>Low–Medium</td></tr>
<tr><td>GCC / Captive</td><td>60–90 days</td><td>Medium–High</td><td>Medium (BGV strict)</td></tr>
</tbody>
</table>
<p>July 2026 patterns. Validate your offer timeline with the <a href="/salary-calculator/">CTC Decoder</a> and resignation timing tools before you sign.</p>
""",
        "stuck_point": _p(
            "'I'll resign after the new offer letter is in hand' — correct — but also get written start-date flexibility for paperwork delay.",
            "'My manager likes me so clearance will be fine' — managers rotate; email the exit checklist to HR the week you resign.",
            "'Bond is illegal so I can ignore it' — civil recovery risk still exists; get numbers from the <a href=\"/resignation-risk/\">Resignation Risk Analyzer</a>.",
        ),
        "verdict": _p(
            "Treat the relieving letter as a project with owners, dates, and escalation — not a courtesy HR 'will handle.'",
            "In July 2026's post-appraisal switch wave, paperwork friction is rising faster than hiring intent. "
            "Protect your start date in writing, document every clearance step, and do not resign until "
            "buyout / notice math is clear.",
        ),
    },
    {
        "slug": "gcc-return-to-office-hybrid-reality-india-2026",
        "title": "GCC Return-to-Office Reality: Hybrid Promises vs Desk Mandates in Mid-2026",
        "category_slug": "career-reality-checks",
        "category_name": "Career Reality Checks",
        "meta_title": "GCC Return-to-Office India 2026 — Hybrid vs Mandate",
        "meta_description": (
            "Mid-2026 reality check on GCC and captive return-to-office rules in India — "
            "what 'hybrid' means, who is exempt, and how it changes offer decisions."
        ),
        "target_persona": _p(
            "Engineers evaluating GCC offers in Bengaluru, Hyderabad, Pune, and Chennai in July–August 2026.",
            "Current captive employees told 'hybrid continues' while badge data shows three–four days in office.",
            "Parents and spouses planning city moves around a GCC role that may not stay remote-friendly.",
        ),
        "who_should_avoid": _p(
            "Fully onsite manufacturing / plant IT roles — different constraints.",
            "US-remote contractors paid in USD — this article covers India-entity GCC employment.",
        ),
        "common_expectation": _p(
            "GCCs copied Silicon Valley hybrid forever after 2022.",
            "Badge compliance is soft; managers will protect high performers from RTO.",
            "Remote-first offers from captives are still common for senior ICs.",
            "RTO is temporary 'team building' then reverts.",
        ),
        "actual_reality": _p(
            "By late July 2026, most large GCCs in India have settled into <strong>3–4 days in office</strong> "
            "as the real policy — even when careers pages still say 'flexible hybrid.' Badge analytics and "
            "facilities utilization, not culture decks, drive enforcement.",
            "Exemptions exist for caregiving, disability, and rare specialist roles — not for 'I am more "
            "productive at home' without documentation. High performers get temporary exceptions; they "
            "rarely get permanent remote contracts at captives.",
            "Offer letters increasingly include location clauses and hybrid schedules as contractual, not "
            "informal. Renegotiating after joining is harder than negotiating before signing. Compare "
            "total cost of commute + rent against the <a href=\"/salary-reality/\">Salary Reality</a> "
            "band for that city.",
            "The <a href=\"/article/gcc-gold-rush-india-captive-center-reality/\">GCC gold rush</a> still "
            "pays a premium over IT services — but the premium now buys less lifestyle flexibility than "
            "2023–24 offers implied. Factor RTO into the real raise when you use the "
            "<a href=\"/salary-calculator/\">CTC Decoder</a>.",
            "Startups and mid-tier SaaS remain more flexible on paper; GCCs are converging toward "
            "parent-company global attendance norms. July hiring freezes in some captives also mean "
            "less leverage to negotiate remote exceptions.",
        ),
        "salary_reality": """
<table class="editorial-table">
<thead><tr><th>Policy Label</th><th>What It Usually Means (Jul 2026)</th><th>Negotiation Room</th></tr></thead>
<tbody>
<tr><td>"Flexible hybrid"</td><td>3–4 days office, manager discretion</td><td>Low after joining</td></tr>
<tr><td>"Hybrid 2–3 days"</td><td>Often drifts to 3+ within 2 quarters</td><td>Medium at offer stage</td></tr>
<tr><td>"Office-first"</td><td>4–5 days; WFH needs approval</td><td>Low</td></tr>
<tr><td>"Remote-eligible"</td><td>Rare; usually specialist / legacy</td><td>Role-specific</td></tr>
</tbody>
</table>
<p>Track market pressure on the <a href="/career-reality-index/">Career Reality Index</a> when weighing a city move for a GCC seat.</p>
""",
        "stuck_point": _p(
            "'The recruiter said hybrid' — get days-per-week in the offer letter, not a Slack promise.",
            "'I'll accept and renegotiate later' — badge culture hardens after facilities spend is committed.",
            "'RTO will reverse when hiring gets hard again' — captives can stay selective without going fully remote.",
        ),
        "verdict": _p(
            "Price the commute. A 20% GCC raise that costs 10 hours/week and a rent bump can be a real-terms wash.",
            "In mid-2026, treat RTO policy as part of compensation. Negotiate before you sign, document the "
            "hybrid schedule, and do not plan your family's geography on a careers-page slogan.",
        ),
    },
    {
        "slug": "staff-engineer-promotion-freeze-india-2026",
        "title": "The Staff Engineer Freeze: Why IC Promotions Stalled in Indian Tech (2026)",
        "category_slug": "software-engineering",
        "category_name": "Software Engineering",
        "meta_title": "Staff Engineer Promotion Freeze India 2026",
        "meta_description": (
            "Why Staff+ IC promotions slowed in Indian product companies and GCCs in 2026 — "
            "leveling bars, scope evidence, and what to do if you are stuck at Senior."
        ),
        "target_persona": _p(
            "Senior engineers (5–9 YOE) told they are 'almost Staff' for the second or third cycle.",
            "ICs comparing Manager-track pressure against a frozen Staff ladder in July 2026.",
            "Engineers who shipped features all year but lack org-level scope narratives.",
        ),
        "who_should_avoid": _p(
            "If you were promoted to Staff/Principal in the last 12 months — congratulations; this is context, not advice.",
            "Pure people-managers evaluating eng manager bands — see Manager vs IC coverage instead.",
        ),
        "common_expectation": _p(
            "Strong delivery for 18 months automatically unlocks Staff.",
            "Staff is mostly a title bump with a 15–20% hike.",
            "Every product company has a healthy Staff ratio like FAANG blogs describe.",
            "Switching companies is the reliable path to Staff if internal promo is slow.",
        ),
        "actual_reality": _p(
            "Late-2025 through July 2026, many Indian product companies and GCCs quietly raised the "
            "Staff bar: cross-team technical strategy, multi-quarter roadmaps, and measurable org leverage "
            "— not 'I closed 40 tickets.' Calibration committees are rejecting Senior→Staff packets that "
            "would have passed in 2022.",
            "Headcount freezes mean fewer Staff slots even when individuals are ready. Promo budgets "
            "shifted to retention counters for flight-risk seniors, not level expansions. That shows up "
            "as 'exceeds expectations' ratings without title change.",
            "External Staff offers exist but interview loops now probe system design + incident leadership "
            "+ stakeholder influence. Title inflation at startups ('Staff at 4 YOE') is discounted by "
            "GCCs and larger product firms — they re-level on the way in.",
            "The <a href=\"/article/senior-developer-salary-ceiling-india/\">senior developer ceiling</a> "
            "still holds: without Staff scope, compensation compresses near ₹35–45 LPA in many Bengaluru "
            "product bands. Check live medians on <a href=\"/salary-reality/\">Salary Reality</a>.",
            "Manager-track pressure increases when IC promo freezes — not because you want to manage, "
            "but because that is where the open slots are. Choosing management without desire is a "
            "career trap; read <a href=\"/article/manager-vs-ic-career-path-india/\">Manager vs IC</a> first.",
        ),
        "salary_reality": """
<table class="editorial-table">
<thead><tr><th>Level</th><th>Bengaluru Product Median</th><th>GCC Median</th><th>July 2026 Promo Odds*</th></tr></thead>
<tbody>
<tr><td>Senior (L5-ish)</td><td>₹28–40 LPA</td><td>₹26–38 LPA</td><td>Baseline</td></tr>
<tr><td>Staff (L6-ish)</td><td>₹42–60 LPA</td><td>₹38–55 LPA</td><td>Selective / slot-limited</td></tr>
<tr><td>External Staff hire</td><td>+10–20% vs internal</td><td>+5–15%</td><td>Re-level risk high</td></tr>
</tbody>
</table>
<p>*Illustrative mid-2026. Use the <a href="/salary-calculator/">CTC Decoder</a> on offers; variable and joining bonus distort headlines.</p>
""",
        "stuck_point": _p(
            "'My manager said next cycle' for three cycles — ask for written leveling gaps, not vibes.",
            "'I'll wait; switching is risky' — waiting without building Staff-scope evidence freezes you longer.",
            "'I'll take the EM role for the hike' — title change without interest is how tech leads burn out.",
        ),
        "verdict": _p(
            "Staff in 2026 is a scope problem more than a loyalty problem. Document org-level impact, "
            "seek projects with multi-team blast radius, or switch only when you can prove that scope.",
            "If your company froze Staff slots, do not invent a passion for management. Negotiate scope, "
            "comp, or exit — with eyes open.",
        ),
    },
    {
        "slug": "joining-bonus-clawback-offer-letter-traps-2026",
        "title": "Joining Bonus Clawbacks: The Offer Letter Trap Indian Engineers Miss in 2026",
        "category_slug": "money-reality",
        "category_name": "Money Reality",
        "meta_title": "Joining Bonus Clawback India 2026 — Offer Letter Traps",
        "meta_description": (
            "How joining bonuses, retention bonuses, and clawback clauses work in Indian tech offers "
            "in 2026 — real numbers, exit risk, and how to decode the letter."
        ),
        "target_persona": _p(
            "Engineers comparing July–August 2026 offers that look rich because of a ₹2–6 L joining bonus.",
            "Anyone planning to switch again within 12–18 months after accepting a clawback-heavy package.",
            "Candidates who treat 'CTC' as spendable income without reading annexures.",
        ),
        "who_should_avoid": _p(
            "If your offer has zero joining/retention bonus and simple fixed pay — still read once, then move on.",
            "ESOP-only startup packages — different dilution math; see ESOP reality coverage.",
        ),
        "common_expectation": _p(
            "Joining bonus is free money for signing.",
            "Clawbacks are rare and only apply if you are fired for cause.",
            "Leaving after 11 months is safe if the clawback says 12 months — companies will not chase.",
            "CTC including joining bonus is the right number for lifestyle planning.",
        ),
        "actual_reality": _p(
            "In mid-2026, joining bonuses are back as a hiring tool after appraisal-season talent flight — "
            "especially for backend, platform, and GenAI-adjacent roles. The catch is standard: "
            "<strong>pro-rata clawback for 12–24 months</strong> if you resign (sometimes even if laid off "
            "in certain wordings — read carefully).",
            "A ₹4 L joining bonus on an 18-month clawback is not ₹4 L of wealth. Leave at month 9 and "
            "you may owe roughly half, often recovered from full & final or via legal notice. That "
            "interacts badly with relieving-letter delays — see our "
            "<a href=\"/article/relieving-letter-hostage-notice-period-india-2026/\">relieving letter</a> piece.",
            "Offers advertise '₹32 LPA' when ₹4 L is one-time bonus and ₹3 L is annual variable at 70% "
            "historical payout. First-year spendable income can be closer to a ₹24–26 LPA fixed story. "
            "Always run the <a href=\"/salary-calculator/\">CTC Decoder</a> and ask for fixed vs variable vs bonus split in writing.",
            "Retention bonuses paid at month 12 are also rising at GCCs. Missing the date by resigning "
            "at month 11 is a classic self-own. Calendar the cliff before you accept.",
            "Compare bands on <a href=\"/salary-reality/\">Salary Reality</a> using <em>fixed + expected variable</em>, "
            "not headline CTC. Bonus-heavy packages look competitive in screenshots and weak in month-13 reality.",
        ),
        "salary_reality": """
<table class="editorial-table">
<thead><tr><th>Offer Shape</th><th>Headline CTC</th><th>Year-1 Reliable</th><th>Clawback Risk</th></tr></thead>
<tbody>
<tr><td>Fixed-heavy</td><td>₹24 LPA</td><td>~₹22–23 L effective</td><td>Low</td></tr>
<tr><td>Fixed + ₹3L join bonus (12 mo)</td><td>₹27 LPA advertised</td><td>~₹24 L if you stay</td><td>Medium</td></tr>
<tr><td>Fixed + ₹5L join (24 mo) + high variable</td><td>₹35 LPA advertised</td><td>Often ₹26–29 L</td><td>High if early exit</td></tr>
</tbody>
</table>
<p>Illustrative July 2026 structures. Decode every annexure before you celebrate on LinkedIn.</p>
""",
        "stuck_point": _p(
            "'HR said clawback is never enforced' — get that in writing or assume it is enforced.",
            "'I'll stay one year then switch' — calendar the clawback end date; companies know this pattern.",
            "'Bonus covers my notice buyout' — only if it is not clawed back when you resign to leave.",
        ),
        "verdict": _p(
            "Treat joining bonus as a loan secured against your tenure — not a gift.",
            "In 2026's competitive mid-year market, flashy CTC is a screening weapon. Optimize for "
            "fixed pay, expected variable, and clawback length — then sign.",
        ),
    },
]


def main():
    import django

    django.setup()
    from content.models import Article, Author, Category

    author = Author.objects.filter(is_active=True).order_by("id").first()
    if not author:
        raise SystemExit("No active author found")

    for data in ARTICLES:
        category, _ = Category.objects.get_or_create(
            slug=data["category_slug"],
            defaults={"name": data["category_name"], "order": 1},
        )
        article, created = Article.objects.update_or_create(
            slug=data["slug"],
            defaults={
                "title": data["title"],
                "author": author,
                "category": category,
                "status": "published",
                "target_persona": data["target_persona"],
                "who_should_avoid": data["who_should_avoid"],
                "common_expectation": data["common_expectation"],
                "actual_reality": data["actual_reality"],
                "salary_reality": data["salary_reality"],
                "stuck_point": data["stuck_point"],
                "verdict": data["verdict"],
                "meta_title": data["meta_title"][:60],
                "meta_description": data["meta_description"][:160],
                "published_at": PUBLISHED,
                "last_reality_check": REALITY_CHECK,
            },
        )
        print(f"{'Created' if created else 'Updated'}: {article.slug}")

    print(f"Published total: {Article.objects.filter(status='published').count()}")


if __name__ == "__main__":
    main()
