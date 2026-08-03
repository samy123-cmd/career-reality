"""
Seed 3 August 2026 long-form articles:
  1. Cybersecurity & Privacy Careers Beyond Tech
  2. Green Careers: ESG, Renewable Energy & Sustainability
  3. Portfolio-First Hiring & Gig Economy Careers

Run: python seed_august_2026.py
"""
from __future__ import annotations

import datetime
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

PUBLISHED = datetime.datetime(2026, 8, 3, 9, 0, 0, tzinfo=datetime.timezone.utc)
REALITY_CHECK = datetime.date(2026, 8, 3)


def _p(*paragraphs: str) -> str:
    return "".join(f"<p>{p}</p>" for p in paragraphs)


def _h3(title: str) -> str:
    return f"<h3>{title}</h3>"


def _section(title: str, *paragraphs: str) -> str:
    return _h3(title) + _p(*paragraphs)


ARTICLES = [
    # ── 1. Cybersecurity & Privacy Beyond Tech ───────────────────────────────
    {
        "slug": "cybersecurity-privacy-careers-beyond-tech-india-2026",
        "title": "Cybersecurity & Privacy Careers Beyond Tech: The GRC Surge India Can't Ignore in 2026",
        "category_slug": "career-reality-checks",
        "category_name": "Career Reality Checks",
        "meta_title": "Cybersecurity Jobs India 2026 — GRC & Privacy Beyond Tech",
        "meta_description": (
            "August 2026 reality check on cybersecurity jobs India 2026: GRC careers, "
            "cloud security specialists, privacy analysts, and non-tech sector hiring."
        ),
        "target_persona": _p(
            "IT professionals in India considering a pivot into cybersecurity, GRC, or privacy "
            "roles in August 2026 — especially those tired of pure coding tracks or IT-services delivery.",
            "Risk, audit, legal, and operations professionals in BFSI, healthcare, manufacturing, "
            "and telecom who keep seeing 'cybersecurity' and 'DPDP' in job descriptions.",
            "Career switchers chasing cybersecurity jobs India 2026 after bootcamps or CompTIA/CISSP "
            "prep, unsure whether SOC analyst, GRC analyst, or privacy analyst is the real demand.",
        ),
        "who_should_avoid": _p(
            "If you already hold a senior cloud security architect seat at a product company or GCC "
            "with production ownership — this is context, not a career alarm.",
            "Pure offensive-security researchers with published CVEs and red-team retainers operate "
            "in a different market; this piece focuses on GRC, privacy, and industry cyber talent.",
            "Anyone expecting a six-week certification to replace domain fluency in banking, hospitals, "
            "or plant OT environments will waste money — skip the fantasy, not the article.",
        ),
        "common_expectation": _p(
            "Cybersecurity careers live only inside tech product companies and Big Four 'cyber' practices.",
            "A Security+ or CEH certificate plus LinkedIn keyword stuffing is enough to land cybersecurity "
            "jobs India 2026 at ₹20 LPA.",
            "GRC is soft paperwork — less prestigious and lower-paid than 'real' hacking or SOC work.",
            "Privacy analyst roles are niche legal jobs; engineers need not apply.",
            "Non-tech industries (hospitals, factories, insurers) hire cyber talent only for IT helpdesk "
            "and antivirus admin — nothing strategic.",
        ),
        "actual_reality": (
            _p(
                "By August 2026, the sharpest growth in cybersecurity jobs India 2026 is not another "
                "Bengaluru SOC night shift. It is Governance, Risk, and Compliance (GRC), cloud security "
                "specialists embedded in regulated industries, and privacy analysts who can translate "
                "India's Digital Personal Data Protection (DPDP) Act into product and vendor decisions. "
                "Tech still pays well — but BFSI, healthcare, manufacturing, energy, and telecom are "
                "competing for the same scarce mid-level talent, often with clearer mandates and less "
                "title inflation.",
                "Global context matters: ransomware against hospitals and logistics firms, EU AI Act "
                "adjacent controls, and US SEC cyber disclosure norms have pushed boards to fund "
                "security as business risk — not as an IT ticket queue. India mirrors that shift with "
                "a local twist: DPDP enforcement timelines, RBI IT and cyber guidelines for banks and "
                "NBFCs, IRDAI expectations for insurers, and CERT-In reporting habits. Career reality: "
                "the people who win are bilingual — technical enough to challenge a vendor, and "
                "business-fluent enough to brief a CRO.",
            )
            + _section(
                "The Rise of GRC Roles",
                "GRC careers India 2026 are absorbing professionals from audit, quality, IT risk, and "
                "even mid-level developers who prefer control design over on-call. A GRC analyst owns "
                "policy frameworks, control testing, vendor risk questionnaires, evidence packs for "
                "ISO 27001 / SOC 2 / PCI DSS, and board-facing risk registers. It is not 'soft' work. "
                "Poor GRC writing loses deals; strong GRC writing unlocks enterprise sales and regulator "
                "patience.",
                "Hiring managers in August 2026 repeatedly say the same thing in community threads "
                "adjacent to <a href=\"/layoff-radar/\">Layoff Radar</a>: they can find junior SOC "
                "analysts who escalate alerts; they cannot find mid-level GRC people who map a control "
                "to a business process and survive an external audit without panic. That scarcity shows "
                "up in salary bands that now rival many application-security engineer packages outside "
                "top product firms.",
                "Typical GRC entry paths: internal audit → IT risk → GRC analyst; quality / ISO "
                "coordinator → information security management; backend engineer → security champion → "
                "GRC with technical depth. Bootcamp-only candidates without evidence of a real control "
                "cycle (plan → implement → test → remediate) stall at HR screens.",
            )
            + _section(
                "Cloud Security Specialists: Demand Across Industries",
                "Cloud security specialist roles exploded because 'we moved to AWS/Azure' without "
                "identity hygiene. In India, captives and mid-market firms now ask for IAM design, "
                "CSPM tooling, Kubernetes hardening, and shared-responsibility literacy — not just "
                "firewall rules. Banks' cloud migration programs and insurer core-modernisation "
                "projects create multi-year demand for people who can read a Terraform plan and a "
                "regulator circular in the same week.",
                "Compare this with generic DevOps: DevOps/SRE on-call culture is brutal (see "
                "<a href=\"/article/devops-sre-reality-india-oncall/\">DevOps SRE Reality</a>). Cloud "
                "security specialists often sit closer to architecture and risk committees. The trade: "
                "you must stay current on misconfiguration classes and identity attacks. The upside: "
                "your work is measured by reduced blast radius, not ticket velocity alone.",
                "August 2026 pattern: GCCs hire cloud security for parent-company standards; Indian "
                "product SaaS firms hire for customer trust questionnaires; manufacturing and energy "
                "firms hire to connect OT/IT boundaries after high-profile global OT incidents. "
                "Geography still clusters around Bengaluru, Hyderabad, Pune, Mumbai, and Gurgaon — "
                "but remote-India contracts appear when niche cloud-security depth is scarce.",
            )
            + _section(
                "Privacy Analysts After DPDP",
                "Privacy analyst jobs are no longer a niche for law-firm associates. Product companies, "
                "fintechs, edtech platforms, and healthcare chains need people who can run DPIA-style "
                "assessments, map data flows, negotiate processor contracts, and explain consent "
                "UX to engineering. Global peers (GDPR veterans) set the playbook; Indian privacy "
                "analysts adapt it to DPDP rules, sectoral overlays, and cross-border transfer "
                "practicalities.",
                "Engineers who can read API logs and also write a readable privacy impact note are "
                "over-indexed in offers. Pure legal profiles without systems curiosity struggle when "
                "asked how a marketing SDK actually ships data. Pure engineers without stakeholder "
                "patience struggle when legal and marketing disagree. The winning privacy analyst "
                "is a translator — similar to the best product managers, minus the Jira theatre "
                "(see <a href=\"/article/product-manager-reality-india-jira-janitor/\">PM Reality</a>).",
            )
            + _section(
                "Case Study: BFSI — Banks and NBFCs",
                "A mid-sized private bank in Mumbai rebuilt its cyber hiring slate in 2025–26 after "
                "regulator observations on third-party risk. Instead of only expanding the SOC, it "
                "hired two GRC leads for vendor oversight, one cloud security specialist for hybrid "
                "core migration, and a privacy analyst shared with the digital products group. "
                "Comp for the GRC leads landed near senior backend bands for 7–9 YOE — not because "
                "of hacking glory, but because failed audits threaten business continuity.",
                "NBFCs and fintechs show a parallel: appsec still matters, but the board pack now "
                "asks about DPDP readiness and cloud shared-responsibility evidence. Candidates who "
                "only list tools (Qualys, Nessus, Splunk) without naming a control outcome lose to "
                "candidates who can narrate a closed risk.",
            )
            + _section(
                "Case Study: Healthcare and Hospitals",
                "Hospital groups and diagnostic chains in India accelerated cybersecurity hiring after "
                "global hospital ransomware waves and local digitisation of patient records. A "
                "multi-city hospital network in South India hired a privacy analyst and a GRC "
                "coordinator before hiring another penetration tester — because EHR vendor contracts "
                "and patient-consent workflows were the weak points auditors flagged first.",
                "Clinical engineering and biomedical IT staff are being upskilled into OT-adjacent "
                "security for connected devices. Career lesson: domain fluency (how a hospital "
                "actually runs) beats a generic 'ethical hacking' certificate when the asset is a "
                "ventilator network segment, not a CTF challenge.",
            )
            + _section(
                "Case Study: Manufacturing, Energy, and Telecom",
                "Manufacturing exporters chasing EU customer security questionnaires now staff "
                "information-security managers who speak both ISO and shop-floor reality. Energy and "
                "utilities firms blend IT security with OT consultants; telecom operators combine "
                "privacy, lawful-intercept compliance, and cloud security for 5G and edge workloads.",
                "These employers rarely post on the same LinkedIn hashtags as 'cybersecurity jobs "
                "India 2026' influencers. They hire through specialist recruiters, Big Four alumni "
                "networks, and internal risk rotations. If your job search only watches product-startup "
                "boards, you are sampling the wrong market.",
            )
            + _section(
                "Skills Reality vs Certificate Theatre",
                "Certificates help HR parse keywords. They do not replace evidence. Strong portfolios "
                "for GRC/privacy/cloud security include: a sample control matrix, a redacted vendor "
                "risk memo, a cloud misconfiguration postmortem write-up, or a privacy data-flow "
                "diagram for a fictional product. That is closer to "
                "<a href=\"/article/portfolio-first-hiring-gig-economy-careers-india-2026/\">portfolio-first hiring</a> "
                "than to collecting badges.",
                "Avoid the trap documented in "
                "<a href=\"/article/self-learning-trap-online-courses-expensive-entertainment/\">online courses reality</a>: "
                " bingeing cyber MOOCs without shipping a control cycle. Also avoid "
                "<a href=\"/article/ai-upskilling-trap-india-api-wrapper-reality/\">AI upskilling theatre</a> "
                "dressed as 'AI for cyber' — employers want threat judgment, not chatbot demos.",
            )
            + _section(
                "Global Demand Signals Meeting Indian Hiring",
                "NIST CSF updates, ISO 27001:2022 transitions, and insurer underwriting questionnaires "
                "have standardised what 'good enough' security evidence looks like for mid-market firms. "
                "Indian employers importing those norms — especially exporters and GCCs — now write "
                "job descriptions that would have been rare in 2022: continuous control monitoring, "
                "third-party risk orchestration, and privacy-by-design reviews tied to release gates.",
                "For candidates, that means interview loops increasingly include a mini case: map a "
                "risk, propose a control, estimate residual risk, and brief a non-technical stakeholder. "
                "Practise that narrative. Tool names without a stakeholder story fail. Conversely, "
                "audit veterans who learn cloud identity basics suddenly become competitive for hybrid "
                "GRC-cloud roles that pure hackers ignore.",
                "August 2026 also shows more contract-to-hire GRC and privacy seats as companies test "
                "fit before opening permanent headcount. Treat those as portfolio opportunities: deliver "
                "a clean evidence pack or DPIA template set, then convert. The same dynamic appears in "
                "<a href=\"/article/portfolio-first-hiring-gig-economy-careers-india-2026/\">portfolio-first hiring</a> "
                "across design and marketing — cyber is catching up.",
            )
            + _section(
                "Career Sequencing Advice for Switchers",
                "If you are exiting IT services delivery, do not leap straight to 'Chief Information "
                "Security Officer' fantasies. Sequence: (1) own a control family end-to-end inside your "
                "current employer if possible; (2) publish a redacted write-up; (3) target analyst roles "
                "in regulated industries; (4) specialise toward cloud security or privacy after twelve "
                "months of evidence. Skipping steps produces resume spam and interview fatigue.",
                "If you are already in SOC, negotiate for project time on detection content or "
                "control testing — that creates the bridge out of shift work. If you are in legal or "
                "compliance, pair with an engineer mentor for one product data-flow map. Bilingual "
                "proof compounds faster than solitary certificate grinding.",
            )
        ),
        "salary_reality": """
<h3>Salary and Growth Bands — Cybersecurity Jobs India 2026</h3>
<p>Medians vary by city and employer type. Use the <a href="/salary-calculator/">CTC Decoder</a> for in-hand math and compare against <a href="/salary-reality/">Salary Reality</a> engineering bands — GRC and privacy often sit between audit and senior engineering packages.</p>
<table class="editorial-table">
<thead><tr><th>Role</th><th>Experience</th><th>Bengaluru / Hyderabad</th><th>Mumbai / Gurgaon (BFSI tilt)</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>SOC Analyst L1–L2</td><td>0–3 YOE</td><td>5–10 LPA</td><td>6–11 LPA</td><td>High burnout; night shifts common</td></tr>
<tr><td>GRC Analyst</td><td>2–5 YOE</td><td>9–16 LPA</td><td>10–18 LPA</td><td>Audit/ISO evidence valued</td></tr>
<tr><td>Privacy Analyst</td><td>3–6 YOE</td><td>12–20 LPA</td><td>14–24 LPA</td><td>DPDP + product fluency premium</td></tr>
<tr><td>Cloud Security Specialist</td><td>4–8 YOE</td><td>18–32 LPA</td><td>20–34 LPA</td><td>IAM + CSPM + K8s hardening</td></tr>
<tr><td>GRC / InfoSec Manager</td><td>7–12 YOE</td><td>24–40 LPA</td><td>26–45 LPA</td><td>Board reporting + vendor risk</td></tr>
<tr><td>AppSec / SecEng (product)</td><td>4–8 YOE</td><td>20–36 LPA</td><td>18–32 LPA</td><td>Still strong; competitive with cloud sec</td></tr>
</tbody>
</table>
<p><em>August 2026 editorial ranges. Variable pay and joining bonuses distort headlines — decode clawbacks before you celebrate.</em></p>
<h3>Growth Pattern</h3>
<p>SOC → specialised detection engineering or exit to GRC/cloud security is a common escape from shift work. GRC analyst → GRC manager → Head of InfoSec Risk is a viable non-coding ladder. Privacy analysts can move into product counsel partnerships or Chief Privacy Officer tracks in larger groups. Cloud security specialists who learn threat modelling become security architects — often higher leverage than title-chasing in pure AppSec.</p>
<p>Compare total comp carefully against <a href="/article/what-20-lpa-actually-feels-like-india-purchasing-power/">what ₹20 LPA feels like</a> and metro cost of living. A ₹22 LPA GRC role in Mumbai with predictable hours can beat a ₹28 LPA SOC lead with rotating nights on real quality-of-life math.</p>
""",
        "stuck_point": _p(
            "'I'll do CEH and apply to every cyber posting' — without a control story or cloud lab "
            "evidence, you join the reject pile for cybersecurity jobs India 2026.",
            "'GRC is boring so I'll wait for red team' — red-team seats are rare; GRC seats are hiring "
            "now across BFSI and healthcare.",
            "'I'm from IT services so non-tech industries won't want me' — they often prefer your "
            "client-audit scars if you can reframe them as risk ownership.",
            "'Privacy is only for lawyers' — product and data engineers with DPDP literacy are "
            "explicitly shortlisted in August 2026 fintech and health-tech loops.",
            "'Night SOC is temporary' — temporary becomes three years; plan the exit skill before "
            "burnout plans it for you (see <a href=\"/article/work-life-balance-myth-high-performers/\">work-life balance myth</a>).",
        ),
        "verdict": _p(
            "Cybersecurity careers beyond tech are not a consolation prize — they are where regulation, "
            "cloud migration, and privacy law are forcing real budgets in August 2026.",
            "If you want durable cybersecurity jobs India 2026, build bilingual proof: one technical "
            "artifact (cloud hardening note, detection rule, data-flow map) and one governance artifact "
            "(control matrix, vendor risk memo, privacy assessment). That portfolio beats certificate "
            "stacks.",
            "GRC careers India, cloud security specialists, and privacy analysts will keep absorbing "
            "talent from both engineering and risk backgrounds. Choose the lane that matches how you "
            "like to work — then verify the mandate is real, not greenwashed 'cyber' branding on an "
            "IT admin job.",
        ),
    },
    # ── 2. Green Careers ESG / Renewables ────────────────────────────────────
    {
        "slug": "green-careers-esg-renewable-sustainability-india-2026",
        "title": "Green Careers in India 2026: ESG Analysts, Carbon Accounting & Renewable Reality",
        "category_slug": "career-strategy",
        "category_name": "Career Strategy",
        "meta_title": "Sustainability Careers India 2026 — ESG & Renewables",
        "meta_description": (
            "August 2026 guide to sustainability careers India: ESG analyst jobs, carbon accounting, "
            "renewable energy engineers, EV/solar case studies, and consulting paths."
        ),
        "target_persona": _p(
            "Engineers, finance analysts, and consultants in India exploring sustainability careers "
            "India in August 2026 — ESG analyst jobs, carbon accounting, or renewable energy engineering.",
            "MBA and CA/CS professionals weighing corporate ESG initiatives against traditional "
            "finance or strategy tracks.",
            "Mechanical, electrical, and civil engineers eyeing solar, wind, storage, and EV "
            "manufacturing roles amid India's clean-energy build-out.",
        ),
        "who_should_avoid": _p(
            "If you already lead a funded decarbonisation programme with P&L ownership — use this as "
            "market context, not a beginner map.",
            "Skip if you want 'green' only as LinkedIn branding without learning measurement standards "
            "(GHG Protocol, BRSR, ISSB-aligned disclosures).",
            "Pure activism careers and grassroots NGO paths matter — but they follow different funding "
            "and risk models than the corporate/consulting market covered here.",
        ),
        "common_expectation": _p(
            "Sustainability careers India are niche CSR jobs writing annual report paragraphs.",
            "Any MBA can become an ESG analyst after one certificate; technical depth is optional.",
            "Renewable energy engineer roles pay like FAANG and hire as fast as IT services campus drives.",
            "Carbon accounting is just Excel with 'Scope 3' labels — accountants already know it.",
            "India's EV and solar boom guarantees safe, high-growth jobs for anyone who pivots in 2026.",
        ),
        "actual_reality": (
            _p(
                "August 2026 sustainability careers India sit at the intersection of policy, analytics, "
                "engineering, and capital markets — not at the intersection of buzzwords and tree-planting "
                "days. Corporate ESG initiatives are now driven by BRSR Core disclosures for listed "
                "entities, lender questionnaires, export-market carbon expectations, and investor diligence. "
                "That creates real seats for ESG analysts, carbon accounting specialists, renewable energy "
                "engineers, and sustainability consultants. It also creates title inflation: many 'ESG "
                "executive' postings are still CSR coordination with a new hashtag.",
                "Globally, Europe's CSRD wave and US state/climate disclosure experiments raised the "
                "bar for assurance-ready data. India is not copying Europe line-for-line, but exporters "
                "and GCCs feel the pressure through supply-chain questionnaires. Career reality: the "
                "people who win can measure, explain uncertainty, and connect emissions data to "
                "capex decisions — not only to LinkedIn carousels.",
            )
            + _section(
                "Carbon Accounting: The Measurement Jobs",
                "Carbon accounting careers start where inventory quality starts. Scope 1 and 2 are "
                "increasingly standardised for large industrials; Scope 3 (suppliers, logistics, "
                "product use) is where the pain — and the hiring — lives. Specialists clean activity "
                "data, choose emission factors, document assumptions, and prepare packs for limited "
                "assurance. This looks more like financial close discipline than activism.",
                "Who thrives: CA/CMA profiles who learn GHG Protocol; chemical/mechanical engineers "
                "who understand process data; data analysts who can build repeatable pipelines instead "
                "of one-off spreadsheets. Who stalls: certificate collectors who cannot explain why "
                "two Scope 3 categories dominate a company's footprint.",
                "In August 2026, Big Four and specialist assurance firms still absorb a large share of "
                "early carbon talent, then corporate sustainability teams hire them back at a premium "
                "once disclosure cycles mature. That revolving door is a feature — use it intentionally.",
            )
            + _section(
                "ESG Analyst Roles: Markets Meet Operations",
                "ESG analyst jobs India span sell-side/buy-side research, corporate sustainability, "
                "and banking ESG risk. The corporate ESG analyst translates operations into disclosure "
                "and improvement roadmaps. The investor ESG analyst scores issuers and flags "
                "controversies. The bank ESG risk analyst embeds climate and social factors into credit.",
                "Expectation gap: many candidates apply with only 'ESG rating' familiarity. Employers "
                "want sector fluency — cement is not IT services; EV OEMs are not solar EPCs. The "
                "best analysts pick one sector depth and one framework depth (BRSR, ISSB-aligned "
                "metrics, or lender taxonomies) rather than skim-reading every framework logo.",
                "Compensation often tracks finance analyst bands early, then diverges: corporate roles "
                "may lag markets roles on cash but offer closer access to plant and product decisions. "
                "Validate offers with the <a href=\"/salary-calculator/\">CTC Decoder</a> and against "
                "<a href=\"/salary-reality/\">Salary Reality</a> generalist tables — do not assume a "
                "green title equals a green premium.",
            )
            + _section(
                "Renewable Energy Engineers: Build Reality",
                "Renewable energy engineer demand is tied to project pipelines — solar parks, wind, "
                "hybrid, BESS (battery storage), and transmission upgrades — not to motivational "
                "keynotes. Electrical and civil engineers with plant commissioning, grid interconnection, "
                "and O&M experience remain scarce relative to slide-deck 'renewables enthusiasts.'",
                "Hiring clusters: project developers, EPCs, OEMs, and increasingly GCC energy analytics "
                "teams supporting global portfolios. Roles include design engineers, site managers, "
                "SCADA/controls specialists, and performance analysts. Travel and site months are "
                "common; remote-only 'renewable engineer' jobs often turn out to be proposal writing.",
                "Salary reality is uneven: strong project engineers at reputable developers can out-earn "
                "mid IT-services developers; weak EPC shops with delayed payments recreate the "
                "instability freelancers know (see "
                "<a href=\"/article/freelancing-reality-india-freedom-myth/\">freelancing reality</a>). "
                "Always check project funding status and payment cycles before romanticising the site.",
            )
            + _section(
                "Where Sustainability Meets Policy, Analytics, and Consulting",
                "Policy fluency is a career asset: state renewable purchase obligations, central "
                "auction designs, EV FAME-era afterlives, and carbon market pilots shape which "
                "projects get built. Consultants who can model policy scenarios for CXOs sit between "
                "strategy firms and engineering houses.",
                "Analytics intersection: satellite and IoT data for asset performance; LCA tools for "
                "product footprints; scenario analysis for transition risk. This is where data "
                "engineers who refuse the "
                "<a href=\"/article/data-science-bubble-excel-work-reality/\">data science bubble</a> "
                "can still add value — by shipping reliable pipelines, not by overclaiming ML.",
                "Consulting intersection: Big Four sustainability practices, boutique climate "
                "advisories, and captive strategy teams. The trap is endless deck work with no "
                "implementation ownership — the same prestige trap PMs know. Negotiate for delivery "
                "mandates if you want skills that transfer into industry.",
            )
            + _section(
                "India Case Study: EV Value Chain",
                "India's EV push created jobs beyond assembly-line slogans: battery pack engineering, "
                "charger network ops, fleet electrification analysts, and ESG reporting for auto "
                "suppliers under OEM pressure. A Pune-based auto-component maker hired an ESG analyst "
                "and a carbon accounting lead in 2025–26 specifically because European OEM questionnaires "
                "started blocking RFQs without Scope 3 plans.",
                "Career lesson: EV 'green jobs' often sit inside traditional manufacturing HR systems "
                "with traditional politics. Title may say sustainability; calendar may say plant "
                "shutdown coordination. Go in with eyes open — and ask who owns the data systems.",
            )
            + _section(
                "India Case Study: Solar and Corporate Power Purchase",
                "Utility-scale solar and commercial & industrial (C&I) open-access deals continue to "
                "hire renewable energy engineers and energy managers. Meanwhile, large IT campuses and "
                "GCCs staff sustainability leads to manage renewable PPAs, green-building certifications, "
                "and employee commuting disclosures — linking facilities, finance, and ESG reporting.",
                "A Hyderabad GCC energy programme in 2026 illustrated the hybrid skillset: one hire "
                "with electrical background for onsite solar and DG displacement analysis; one hire "
                "with finance background for PPA and carbon-accounting integration. Neither was a "
                "generic 'ESG intern.' Both had artefacts: a model and a measurement plan.",
            )
            + _section(
                "India Case Study: Corporate ESG Initiatives That Are Real vs Theatre",
                "Real initiatives have budget lines, assurance timelines, and executive owners. "
                "Theatre has poster campaigns and unpaid 'green champions.' Before joining, ask: "
                "Who signs off on BRSR numbers? Is there an assurance provider? What capital projects "
                "are tied to emission targets? If answers are vague, you are joining marketing.",
                "Cross-link your search with broader career strategy — "
                "<a href=\"/article/career-switch-illusion-changing-jobs-not-career/\">job switches vs career switches</a> "
                "apply here. Moving from IT support to 'ESG executive' without measurement skills is "
                "a lateral title change, not a green career.",
            )
            + _section(
                "What Good Looks Like in Interviews",
                "ESG and sustainability interviews in August 2026 rarely stop at definitions of Scope 1 "
                "versus Scope 2. Expect a case: given a cement plant or an IT campus, which data would "
                "you collect first, which estimates are acceptable, and how would you present uncertainty "
                "to a CFO who cares about assurance cost? Candidates who recite framework acronyms "
                "without measurement judgment lose to quieter analysts who show a worked example.",
                "Renewable interviews probe commissioning stories, grid-curtailment handling, and "
                "safety culture. Bring numbers: performance ratio, downtime causes, PR differences "
                "across seasons. Proposal-only experience is weaker than site-backed experience — "
                "say so honestly and show how you close the gap.",
                "Consulting interviews still over-index on slides. Counter with a one-page "
                "implementation plan: owners, systems, quarterly milestones. Hiring managers burned "
                "by deck-only juniors now ask for that plan explicitly.",
            )
            + _section(
                "Policy Literacy as a Career Moat",
                "India's energy transition is policy-shaped: auction designs, open-access rules, "
                "state-level deviations, and evolving carbon-market pilots. Professionals who can "
                "summarise a regulation's career implication — who gets hired, which projects stall — "
                "become internal translators for leadership. That skill travels between consulting, "
                "corporate strategy, and developer roles.",
                "Build a personal briefing habit: one policy note per month, 600–800 words, with "
                "sources and a 'so what for hiring/capex' paragraph. Over a year you accumulate a "
                "portfolio that looks nothing like certificate galleries and everything like executive "
                "advisory. Pair it with sector-thesis artefacts when switching firms.",
                "International literacy still matters for exporters: CBAM-style mechanisms and buyer "
                "codes of conduct change supplier ESG staffing. If your employer sells into Europe, "
                "learn the buyer's questionnaire logic — that knowledge is portable across industries.",
            )
            + _section(
                "Adjacent Roles People Overlook",
                "Beyond headline ESG analyst and renewable engineer titles, August 2026 demand includes "
                "sustainable procurement specialists, green-building and energy managers for campuses, "
                "climate risk analysts in banks, and product carbon footprint leads inside consumer "
                "goods. Many of these hire from operations, facilities, and supply-chain backgrounds "
                "rather than from pure environmental science.",
                "That is good news for career switchers who already understand how factories, fleets, "
                "or campuses run. Your edge is operational access to data. Add measurement literacy "
                "and you compete — often successfully — against fresher ESG graduates with theory "
                "but no plant access.",
            )
        ),
        "salary_reality": """
<h3>Salary Bands — Sustainability Careers India (August 2026)</h3>
<p>Ranges are editorial medians for metropolitan India. Always decode fixed vs variable with the <a href="/salary-calculator/">CTC Decoder</a>.</p>
<table class="editorial-table">
<thead><tr><th>Role</th><th>Experience</th><th>Typical CTC</th><th>Employer Types</th><th>Skill Premium</th></tr></thead>
<tbody>
<tr><td>ESG Analyst (corporate)</td><td>2–5 YOE</td><td>8–16 LPA</td><td>Listed industrials, GCCs</td><td>BRSR + sector depth</td></tr>
<tr><td>ESG / Climate Analyst (markets)</td><td>2–6 YOE</td><td>12–22 LPA</td><td>AMCs, banks, ratings</td><td>Credit + climate scenarios</td></tr>
<tr><td>Carbon Accounting Specialist</td><td>3–7 YOE</td><td>10–20 LPA</td><td>Corporates, Big Four</td><td>Scope 3 + assurance readiness</td></tr>
<tr><td>Renewable Energy Engineer</td><td>3–8 YOE</td><td>9–18 LPA</td><td>Developers, EPCs, OEMs</td><td>Commissioning + grid skills</td></tr>
<tr><td>Sustainability Consultant</td><td>4–9 YOE</td><td>14–28 LPA</td><td>Big Four, boutiques</td><td>Delivery ownership > decks</td></tr>
<tr><td>Head of Sustainability / ESG</td><td>10–15 YOE</td><td>28–50 LPA+</td><td>Large listed / conglomerates</td><td>Board reporting + capex influence</td></tr>
</tbody>
</table>
<h3>Growth and Geographic Reality</h3>
<p>Mumbai and Delhi-NCR lean finance/ESG risk; Bengaluru and Hyderabad lean GCC + tech-campus sustainability; Chennai, Pune, and Ahmedabad lean manufacturing and auto supply-chain ESG; renewable project roles follow asset locations as much as metro offices.</p>
<p>Compare purchasing power using <a href="/article/what-20-lpa-actually-feels-like-india-purchasing-power/">₹20 LPA reality</a>. A site-heavy renewable role at ₹15 LPA with travel allowances can beat a ₹18 LPA pure-reporting role in central Mumbai after rent — or not, depending on your family constraints. Model it; don't vibe it.</p>
""",
        "stuck_point": _p(
            "'I'll take any green title' — greenwashing titles stall your CV when the next employer "
            "asks for measurement artefacts.",
            "'ESG is only reporting' — reporting without operational leverage becomes a dead end by "
            "year four; push for projects tied to capex or supplier change.",
            "'Solar boom means easy campus offers' — project hiring is lumpy; unpaid delays at weak "
            "EPCs are common. Check funding and payment history.",
            "'My MBA guarantees ESG consulting' — without sector depth or analytics proof, you become "
            "slide inventory. See <a href=\"/article/mba-reality-india-worth-it-2026/\">MBA reality India 2026</a>.",
            "'I'll wait for a perfect green role in pure software' — August 2026 transition-economy "
            "roles in EV, solar, and corporate ESG already compete with mid-software tracks for "
            "people who want measurement work tied to real capital projects.",
            "'Carbon accounting is Excel forever' — employers now want systems and audit trails; "
            "spreadsheet-only profiles plateau.",
        ),
        "verdict": _p(
            "Sustainability careers India in August 2026 are real where measurement, engineering, and "
            "capital allocation meet — and fake where posters replace budgets.",
            "Build a proof stack: one disclosure or inventory artefact, one sector thesis (EV, solar, "
            "cement, IT supply chain), and one policy or market literacy note. That combination "
            "outperforms generic ESG certificates and positions you for both corporate and consulting tracks.",
            "ESG analyst jobs, carbon accounting, and renewable energy engineer paths will keep "
            "expanding with India's energy transition — but selectively. Choose employers with "
            "assurance timelines and funded projects, not just Earth Day calendars. Verify mandates "
            "the same way you would decode a CTC annexure: ask for owners, systems, and dates.",
        ),
    },
    # ── 3. Portfolio-First Hiring & Gig Economy ──────────────────────────────
    {
        "slug": "portfolio-first-hiring-gig-economy-careers-india-2026",
        "title": "Portfolio-First Hiring & Gig Economy Careers: How India Recruits in 2026",
        "category_slug": "career-reality-checks",
        "category_name": "Career Reality Checks",
        "meta_title": "Gig Economy Careers India 2026 — Portfolio-First Hiring",
        "meta_description": (
            "Portfolio-first hiring in India 2026: gig economy careers, freelance AI PMs, "
            "data scientists, digital marketers, and portfolio steps that attract recruiters."
        ),
        "target_persona": _p(
            "Designers, marketers, engineers, and PMs in India navigating portfolio-first hiring "
            "and gig economy careers India in August 2026.",
            "Professionals considering freelance AI product manager, freelance data scientist, or "
            "digital marketing contractor paths alongside — or instead of — full-time roles.",
            "Hiring managers and candidates tired of résumé keyword theatre who want evidence of "
            "shipped work to drive recruitment decisions.",
        ),
        "who_should_avoid": _p(
            "If you already run a stable specialist practice with retainer clients and audited books — "
            "this is refinement, not revelation.",
            "Skip if you need the full-time benefits stack (PF, gratuity, parental leave predictability) "
            "and cannot tolerate invoice volatility — read "
            "<a href=\"/article/freelancing-reality-india-freedom-myth/\">freelancing reality</a> first.",
            "Government and PSU hiring still lean credentials and exams; portfolio-first dynamics "
            "apply weakly there.",
        ),
        "common_expectation": _p(
            "Portfolios are only for designers and photographers; engineers and PMs win on résumés "
            "and LeetCode.",
            "Gig economy careers India mean food-delivery hustles — not high-skill AI and marketing work.",
            "Freelance AI product managers and data scientists easily earn 2× full-time CTC with no "
            "business development effort.",
            "A Notion page of course certificates is a portfolio.",
            "Once you have a strong portfolio, recruiters will discover you automatically.",
        ),
        "actual_reality": (
            _p(
                "Portfolio-first hiring is reshaping recruitment in tech, design, and marketing across "
                "India's product companies, startups, and increasingly GCCs' contractor benches. "
                "August 2026 loops still include résumés and interviews — but the gate that matters "
                "early is evidence: shipped interfaces, growth experiments with numbers, evaluation "
                "harnesses, case write-ups, and public artefacts recruiters can skim in four minutes.",
                "This is distinct from the freedom myth of freelancing. Gig economy careers India at "
                "the high-skill end are closer to specialised consulting with platform discovery "
                "(LinkedIn, Contra-like networks, agency benches, captive contractor programmes) than "
                "to rideshare. Income can be strong. Volatility, tax complexity, and feast-famine "
                "cycles remain. Portfolio-first is the filter; cashflow discipline is the job.",
            )
            + _section(
                "How Portfolio-First Hiring Reshapes Tech Recruitment",
                "Engineering teams burned by credential inflation now ask for GitHub activity that "
                "shows judgment — tests, design docs, incident notes — not only tutorial clones. "
                "Staff-level and platform interviews increasingly start from a candidate-chosen "
                "artefact: 'Walk us through a system you owned.' Candidates without a shareable "
                "story lose to peers with mediocre brands but clear ownership narratives.",
                "AI-adjacent tech hiring is especially artefact-driven. 'Built a RAG demo' is common; "
                "'measured retrieval quality and cost per query in production-like conditions' is rare "
                "and valuable. That mirrors the "
                "<a href=\"/article/ai-upskilling-trap-india-api-wrapper-reality/\">AI upskilling trap</a>: "
                "wrappers without evaluation discipline do not survive portfolio-first screens.",
                "GCCs and product firms still run DSA rounds for campus and junior pipelines. Mid-level "
                "lateral hiring, however, is tilting toward take-home evidence and prior-work deep "
                "dives — especially when headcount freezes make every hire higher-stakes (see "
                "<a href=\"/article/staff-engineer-promotion-freeze-india-2026/\">Staff promotion freeze</a>).",
            )
            + _section(
                "Design and Marketing: Portfolios Were Always the Product",
                "Design hiring never trusted résumés alone. What changed in 2026 is the bar for "
                "narrative: case studies must show problem framing, constraints, failed experiments, "
                "and business outcomes — not only aesthetic final screens. UX salary plateaus still "
                "exist (<a href=\"/article/ux-salary-myth-design-careers-plateau/\">UX salary myth</a>); "
                "portfolio quality is how you escape commodity UI work.",
                "Digital marketing recruitment is shifting from 'managed Facebook ads' claims to "
                "portfolio proof: experiment logs, creative tests, MER/CAC narratives, and landing-page "
                "iterations. Agency burnout paths remain real "
                "(<a href=\"/article/digital-marketing-reality-agency-burnout/\">agency reality</a>); "
                "portfolio-first freelancers who specialise (e.g., B2B LinkedIn + webinar funnels) "
                "often out-earn generalist agency executives — with different risk.",
            )
            + _section(
                "The Rise of Freelance AI Product Managers",
                "Freelance AI product managers emerged because companies want AI features without "
                "full-time PM headcount or clear internal expertise. Typical engagements: discovery "
                "sprints, eval metric design, vendor selection, and MVP scoping for RAG/agents. "
                "Rates in August 2026 for credible freelancers with shipped AI products often beat "
                "pro-rata full-time PM cash — before you subtract unpaid business development time.",
                "Reality check: clients hire you for judgment under ambiguity, not for writing "
                "user stories in Jira. If your experience was pure coordination "
                "(<a href=\"/article/product-manager-reality-india-jira-janitor/\">PM Jira reality</a>), "
                "freelance AI PM work will expose that quickly. Build a case study showing a metric "
                "moved by an AI-assisted workflow you owned.",
            )
            + _section(
                "Freelance Data Scientists and Digital Marketers",
                "Freelance data scientists in India increasingly sell scoped analytics and ML "
                "prototypes to mid-market firms that cannot staff full data teams. The market punishes "
                "title inflation: clients who were burned by 'data science' dashboards now ask for "
                "pipeline ownership and decision impact. Read "
                "<a href=\"/article/junior-data-scientist-reality-india/\">junior data scientist reality</a> "
                "and <a href=\"/article/data-science-bubble-excel-work-reality/\">Excel-work reality</a> "
                "before branding yourself.",
                "Freelance digital marketers with portfolio-first proof (paid social, SEO content "
                "systems, lifecycle email) plug into startup growth teams and traditional SME brands "
                "going online. Gig economy careers India here look like retainers plus project spikes. "
                "The ones who last treat client education and measurement as product — not vanity "
                "impressions.",
            )
            + _section(
                "Practical Steps: Building a Portfolio Recruiters Actually Open",
                "Step 1 — Pick three artefacts, not thirty. One deep case study beats a grid of "
                "unexplained thumbnails. Each artefact needs context, your role, constraints, what "
                "you tried, what failed, and a measurable or qualitative outcome.",
                "Step 2 — Make it scannable in four minutes. Top: one-sentence outcome. Middle: "
                "process with visuals or diagrams. Bottom: lessons and tools. Recruiters do not read "
                "novels on the first pass.",
                "Step 3 — Prove production or decision proximity. 'Class project' is fine for juniors "
                "if the reasoning is sharp; mid-levels need evidence of stakeholders, trade-offs, and "
                "maintenance — the stuff interviews probe.",
                "Step 4 — Publish where your buyers look. Designers: personal site + selective "
                "Behance/Dribbble. Engineers: GitHub + design docs. Marketers: Notion/public teardown "
                "threads with numbers. AI PMs: case PDFs and Loom walkthroughs. One canonical URL "
                "on your résumé beats five half-updated profiles.",
                "Step 5 — Attach a risk-reduction offer. For gig work, propose a paid discovery week "
                "with a clear deliverable. Portfolio-first hiring loves bounded proof. For full-time, "
                "offer a take-home that mirrors the job — then over-index on clarity.",
                "Step 6 — Update monthly. August 2026 market labels change; so should your pinned "
                "artefact. Stale portfolios signal abandoned craft — the opposite of what "
                "portfolio-first screens select for.",
            )
            + _section(
                "Recruitment Mechanics: What Actually Happens in Loops",
                "Recruiter skim → hiring-manager artefact review → deep-dive interview → references "
                "or paid trial. ATS keyword filters still exist, so résumés matter as indexes — but "
                "they are not the product. Candidates who obsess over résumé verbs while neglecting "
                "artefacts fail modern loops in design, growth, and AI product work.",
                "Internal mobility is slower to adopt portfolio-first norms; external hiring is "
                "faster because managers are scarred by bad hires during layoff cycles "
                "(<a href=\"/article/indian-it-layoff-cycle-2026/\">IT layoff cycle</a>). Use that: "
                "external evidence can outrun internal politics if you are switching firms.",
            )
            + _section(
                "Money, Tax, and Risk — Gig vs Full-Time",
                "High-skill gig economy careers India can out-earn full-time roles in peak months and "
                "under-earn in troughs. Model a six-month cash buffer. Price for unpaid sales time. "
                "Understand GST, advance tax, and contract IP clauses. A ₹2.5L/month freelance peak "
                "is not a ₹30 LPA job — it is a volatile small business.",
                "Compare lifestyle math with "
                "<a href=\"/article/remote-work-salary-trap-india/\">remote salary trap</a> and "
                "side-hustle failure patterns in "
                "<a href=\"/article/side-hustle-myth-india-reality/\">side hustle reality</a>. "
                "Portfolio-first freelancing works when the portfolio generates inbound or warm "
                "referrals — not when you refresh job boards hoping someone notices your Notion.",
            )
            + _section(
                "Case Patterns: What Winning Portfolios Share",
                "Across tech, design, and marketing, winning August 2026 portfolios share three traits: "
                "constraint honesty (budget, legacy, politics), decision quality (what you chose not to "
                "do), and aftermath (what broke after launch and how you fixed it). Polished fiction "
                "without aftermath reads as junior. Messy reality with clear thinking reads as senior.",
                "A Bengaluru growth marketer converted agency fatigue into a ₹1.8L/month retainer stack "
                "by publishing two tear-downs with anonymised MER curves and creative test matrices. "
                "A Hyderabad data scientist landed a six-month GCC analytics contract by open-sourcing "
                "a redacted evaluation notebook that showed error analysis — not model worship. An "
                "AI PM freelancer in Pune sold discovery sprints using a one-page eval rubric clients "
                "could reuse after the engagement ended — reducing buyer risk.",
                "These are not unicorn stories. They are portfolio-first hiring working as designed: "
                "artefacts reduce uncertainty faster than interviews alone.",
            )
            + _section(
                "How to Run Outbound Without Looking Desperate",
                "Portfolio-first does not mean passive. Warm outbound works when you lead with a "
                "specific observation about the company's product or funnel plus a relevant artefact "
                "link. Cold 'I am open to opportunities' messages die. Cold 'I noticed X metric "
                "pattern; here is a two-paragraph teardown; happy to do a paid half-day discovery' "
                "gets replies.",
                "Set a weekly cadence: two artefact improvements, five tailored outreaches, one "
                "public note. Treat it like a product sprint. Gig economy careers India punish "
                "inconsistent pipelines the same way product companies punish inconsistent delivery.",
                "For full-time seekers, the same cadence feeds interview confidence. You stop "
                "memorising behavioural answers and start pointing at proof. That shift alone changes "
                "how hiring managers score you on ownership.",
            )
            + _section(
                "When to Stay Full-Time vs Go Hybrid",
                "A hybrid model — full-time role plus tightly scoped evening consulting — only works "
                "with employer policy clarity and energy honesty. Many professionals burn out copying "
                "side-hustle Instagram advice. If your full-time job already demands deep focus, "
                "protect it. Build the portfolio first; monetise second.",
                "Full-time still wins when you need mentorship density, brand credentialing for a "
                "later leap, or benefits your family requires. Portfolio-first hiring inside full-time "
                "markets still rewards you: internal promotions increasingly ask for impact narratives "
                "similar to external case studies. Write them down even if you never freelance.",
                "If you do go independent, time-box the decision: e.g., nine months to replace 70% "
                "of full-time net with retainers, or return to employment with a stronger portfolio. "
                "Open-ended freelancing without metrics recreates the "
                "<a href=\"/article/passion-luxury-not-strategy-india/\">passion-without-strategy</a> trap.",
            )
        ),
        "salary_reality": """
<h3>Pay Reality — Portfolio-First and Gig Paths (August 2026)</h3>
<table class="editorial-table">
<thead><tr><th>Path</th><th>Typical Full-Time CTC</th><th>Gig / Contract Range</th><th>What Buyers Pay For</th></tr></thead>
<tbody>
<tr><td>Product Designer</td><td>12–28 LPA</td><td>₹1.5–4L / project or ₹80k–2L / mo retainer</td><td>Case studies with outcomes</td></tr>
<tr><td>Digital Marketer (growth)</td><td>8–22 LPA</td><td>₹75k–2.5L / mo retainer</td><td>Experiment logs + CAC/MER proof</td></tr>
<tr><td>Freelance AI PM</td><td>18–36 LPA FT equivalent</td><td>₹1.5–3.5L / mo (scoped)</td><td>Shipped AI workflow + metrics</td></tr>
<tr><td>Freelance Data Scientist</td><td>12–30 LPA FT equivalent</td><td>₹1–3L / mo or project fees</td><td>Pipeline + decision impact</td></tr>
<tr><td>Full-stack / platform engineer</td><td>14–34 LPA</td><td>₹1.2–3L / mo contract</td><td>Owned systems artefacts</td></tr>
</tbody>
</table>
<p>Decode offers and contracts with the <a href="/salary-calculator/">CTC Decoder</a>. For full-time comparisons use <a href="/salary-reality/">Salary Reality</a>. Gig rates assume you already have proof; beginners earn less while building artefacts.</p>
<h3>Utilisation Reality</h3>
<p>Billable months of 8–10 per year are common even for strong freelancers after sales lag, client pauses, and payment delays. Price a 30–40% utilisation haircut into lifestyle planning. Portfolio-first hiring improves close rates; it does not eliminate collections risk. Track utilisation monthly the same way you would track a product funnel — otherwise peak months create false confidence.</p>
""",
        "stuck_point": _p(
            "'My GitHub has 40 tutorial repos' — that signals consumption, not judgment. Pin three "
            "owned projects with READMEs that explain trade-offs.",
            "'I'll go freelance for freedom' — without a portfolio and pipeline, freedom becomes "
            "unpaid anxiety. Read the freelancing reality piece before resigning.",
            "'Certificates are my portfolio' — recruiters skim artefacts of work, not badges.",
            "'AI PM freelance is easy money' — clients hire outcome owners; Jira coordinators get "
            "cut mid-sprint.",
            "'I'll wait until my portfolio is perfect' — ship a public v1 this month; iterate. "
            "Perfectionism is how August becomes December with nothing to show.",
            "'Recruiters will find me if my work is good' — discovery is a system. Publish, outbound, "
            "and ask satisfied clients for referrals on a schedule.",
        ),
        "verdict": _p(
            "Portfolio-first hiring is not a fad — it is how risk-averse teams hire for design, "
            "marketing, and AI-adjacent work in August 2026 when every seat is expensive.",
            "Gig economy careers India at the high-skill layer reward specialists with proof and "
            "punish generalists with only résumés. Build three sharp artefacts, publish one canonical "
            "URL, and price for volatility.",
            "Whether you stay full-time or go freelance AI PM / data scientist / marketer, the "
            "career asset is the same: evidence that you shipped judgment under constraints. That "
            "is the new recruiting language — learn to speak it fluently, update it monthly, and "
            "treat your portfolio as a product with users named hiring managers and clients.",
        ),
    },
]


def main():
    import django

    django.setup()
    from content.models import Article, Author, Category

    author = Author.objects.filter(is_active=True).order_by("id").first()
    if not author:
        author = Author.objects.create(
            name="P. Mishra",
            display_name="P. Mishra",
            bio="Senior Editor. Independent Observer of Indian Tech Markets.",
            linkedin_url="https://linkedin.com/in/pmishra-reality",
            is_active=True,
        )

    for data in ARTICLES:
        category, _ = Category.objects.get_or_create(
            slug=data["category_slug"],
            defaults={"name": data["category_name"], "order": 1},
        )
        if category.name != data["category_name"]:
            category.name = data["category_name"]
            category.save(update_fields=["name"])

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
        print(f"{'Created' if created else 'Updated'}: {data['slug']}")


if __name__ == "__main__":
    main()
