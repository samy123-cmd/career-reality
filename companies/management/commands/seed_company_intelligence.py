"""
Seed Company Intelligence Hub with benchmark data.

Sources (editorial aggregation, not live API):
- Glassdoor / AmbitionBox public ratings (2024–2025)
- Levels.fyi India salary bands
- Community-reported layoff signals from public news cycles

Run:
    python manage.py seed_company_intelligence
    python manage.py seed_company_intelligence --force   # re-link salaries & sync stats
"""

from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from analyzer.models import LayoffReport, SalarySubmission
from companies.models import Company, CompanyReview
from companies.stats import sync_all_company_stats

# ── Company profiles ─────────────────────────────────────────────────────────
COMPANIES = [
    {"name": "Tata Consultancy Services", "sector": "service", "size": "10001+", "headquarters": "Mumbai", "founded_year": 1968, "work_mode": "hybrid", "glassdoor_rating": 3.9, "ambitionbox_rating": 3.8, "description": "India's largest IT services company by revenue and market cap. Known for stable careers but slower growth curves."},
    {"name": "Infosys", "sector": "service", "size": "10001+", "headquarters": "Bangalore", "founded_year": 1981, "work_mode": "hybrid", "glassdoor_rating": 3.8, "ambitionbox_rating": 3.7, "description": "Tier-1 IT bellwether. Strong training program (Mysore campus) but variable team experience."},
    {"name": "Wipro", "sector": "service", "size": "10001+", "headquarters": "Bangalore", "founded_year": 1945, "work_mode": "hybrid", "glassdoor_rating": 3.7, "ambitionbox_rating": 3.5, "description": "Diversified IT services and consulting. Undergoing transformation under new leadership."},
    {"name": "HCLTech", "sector": "service", "size": "10001+", "headquarters": "Noida", "founded_year": 1976, "work_mode": "hybrid", "glassdoor_rating": 3.8, "ambitionbox_rating": 3.6, "description": "Strong in infrastructure management and engineering services. Known for Mode 1-2-3 strategy."},
    {"name": "Tech Mahindra", "sector": "service", "size": "10001+", "headquarters": "Pune", "founded_year": 1986, "work_mode": "hybrid", "glassdoor_rating": 3.6, "ambitionbox_rating": 3.4, "description": "Telecom-focused IT services. Part of Mahindra Group. Known for aggressive deal-making."},
    {"name": "Cognizant", "sector": "service", "size": "10001+", "headquarters": "Chennai", "founded_year": 1994, "work_mode": "hybrid", "glassdoor_rating": 3.8, "ambitionbox_rating": 3.6, "description": "US-headquartered but India-heavy IT services firm. Known for rapid hiring and variable project quality."},
    {"name": "LTIMindtree", "sector": "service", "size": "10001+", "headquarters": "Mumbai", "founded_year": 2022, "work_mode": "hybrid", "glassdoor_rating": 3.7, "ambitionbox_rating": 3.5, "description": "Merged entity of LTI and Mindtree under L&T Group. Growing mid-tier challenger."},
    {"name": "Flipkart", "sector": "ecommerce", "size": "10001+", "headquarters": "Bangalore", "founded_year": 2007, "work_mode": "hybrid", "glassdoor_rating": 3.9, "ambitionbox_rating": 4.0, "description": "India's largest e-commerce platform. Walmart-owned. Known for strong engineering culture and competitive pay."},
    {"name": "Razorpay", "sector": "bfsi", "size": "1001-5000", "headquarters": "Bangalore", "founded_year": 2014, "work_mode": "hybrid", "glassdoor_rating": 3.6, "ambitionbox_rating": 3.8, "description": "Leading Indian payments infrastructure company. Known for fast-paced fintech culture."},
    {"name": "Zerodha", "sector": "bfsi", "size": "201-1000", "headquarters": "Bangalore", "founded_year": 2010, "work_mode": "office", "glassdoor_rating": 3.8, "ambitionbox_rating": 4.1, "description": "India's largest retail stockbroker. Bootstrapped. Known for lean team and strong tech culture."},
    {"name": "PhonePe", "sector": "bfsi", "size": "5001-10000", "headquarters": "Bangalore", "founded_year": 2015, "work_mode": "hybrid", "glassdoor_rating": 3.7, "ambitionbox_rating": 3.9, "description": "UPI payments leader. Walmart-backed. Known for high-growth fintech culture."},
    {"name": "CRED", "sector": "bfsi", "size": "201-1000", "headquarters": "Bangalore", "founded_year": 2018, "work_mode": "office", "glassdoor_rating": 3.5, "ambitionbox_rating": 3.8, "description": "Credit card rewards platform. Known for premium brand but debated unit economics."},
    {"name": "Freshworks", "sector": "product", "size": "5001-10000", "headquarters": "Chennai", "founded_year": 2010, "work_mode": "hybrid", "glassdoor_rating": 3.7, "ambitionbox_rating": 3.8, "description": "SaaS company (CRM, ITSM). NASDAQ-listed. Chennai's flagship tech product company."},
    {"name": "Zoho", "sector": "product", "size": "10001+", "headquarters": "Chennai", "founded_year": 1996, "work_mode": "office", "glassdoor_rating": 4.0, "ambitionbox_rating": 4.1, "description": "Bootstrapped SaaS giant with 55+ products. Known for rural development centers and no-VC model."},
    {"name": "Postman", "sector": "product", "size": "201-1000", "headquarters": "Bangalore", "founded_year": 2014, "work_mode": "hybrid", "glassdoor_rating": 4.1, "ambitionbox_rating": 4.2, "description": "API development platform used by 30M+ developers. YC-backed, strong engineering culture."},
    {"name": "Zomato", "sector": "ecommerce", "size": "5001-10000", "headquarters": "Gurugram", "founded_year": 2008, "work_mode": "hybrid", "glassdoor_rating": 3.5, "ambitionbox_rating": 3.6, "description": "Food delivery and quick commerce (Blinkit). Public company. Known for aggressive culture."},
    {"name": "Swiggy", "sector": "ecommerce", "size": "5001-10000", "headquarters": "Bangalore", "founded_year": 2014, "work_mode": "hybrid", "glassdoor_rating": 3.6, "ambitionbox_rating": 3.5, "description": "Food delivery and quick commerce (Instamart). Known for fast-paced execution culture."},
    {"name": "Meesho", "sector": "ecommerce", "size": "1001-5000", "headquarters": "Bangalore", "founded_year": 2015, "work_mode": "hybrid", "glassdoor_rating": 3.4, "ambitionbox_rating": 3.5, "description": "Social commerce platform for Tier 2-3 India. Known for high growth but burnout concerns."},
    {"name": "Ola", "sector": "other", "size": "5001-10000", "headquarters": "Bangalore", "founded_year": 2010, "work_mode": "office", "glassdoor_rating": 3.3, "ambitionbox_rating": 3.2, "description": "Ride-hailing and EV company. Known for founder-driven culture and pivot to electric vehicles."},
    {"name": "Paytm", "sector": "bfsi", "size": "10001+", "headquarters": "Noida", "founded_year": 2010, "work_mode": "office", "glassdoor_rating": 3.4, "ambitionbox_rating": 3.3, "description": "Fintech and digital payments. Public company. Known for regulatory challenges and pivot cycles."},
    {"name": "Byju's", "sector": "edtech", "size": "5001-10000", "headquarters": "Bangalore", "founded_year": 2011, "work_mode": "office", "glassdoor_rating": 3.0, "ambitionbox_rating": 2.8, "description": "Once India's most valuable edtech startup. Known for aggressive sales culture and financial distress."},
    {"name": "Unacademy", "sector": "edtech", "size": "1001-5000", "headquarters": "Bangalore", "founded_year": 2015, "work_mode": "hybrid", "glassdoor_rating": 3.2, "ambitionbox_rating": 3.0, "description": "EdTech platform for competitive exam prep. Known for layoff cycles and pivot from live to recorded."},
    {"name": "Google India", "sector": "mnc_captive", "size": "10001+", "headquarters": "Bangalore", "founded_year": 2004, "work_mode": "hybrid", "glassdoor_rating": 4.4, "ambitionbox_rating": 4.5, "description": "Top tier compensation and engineering culture. Hyderabad and Bangalore offices. Extremely selective hiring."},
    {"name": "Microsoft India", "sector": "mnc_captive", "size": "10001+", "headquarters": "Hyderabad", "founded_year": 1990, "work_mode": "hybrid", "glassdoor_rating": 4.3, "ambitionbox_rating": 4.4, "description": "Largest MNC engineering center in India. Known for work-life balance and Azure/AI growth."},
    {"name": "Amazon India", "sector": "mnc_captive", "size": "10001+", "headquarters": "Bangalore", "founded_year": 2004, "work_mode": "office", "glassdoor_rating": 3.9, "ambitionbox_rating": 3.8, "description": "Massive engineering, retail, and AWS presence. Known for high bar, PIP culture, and competitive RSU packages."},
    {"name": "Goldman Sachs India", "sector": "bfsi", "size": "5001-10000", "headquarters": "Bangalore", "founded_year": 2004, "work_mode": "office", "glassdoor_rating": 4.0, "ambitionbox_rating": 4.1, "description": "Major GCC for Goldman Sachs. Strong compensation for fintech roles. Known for long hours."},
    {"name": "Atlassian India", "sector": "product", "size": "1001-5000", "headquarters": "Bangalore", "founded_year": 2005, "work_mode": "remote", "glassdoor_rating": 4.2, "ambitionbox_rating": 4.3, "description": "TEAM Anywhere policy — fully distributed. Strong DevOps/Agile tooling maker. Premium compensation."},
    {"name": "Adobe India", "sector": "mnc_captive", "size": "5001-10000", "headquarters": "Noida", "founded_year": 1997, "work_mode": "hybrid", "glassdoor_rating": 4.3, "ambitionbox_rating": 4.4, "description": "India's largest R&D center for Adobe. Known for excellent work-life balance and creative culture."},
    {"name": "Uber India", "sector": "mnc_captive", "size": "1001-5000", "headquarters": "Bangalore", "founded_year": 2013, "work_mode": "hybrid", "glassdoor_rating": 4.0, "ambitionbox_rating": 3.9, "description": "Key engineering hub for Uber. Strong compensation and scale challenges. Known for data-driven culture."},
    {"name": "Practo", "sector": "healthtech", "size": "201-1000", "headquarters": "Bangalore", "founded_year": 2008, "work_mode": "hybrid", "glassdoor_rating": 3.5, "ambitionbox_rating": 3.4, "description": "India's largest health-tech platform. Connecting patients with doctors. Profitable but slow-growing."},
    {"name": "PharmEasy", "sector": "healthtech", "size": "1001-5000", "headquarters": "Mumbai", "founded_year": 2015, "work_mode": "hybrid", "glassdoor_rating": 3.3, "ambitionbox_rating": 3.2, "description": "Online pharmacy and diagnostics. Known for aggressive expansion and valuation questions."},
    {"name": "Nykaa", "sector": "ecommerce", "size": "1001-5000", "headquarters": "Mumbai", "founded_year": 2012, "work_mode": "office", "glassdoor_rating": 3.4, "ambitionbox_rating": 3.3, "description": "Beauty and fashion e-commerce. Public company. Known for strong brand but tech team churn."},
    {"name": "Dream11", "sector": "other", "size": "201-1000", "headquarters": "Mumbai", "founded_year": 2008, "work_mode": "office", "glassdoor_rating": 3.8, "ambitionbox_rating": 4.0, "description": "India's largest fantasy sports platform. Profitable unicorn. Known for lean team and high comp."},
    {"name": "Groww", "sector": "bfsi", "size": "1001-5000", "headquarters": "Bangalore", "founded_year": 2016, "work_mode": "hybrid", "glassdoor_rating": 3.7, "ambitionbox_rating": 3.8, "description": "Investment and trading platform challenging Zerodha. Known for rapid growth and young team."},
    {"name": "Juspay", "sector": "bfsi", "size": "201-1000", "headquarters": "Bangalore", "founded_year": 2012, "work_mode": "office", "glassdoor_rating": 3.6, "ambitionbox_rating": 3.7, "description": "Payment orchestration platform behind many UPI apps. Known for Haskell/FP engineering culture."},
]

