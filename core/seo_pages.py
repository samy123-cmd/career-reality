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

SALARY_REALITY_ENGINE = PageSEO(
    title="Salary Reality Engine — Am I Underpaid? Free India Salary Percentile Tool",
    description=(
        "Enter your role, YOE, city, and CTC to see your salary percentile, market range, "
        "and realistic next salary. Built on crowdsourced Indian tech data."
    ),
    h1="Salary Reality Engine",
    keywords=(
        "am i underpaid india",
        "salary percentile calculator india",
        "market salary range software engineer",
    ),
)

OFFER_ANALYZER = PageSEO(
    title="Job Offer Analyzer India — Compare Two Offers (Free)",
    description=(
        "Paste two job offers and get a clear verdict comparing salary, variable pay, "
        "commute, WLB, stability, growth, and risk."
    ),
    h1="Offer Analyzer",
    keywords=("job offer comparison india", "which offer should i take", "offer analyzer"),
)

STAY_VS_SWITCH = PageSEO(
    title="Stay vs Switch Analyzer — Should I Leave My Job? (Free India Tool)",
    description=(
        "Enter your current job and market situation. Get Stay, Switch, or Wait "
        "with financial and career reasoning backed by real data."
    ),
    h1="Stay vs Switch Analyzer",
    keywords=("should i switch jobs india", "stay or leave job", "career switch calculator"),
)

AI_CAREER_IMPACT = PageSEO(
    title="AI Career Impact — AI Risk Score for Your Job Title (Free)",
    description=(
        "Enter your job title to get an AI Risk Score, vulnerable tasks, future demand, "
        "and skills to learn to stay valuable in 2026."
    ),
    h1="AI Career Impact",
    keywords=("ai job risk calculator", "will ai replace my job", "ai career impact india"),
)

NEXT_CAREER_MOVE = PageSEO(
    title="Next Career Move — Highest ROI Career Paths for Indian Tech (Free)",
    description=(
        "Based on your skills, experience, and salary, get ranked recommendations: "
        "promotion, company switch, GCC, management, architecture, or AI upskill."
    ),
    h1="Next Career Move",
    keywords=("career path calculator india", "next career move tech", "career roi"),
)

ASK_CAREER_REALITY = PageSEO(
    title="Ask CareerReality — AI Career Advisor for Indian Tech Professionals",
    description=(
        "Ask career questions like 'I make ₹18L at TCS — should I take ₹23L at a startup?' "
        "and get evidence-backed answers using CareerReality data."
    ),
    h1="Ask CareerReality",
    keywords=("career advice india", "ask career advisor", "career chatbot india"),
)

# Per-tool FAQ content for JSON-LD and visible accordions on tool pages.
TOOL_FAQS: dict[str, tuple[dict[str, str], ...]] = {
    "salary_reality_engine": (
        {"q": "How accurate is the salary percentile?", "a": "We blend crowdsourced submissions with editorial bands. Sample size and confidence are shown on every result."},
        {"q": "What does underpaid mean?", "a": "Your CTC is more than 10% below the market median for your role, YOE, and city band."},
        {"q": "Is my data stored?", "a": "No login required. Inputs are used only to compute your result in this session."},
    ),
    "offer_analyzer": (
        {"q": "How do you compare two offers?", "a": "We score effective comp, company stability, market fit, WLB, commute, and growth on a 0–10 scale."},
        {"q": "Should I include ESOP in CTC?", "a": "Enter ESOP value separately if known. We amortize it over 4 years in effective comp."},
        {"q": "What if the company is not in your database?", "a": "We use conservative stability estimates and still compare compensation and commute factors."},
    ),
    "stay_vs_switch": (
        {"q": "What does Wait mean?", "a": "Signals are mixed — build leverage (offer, savings, skills) before resigning."},
        {"q": "Does this replace financial advice?", "a": "No. This is decision support based on market data, not personalized financial planning."},
        {"q": "How is company risk factored in?", "a": "We use layoff reports, review scores, and the Company Reality Score when available."},
    ),
    "ai_career_impact": (
        {"q": "What is an AI Risk Score?", "a": "A 0–100 measure of how exposed your role's tasks are to automation and AI tooling in 2026."},
        {"q": "Is my job safe if the score is low?", "a": "Low exposure means core work involves judgment and scope AI cannot easily replace — still upskill proactively."},
        {"q": "Where does the data come from?", "a": "Rule-based mapping from editorial research plus AI Pulse career impact signals."},
    ),
    "next_career_move": (
        {"q": "How are paths ranked?", "a": "By ROI score (comp upside) weighted with fit score (your YOE, company type, and skills)."},
        {"q": "Why only one path on free?", "a": "Pro unlocks the full ranked list with action plans for every path."},
        {"q": "Is GCC always better than IT services?", "a": "Not always — we factor your current company type and typical GCC premiums at your YOE."},
    ),
    "ask_career_reality": (
        {"q": "What can I ask?", "a": "Salary comparisons, offer decisions, switch timing — include role, YOE, CTC, and city for best answers."},
        {"q": "How many free questions?", "a": "Three per month for free users. Pro gets unlimited access."},
        {"q": "Does it use ChatGPT?", "a": "We use CareerReality's own salary, company, and layoff data first; optional AI narration when an API key is configured."},
    ),
}

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
        "label": "Salary Reality Engine",
        "description": "Role + YOE + city → percentile, market range, under/overpaid flag.",
        "url_name": "tools:salary_reality_engine",
        "icon": "salary",
    },
    {
        "label": "Offer Analyzer",
        "description": "Compare two offers — get a clear which-one-to-take verdict.",
        "url_name": "tools:offer_analyzer",
        "icon": "ctc",
    },
    {
        "label": "Stay vs Switch",
        "description": "Stay, Switch, or Wait — with financial and career reasoning.",
        "url_name": "tools:stay_vs_switch",
        "icon": "risk",
    },
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
        "label": "AI Career Impact",
        "description": "AI risk score, vulnerable tasks, and skills to learn.",
        "url_name": "tools:ai_career_impact",
        "icon": "pulse",
    },
    {
        "label": "Next Career Move",
        "description": "Highest-ROI paths: switch, promotion, GCC, AI upskill.",
        "url_name": "tools:next_career_move",
        "icon": "company",
    },
    {
        "label": "IT Layoff Radar",
        "description": "Hiring freeze and layoff signals across Indian tech.",
        "url_name": "layoff_radar",
        "icon": "radar",
    },
    {
        "label": "Ask CareerReality",
        "description": "Evidence-backed career advice from our own data.",
        "url_name": "tools:ask_career_reality",
        "icon": "company",
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
