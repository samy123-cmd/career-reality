"""
Seed Indian tech companies for Company Intelligence Hub.
Run: python manage.py shell < scripts/seed_companies.py
"""
import os, sys, django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from companies.models import Company

COMPANIES = [
    # IT Services
    {"name": "Tata Consultancy Services", "sector": "service", "size": "10001+", "headquarters": "Mumbai", "founded_year": 1968, "work_mode": "hybrid", "glassdoor_rating": 3.9, "ambitionbox_rating": 3.8, "description": "India's largest IT services company by revenue and market cap. Known for stable careers but slower growth curves."},
    {"name": "Infosys", "sector": "service", "size": "10001+", "headquarters": "Bangalore", "founded_year": 1981, "work_mode": "hybrid", "glassdoor_rating": 3.8, "ambitionbox_rating": 3.7, "description": "Tier-1 IT bellwether. Strong training program (Mysore campus) but variable team experience."},
    {"name": "Wipro", "sector": "service", "size": "10001+", "headquarters": "Bangalore", "founded_year": 1945, "work_mode": "hybrid", "glassdoor_rating": 3.7, "ambitionbox_rating": 3.5, "description": "Diversified IT services and consulting. Undergoing transformation under new leadership."},
    {"name": "HCLTech", "sector": "service", "size": "10001+", "headquarters": "Noida", "founded_year": 1976, "work_mode": "hybrid", "glassdoor_rating": 3.8, "ambitionbox_rating": 3.6, "description": "Strong in infrastructure management and engineering services. Known for Mode 1-2-3 strategy."},
    {"name": "Tech Mahindra", "sector": "service", "size": "10001+", "headquarters": "Pune", "founded_year": 1986, "work_mode": "hybrid", "glassdoor_rating": 3.6, "ambitionbox_rating": 3.4, "description": "Telecom-focused IT services. Part of Mahindra Group. Known for aggressive deal-making."},
    {"name": "Cognizant", "sector": "service", "size": "10001+", "headquarters": "Chennai", "founded_year": 1994, "work_mode": "hybrid", "glassdoor_rating": 3.8, "ambitionbox_rating": 3.6, "description": "US-headquartered but India-heavy IT services firm. Known for rapid hiring and variable project quality."},
    {"name": "LTIMindtree", "sector": "service", "size": "10001+", "headquarters": "Mumbai", "founded_year": 2022, "work_mode": "hybrid", "glassdoor_rating": 3.7, "ambitionbox_rating": 3.5, "description": "Merged entity of LTI and Mindtree under L&T Group. Growing mid-tier challenger."},

    # Product Companies
    {"name": "Flipkart", "sector": "ecommerce", "size": "10001+", "headquarters": "Bangalore", "founded_year": 2007, "work_mode": "hybrid", "glassdoor_rating": 3.9, "ambitionbox_rating": 4.0, "description": "India's largest e-commerce platform. Walmart-owned. Known for strong engineering culture and competitive pay."},
    {"name": "Razorpay", "sector": "bfsi", "size": "1001-5000", "headquarters": "Bangalore", "founded_year": 2014, "work_mode": "hybrid", "glassdoor_rating": 3.6, "ambitionbox_rating": 3.8, "description": "Leading Indian payments infrastructure company. Known for fast-paced fintech culture."},
    {"name": "Zerodha", "sector": "bfsi", "size": "201-1000", "headquarters": "Bangalore", "founded_year": 2010, "work_mode": "office", "glassdoor_rating": 3.8, "ambitionbox_rating": 4.1, "description": "India's largest retail stockbroker. Bootstrapped. Known for lean team and strong tech culture."},
    {"name": "PhonePe", "sector": "bfsi", "size": "5001-10000", "headquarters": "Bangalore", "founded_year": 2015, "work_mode": "hybrid", "glassdoor_rating": 3.7, "ambitionbox_rating": 3.9, "description": "UPI payments leader. Walmart-backed. Known for high-growth fintech culture."},
    {"name": "CRED", "sector": "bfsi", "size": "201-1000", "headquarters": "Bangalore", "founded_year": 2018, "work_mode": "office", "glassdoor_rating": 3.5, "ambitionbox_rating": 3.8, "description": "Credit card rewards platform. Known for premium brand but debated unit economics."},
    {"name": "Freshworks", "sector": "product", "size": "5001-10000", "headquarters": "Chennai", "founded_year": 2010, "work_mode": "hybrid", "glassdoor_rating": 3.7, "ambitionbox_rating": 3.8, "description": "SaaS company (CRM, ITSM). NASDAQ-listed. Chennai's flagship tech product company."},
    {"name": "Zoho", "sector": "product", "size": "10001+", "headquarters": "Chennai", "founded_year": 1996, "work_mode": "office", "glassdoor_rating": 4.0, "ambitionbox_rating": 4.1, "description": "Bootstrapped SaaS giant with 55+ products. Known for rural development centers and no-VC model."},
    {"name": "Postman", "sector": "product", "size": "201-1000", "headquarters": "Bangalore", "founded_year": 2014, "work_mode": "hybrid", "glassdoor_rating": 4.1, "ambitionbox_rating": 4.2, "description": "API development platform used by 30M+ developers. YC-backed, strong engineering culture."},

    # Unicorns / Startups
    {"name": "Zomato", "sector": "ecommerce", "size": "5001-10000", "headquarters": "Gurugram", "founded_year": 2008, "work_mode": "hybrid", "glassdoor_rating": 3.5, "ambitionbox_rating": 3.6, "description": "Food delivery and quick commerce (Blinkit). Public company. Known for aggressive culture."},
    {"name": "Swiggy", "sector": "ecommerce", "size": "5001-10000", "headquarters": "Bangalore", "founded_year": 2014, "work_mode": "hybrid", "glassdoor_rating": 3.6, "ambitionbox_rating": 3.5, "description": "Food delivery and quick commerce (Instamart). Known for fast-paced execution culture."},
    {"name": "Meesho", "sector": "ecommerce", "size": "1001-5000", "headquarters": "Bangalore", "founded_year": 2015, "work_mode": "hybrid", "glassdoor_rating": 3.4, "ambitionbox_rating": 3.5, "description": "Social commerce platform for Tier 2-3 India. Known for high growth but burnout concerns."},
    {"name": "Ola", "sector": "other", "size": "5001-10000", "headquarters": "Bangalore", "founded_year": 2010, "work_mode": "office", "glassdoor_rating": 3.3, "ambitionbox_rating": 3.2, "description": "Ride-hailing and EV company. Known for founder-driven culture and pivot to electric vehicles."},
    {"name": "Paytm", "sector": "bfsi", "size": "10001+", "headquarters": "Noida", "founded_year": 2010, "work_mode": "office", "glassdoor_rating": 3.4, "ambitionbox_rating": 3.3, "description": "Fintech and digital payments. Public company. Known for regulatory challenges and pivot cycles."},
    {"name": "Byju's", "sector": "edtech", "size": "5001-10000", "headquarters": "Bangalore", "founded_year": 2011, "work_mode": "office", "glassdoor_rating": 3.0, "ambitionbox_rating": 2.8, "description": "Once India's most valuable edtech startup. Known for aggressive sales culture and financial distress."},
    {"name": "Unacademy", "sector": "edtech", "size": "1001-5000", "headquarters": "Bangalore", "founded_year": 2015, "work_mode": "hybrid", "glassdoor_rating": 3.2, "ambitionbox_rating": 3.0, "description": "EdTech platform for competitive exam prep. Known for layoff cycles and pivot from live to recorded."},

    # MNC Captives / Big Tech India
    {"name": "Google India", "sector": "mnc_captive", "size": "10001+", "headquarters": "Bangalore", "founded_year": 2004, "work_mode": "hybrid", "glassdoor_rating": 4.4, "ambitionbox_rating": 4.5, "description": "Top tier compensation and engineering culture. Hyderabad and Bangalore offices. Extremely selective hiring."},
    {"name": "Microsoft India", "sector": "mnc_captive", "size": "10001+", "headquarters": "Hyderabad", "founded_year": 1990, "work_mode": "hybrid", "glassdoor_rating": 4.3, "ambitionbox_rating": 4.4, "description": "Largest MNC engineering center in India. Known for work-life balance and Azure/AI growth."},
    {"name": "Amazon India", "sector": "mnc_captive", "size": "10001+", "headquarters": "Bangalore", "founded_year": 2004, "work_mode": "office", "glassdoor_rating": 3.9, "ambitionbox_rating": 3.8, "description": "Massive engineering, retail, and AWS presence. Known for high bar, PIP culture, and competitive RSU packages."},
    {"name": "Goldman Sachs India", "sector": "bfsi", "size": "5001-10000", "headquarters": "Bangalore", "founded_year": 2004, "work_mode": "office", "glassdoor_rating": 4.0, "ambitionbox_rating": 4.1, "description": "Major GCC for Goldman Sachs. Strong compensation for fintech roles. Known for long hours."},
    {"name": "Atlassian India", "sector": "product", "size": "1001-5000", "headquarters": "Bangalore", "founded_year": 2005, "work_mode": "remote", "glassdoor_rating": 4.2, "ambitionbox_rating": 4.3, "description": "TEAM Anywhere policy — fully distributed. Strong DevOps/Agile tooling maker. Premium compensation."},
    {"name": "Adobe India", "sector": "mnc_captive", "size": "5001-10000", "headquarters": "Noida", "founded_year": 1997, "work_mode": "hybrid", "glassdoor_rating": 4.3, "ambitionbox_rating": 4.4, "description": "India's largest R&D center for Adobe. Known for excellent work-life balance and creative culture."},
    {"name": "Uber India", "sector": "mnc_captive", "size": "1001-5000", "headquarters": "Bangalore", "founded_year": 2013, "work_mode": "hybrid", "glassdoor_rating": 4.0, "ambitionbox_rating": 3.9, "description": "Key engineering hub for Uber. Strong compensation and scale challenges. Known for data-driven culture."},

    # HealthTech / Other
    {"name": "Practo", "sector": "healthtech", "size": "201-1000", "headquarters": "Bangalore", "founded_year": 2008, "work_mode": "hybrid", "glassdoor_rating": 3.5, "ambitionbox_rating": 3.4, "description": "India's largest health-tech platform. Connecting patients with doctors. Profitable but slow-growing."},
    {"name": "PharmEasy", "sector": "healthtech", "size": "1001-5000", "headquarters": "Mumbai", "founded_year": 2015, "work_mode": "hybrid", "glassdoor_rating": 3.3, "ambitionbox_rating": 3.2, "description": "Online pharmacy and diagnostics. Known for aggressive expansion and valuation questions."},
    {"name": "Nykaa", "sector": "ecommerce", "size": "1001-5000", "headquarters": "Mumbai", "founded_year": 2012, "work_mode": "office", "glassdoor_rating": 3.4, "ambitionbox_rating": 3.3, "description": "Beauty and fashion e-commerce. Public company. Known for strong brand but tech team churn."},
    {"name": "Dream11", "sector": "other", "size": "201-1000", "headquarters": "Mumbai", "founded_year": 2008, "work_mode": "office", "glassdoor_rating": 3.8, "ambitionbox_rating": 4.0, "description": "India's largest fantasy sports platform. Profitable unicorn. Known for lean team and high comp."},
    {"name": "Groww", "sector": "bfsi", "size": "1001-5000", "headquarters": "Bangalore", "founded_year": 2016, "work_mode": "hybrid", "glassdoor_rating": 3.7, "ambitionbox_rating": 3.8, "description": "Investment and trading platform challenging Zerodha. Known for rapid growth and young team."},
    {"name": "Juspay", "sector": "bfsi", "size": "201-1000", "headquarters": "Bangalore", "founded_year": 2012, "work_mode": "office", "glassdoor_rating": 3.6, "ambitionbox_rating": 3.7, "description": "Payment orchestration platform behind many UPI apps. Known for Haskell/FP engineering culture."},
]

created = 0
skipped = 0
for data in COMPANIES:
    name = data["name"]
    if Company.objects.filter(name=name).exists():
        skipped += 1
        continue
    Company.objects.create(**data, is_verified=True)
    created += 1

print(f"Done: {created} companies created, {skipped} skipped (already exist)")
print(f"Total companies: {Company.objects.count()}")