COMPANY_BRANDING = {
    "Tata Consultancy Services": {"website": "https://www.tcs.com", "logo_url": "https://logo.clearbit.com/tcs.com"},
    "Infosys": {"website": "https://www.infosys.com", "logo_url": "https://logo.clearbit.com/infosys.com"},
    "Wipro": {"website": "https://www.wipro.com", "logo_url": "https://logo.clearbit.com/wipro.com"},
    "Cognizant": {"website": "https://www.cognizant.com", "logo_url": "https://logo.clearbit.com/cognizant.com"},
    "HCLTech": {"website": "https://www.hcltech.com", "logo_url": "https://logo.clearbit.com/hcltech.com"},
    "Tech Mahindra": {"website": "https://www.techmahindra.com", "logo_url": "https://logo.clearbit.com/techmahindra.com"},
    "LTIMindtree": {"website": "https://www.ltimindtree.com", "logo_url": "https://logo.clearbit.com/ltimindtree.com"},
    "Zoho": {"website": "https://www.zoho.com", "logo_url": "https://logo.clearbit.com/zoho.com"},
    "Freshworks": {"website": "https://www.freshworks.com", "logo_url": "https://logo.clearbit.com/freshworks.com"},
    "Postman": {"website": "https://www.postman.com", "logo_url": "https://logo.clearbit.com/postman.com"},
    "Google India": {"website": "https://careers.google.com/locations/india/", "logo_url": "https://logo.clearbit.com/google.com"},
    "Microsoft India": {"website": "https://www.microsoft.com/en-in", "logo_url": "https://logo.clearbit.com/microsoft.com"},
    "Amazon India": {"website": "https://www.amazon.jobs/en/locations/india", "logo_url": "https://logo.clearbit.com/amazon.com"},
    "Adobe India": {"website": "https://www.adobe.com/in/", "logo_url": "https://logo.clearbit.com/adobe.com"},
    "Atlassian India": {"website": "https://www.atlassian.com", "logo_url": "https://logo.clearbit.com/atlassian.com"},
    "Uber India": {"website": "https://www.uber.com/in/en/", "logo_url": "https://logo.clearbit.com/uber.com"},
    "Goldman Sachs India": {"website": "https://www.goldmansachs.com/worldwide/india/", "logo_url": "https://logo.clearbit.com/goldmansachs.com"},
    "Razorpay": {"website": "https://razorpay.com", "logo_url": "https://logo.clearbit.com/razorpay.com"},
    "PhonePe": {"website": "https://www.phonepe.com", "logo_url": "https://logo.clearbit.com/phonepe.com"},
    "CRED": {"website": "https://cred.club", "logo_url": "https://logo.clearbit.com/cred.club"},
    "Zerodha": {"website": "https://zerodha.com", "logo_url": "https://logo.clearbit.com/zerodha.com"},
    "Paytm": {"website": "https://paytm.com", "logo_url": "https://logo.clearbit.com/paytm.com"},
    "Groww": {"website": "https://groww.in", "logo_url": "https://logo.clearbit.com/groww.in"},
    "Juspay": {"website": "https://juspay.in", "logo_url": "https://logo.clearbit.com/juspay.in"},
    "Flipkart": {"website": "https://www.flipkart.com", "logo_url": "https://logo.clearbit.com/flipkart.com"},
    "Zomato": {"website": "https://www.zomato.com", "logo_url": "https://logo.clearbit.com/zomato.com"},
    "Swiggy": {"website": "https://www.swiggy.com", "logo_url": "https://logo.clearbit.com/swiggy.com"},
    "Meesho": {"website": "https://meesho.com", "logo_url": "https://logo.clearbit.com/meesho.com"},
    "Nykaa": {"website": "https://www.nykaa.com", "logo_url": "https://logo.clearbit.com/nykaa.com"},
    "Byju's": {"website": "https://byjus.com", "logo_url": "https://logo.clearbit.com/byjus.com"},
    "Unacademy": {"website": "https://unacademy.com", "logo_url": "https://logo.clearbit.com/unacademy.com"},
    "Practo": {"website": "https://www.practo.com", "logo_url": "https://logo.clearbit.com/practo.com"},
    "PharmEasy": {"website": "https://pharmeasy.in", "logo_url": "https://logo.clearbit.com/pharmeasy.in"},
    "Dream11": {"website": "https://www.dream11.com", "logo_url": "https://logo.clearbit.com/dream11.com"},
    "Ola": {"website": "https://www.olacabs.com", "logo_url": "https://logo.clearbit.com/olacabs.com"},
}

# Salary rows: (role, exp, company_type, ctc, in_hand, city, stack)
# Imported from seed_company_salaries.py — truncated in command via exec of external file
SALARY_FILE = "seed_company_salaries.py"

LAYOFF_SIGNALS = [
    ("Byju's", "layoff", "Sales, Content", "Bengaluru", "Multiple restructuring rounds reported across sales and content teams since 2023."),
    ("Unacademy", "layoff", "Operations, Marketing", "Bengaluru", "Repeated layoff cycles during pivot from live classes to recorded content."),
    ("Ola", "freeze", "Corporate", "Bangalore", "Hiring slowed during EV pivot; selective backfills only in core mobility teams."),
    ("Amazon India", "freeze", "Corporate, Support", "Multiple", "Selective hiring freeze in some business units during 2023–24 cost optimization."),
    ("Paytm", "rumor", "Operations", "Noida", "Periodic restructuring rumors amid regulatory scrutiny and business model shifts."),
    ("PharmEasy", "layoff", "Operations", "Mumbai", "Workforce reductions reported during consolidation in online pharmacy sector."),
    ("Meesho", "freeze", "Engineering", "Bengaluru", "Hiring pace moderated after rapid 2021–22 expansion in social commerce."),
    ("Flipkart", "hiring", "Engineering", "Bengaluru", "Continued engineering hiring for supply chain and marketplace platforms."),
    ("Google India", "hiring", "Engineering", "Bengaluru", "Selective hiring in Cloud and AI teams despite global caution."),
    ("Microsoft India", "hiring", "Engineering", "Hyderabad", "Azure and AI hiring remains active in India GCC."),
    ("Zoho", "hiring", "Engineering", "Chennai", "Steady campus and lateral hiring across product lines."),
    ("Infosys", "hiring", "Engineering", "Multiple", "Large fresher intake continues; lateral hiring moderate."),
]

SECTOR_REVIEW_COPY = {
    "service": {
        "pros": "Job security, structured training, and predictable increments for early-career engineers. Good option if you need visa sponsorship pathways or long-term stability.",
        "cons": "Bench periods, slow promotion cycles, and variable project quality. CTC inflation vs actual in-hand can be misleading once benefits are stripped out.",
        "lie": "Fast-track promotion in 18 months",
    },
    "product": {
        "pros": "Ownership of real product problems, better engineering standards, and stronger resume signal when switching. Pay bands often beat service companies at equivalent experience.",
        "cons": "Release pressure, on-call rotations, and reorgs when growth slows. Not every team gets equity or meaningful bonus payouts.",
        "lie": "Flat hierarchy with no politics",
    },
    "unicorn": {
        "pros": "Top-of-market cash + ESOP packages, strong peers, and brand value for your next switch. Exposure to scale problems you won't see in smaller firms.",
        "cons": "Performance bar is brutal, stack ranking in some orgs, and ESOP value depends on liquidity events. Burnout risk is real.",
        "lie": "ESOPs will definitely make you rich",
    },
    "mnc_captive": {
        "pros": "Global engineering standards, excellent benefits, and better work-life balance than most Indian product firms. Strong internal mobility if you perform.",
        "cons": "India teams sometimes get maintenance work, slower decision loops, and timezone friction with US/EU HQs.",
        "lie": "Same career growth as US headquarters",
    },
    "bfsi": {
        "pros": "Strong compensation in core engineering and quant roles. Fintech exposure is valuable if you want to stay in payments or banking tech.",
        "cons": "Regulatory overhead, compliance-driven roadmaps, and sudden pivots when funding tightens.",
        "lie": "Startup speed with bank-level stability",
    },
    "ecommerce": {
        "pros": "High-scale engineering, data-driven culture, and competitive pay during growth phases. Good for learning supply chain and consumer tech.",
        "cons": "Long hours during sale events, frequent strategy changes, and layoff risk when unit economics tighten.",
        "lie": "Hypergrowth forever",
    },
    "edtech": {
        "pros": "Mission-driven teams, fast iteration, and broad full-stack exposure when the business is growing.",
        "cons": "Sales-driven culture in many orgs, compensation volatility, and severe instability when funding dries up.",
        "lie": "Edtech is recession-proof",
    },
    "healthtech": {
        "pros": "Meaningful domain problems, growing market, and less hype-driven hiring than consumer tech.",
        "cons": "Regulatory complexity, slower monetization, and smaller pay bands than fintech or big tech.",
        "lie": "Healthcare margins mean safe jobs",
    },
    "other": {
        "pros": "Varies widely by team — some units offer strong comp and interesting problems.",
        "cons": "Strategy shifts, founder-driven decisions, and uneven manager quality across business units.",
        "lie": "We're profitable so jobs are safe",
    },
}


def _rating_from_glassdoor(gd):
    if gd is None:
        return 3
    return max(1, min(5, round(float(gd))))


def _load_company_salaries():
    """Load COMPANY_SALARIES dict from existing seed script without executing inserts."""
    import ast
    from pathlib import Path

    path = Path(__file__).resolve().parents[3] / "seed_company_salaries.py"
    source = path.read_text(encoding="utf-8")
    start = source.index("COMPANY_SALARIES = {")
    end = source.index("\n\n# ── Update Company records")
    chunk = source[start : end]
    return ast.literal_eval(chunk.split("=", 1)[1].strip())


class Command(BaseCommand):
    help = "Seed company profiles, salaries, reviews, and layoff signals from editorial benchmarks."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Re-link salary rows to companies and re-seed reviews/layoffs if missing.",
        )
        parser.add_argument(
            "--skip-reviews",
            action="store_true",
            help="Skip anonymous review seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        force = options["force"]
        skip_reviews = options["skip_reviews"]

        created_cos = updated_cos = 0
        for data in COMPANIES:
            branding = COMPANY_BRANDING.get(data["name"], {})
            company, created = Company.objects.get_or_create(
                name=data["name"],
                defaults={**data, "is_verified": True, **branding},
            )
            if created:
                created_cos += 1
            else:
                changed = False
                for key, val in data.items():
                    if getattr(company, key) != val:
                        setattr(company, key, val)
                        changed = True
                for key, val in branding.items():
                    if val and getattr(company, key) != val:
                        setattr(company, key, val)
                        changed = True
                if not company.is_verified:
                    company.is_verified = True
                    changed = True
                if changed:
                    company.save()
                    updated_cos += 1

        self.stdout.write(self.style.SUCCESS(f"Companies: {created_cos} created, {updated_cos} updated"))

        company_salaries = _load_company_salaries()
        salaries_created = salaries_linked = 0

        for company_name, entries in company_salaries.items():
            try:
                company = Company.objects.get(name=company_name)
            except Company.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"  Skip salaries — unknown company: {company_name}"))
                continue

            for role, exp, ctype, ctc, in_hand, city, stack in entries:
                existing = SalarySubmission.objects.filter(
                    Q(company=company) | Q(company_name__iexact=company_name),
                    role=role,
                    experience_years=exp,
                    ctc=ctc,
                ).first()

                if existing:
                    if not existing.company_id or not existing.company_name:
                        existing.company = company
                        existing.company_name = company_name
                        existing.verification_status = "verified"
                        existing.save(update_fields=["company", "company_name", "verification_status", "is_verified"])
                        salaries_linked += 1
                    continue

                SalarySubmission.objects.create(
                    company=company,
                    company_name=company_name,
                    role=role,
                    experience_years=exp,
                    company_type=ctype,
                    ctc=ctc,
                    in_hand=in_hand,
                    city=city,
                    tech_stack=stack,
                    verification_status="verified",
                )
                salaries_created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Salaries: {salaries_created} created, {salaries_linked} linked"
        ))

        if not skip_reviews:
            reviews_created = 0
            for company in Company.objects.all():
                if company.reviews.exists() and not force:
                    continue

                if force:
                    company.reviews.filter(is_verified=True).delete()

                copy = SECTOR_REVIEW_COPY.get(company.sector, SECTOR_REVIEW_COPY["other"])
                base = _rating_from_glassdoor(company.glassdoor_rating)

                profiles = [
                    ("Software Engineer", "mid", "current", 28, base),
                    ("Senior Software Engineer", "senior", "former", 42, max(1, base - 1)),
                ]
                if company.sector in ("unicorn", "mnc_captive", "product"):
                    profiles = profiles[:1] + [("Staff Engineer", "lead", "former", 60, min(5, base + 1))]

                for role_title, level, status, tenure, overall in profiles:
                    if CompanyReview.objects.filter(company=company, role_title=role_title, tenure_months=tenure).exists():
                        continue
                    CompanyReview.objects.create(
                        company=company,
                        role_title=role_title,
                        role_level=level,
                        employment_status=status,
                        tenure_months=tenure,
                        rating_overall=overall,
                        rating_salary=max(1, overall - 1) if company.sector == "service" else overall,
                        rating_culture=overall,
                        rating_growth=max(1, overall - 1) if company.sector == "service" else min(5, overall + 1),
                        rating_worklife=min(5, overall + 1) if company.sector in ("mnc_captive", "product") else max(1, overall - 1),
                        rating_management=overall,
                        pros=copy["pros"],
                        cons=copy["cons"],
                        advice_to_management="Invest in honest leveling and transparent pay bands. Engineers talk — secrecy erodes trust faster than bad quarters.",
                        would_rejoin=overall >= 4 and company.sector not in ("edtech",),
                        biggest_lie=copy["lie"],
                        is_verified=True,
                    )
                    reviews_created += 1

            self.stdout.write(self.style.SUCCESS(f"Reviews: {reviews_created} created"))

        layoffs_created = 0
        for name, status, role, location, details in LAYOFF_SIGNALS:
            try:
                company = Company.objects.get(name=name)
            except Company.DoesNotExist:
                continue
            if LayoffReport.objects.filter(company_name__iexact=name, status=status, details=details).exists():
                continue
            LayoffReport.objects.create(
                company=company,
                company_name=name,
                status=status,
                role_affected=role,
                location=location,
                details=details,
                is_verified=True,
            )
            layoffs_created += 1

        self.stdout.write(self.style.SUCCESS(f"Layoff signals: {layoffs_created} created"))

        synced = sync_all_company_stats()
        self.stdout.write(self.style.SUCCESS(f"Synced stats for {synced} companies"))

        from companies.indexing import indexable_companies_queryset, listable_companies_queryset

        self.stdout.write(
            f"\nDirectory totals: "
            f"{listable_companies_queryset().count()} listable companies, "
            f"{indexable_companies_queryset().count()} index-candidate companies, "
            f"{CompanyReview.objects.count()} reviews, "
            f"{SalarySubmission.objects.count()} salary points, "
            f"{LayoffReport.objects.count()} layoff reports"
        )
