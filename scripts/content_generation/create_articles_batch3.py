"""Batch 3: Data Science, Career Strategy, Software Eng, Product Mgmt, Marketing, Design, Financial Reality"""
import os
os.environ['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'postgresql://postgres.iakuzoeqdjkutpgettlx:<YOUR_SUPABASE_PASSWORD>@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()
from content.models import Article, Category, Author
from django.utils import timezone
author = Author.objects.first()

articles = [
    {
        "category_slug": "data-science",
        "title": "The Data Science Bubble: Why 80% of Data Scientists Do Excel Work",
        "slug": "data-science-bubble-excel-work-reality",
        "meta_title": "Data Science Reality: ML or Fancy Excel?",
        "meta_description": "The gap between data science dreams and reality. Most roles are SQL and dashboards, not ML models.",
        "target_persona": "You enrolled in that ML bootcamp dreaming of building AI. Now you wonder why job descriptions ask for SQL and Tableau. You need the real picture.",
        "who_should_avoid": "If you work at a FAANG company building actual ML systems, this does not apply to you. You are in the 5% doing real data science.",
        "common_expectation": """**The Data Science Dream:**
- Build AI/ML models that change the world
- Work on cutting-edge algorithms
- Six-figure salary for writing Python
- Be the smartest person in the room

**What Bootcamps Sell:**
Learn TensorFlow, build neural networks, become a data scientist in 6 months. Jobs everywhere. Companies desperate for talent.""",
        "actual_reality": """**Reality Check:**

<div class="chart-container">
<h4>📊 What Data Scientists Actually Do (Time Split)</h4>
<table class="data-table">
<tr><th>Activity</th><th>Expectation</th><th>Reality</th></tr>
<tr><td>Building ML Models</td><td>50%</td><td>10%</td></tr>
<tr><td>Data Cleaning</td><td>10%</td><td>40%</td></tr>
<tr><td>SQL Queries</td><td>5%</td><td>25%</td></tr>
<tr><td>Dashboards/Reports</td><td>5%</td><td>15%</td></tr>
<tr><td>Meetings</td><td>10%</td><td>10%</td></tr>
</table>
</div>

**The Title Inflation Problem:**

Many companies renamed Data Analyst to Data Scientist for recruitment purposes. Same job, fancier title, higher salary expectations from candidates who then get disappointed.""",
        "salary_reality": """**The Salary Reality:**

<div class="chart-container">
<h4>💰 Data Science Salaries by Actual Work</h4>
<table class="data-table">
<tr><th>Role Type</th><th>0-2 Yrs</th><th>3-5 Yrs</th><th>6+ Yrs</th></tr>
<tr><td>Real ML Engineer</td><td>Rs 15 LPA</td><td>Rs 30 LPA</td><td>Rs 50+ LPA</td></tr>
<tr><td>DS (mostly analysis)</td><td>Rs 8 LPA</td><td>Rs 15 LPA</td><td>Rs 25 LPA</td></tr>
<tr><td>Analyst with DS title</td><td>Rs 6 LPA</td><td>Rs 12 LPA</td><td>Rs 18 LPA</td></tr>
</table>
</div>""",
        "stuck_point": """**Where DS Aspirants Get Stuck:**
1. Learn fancy algorithms, cannot write production code
2. Build models, never deployed anything
3. Kaggle medals, zero business understanding
4. Know Python, struggle with SQL interviews

**The Fix:** Focus on deployment, SQL, and business metrics before deep learning.""",
        "verdict": """**Honest Assessment:**
Data Science is real but rare. Most DS jobs are analysis jobs. If you love data, that is fine. If you want ML, aim for ML Engineer roles at tech companies specifically. The rest is glorified Excel."""
    },
    {
        "category_slug": "career-strategy",
        "title": "The Networking Myth: Why Most Professional Relationships Are Worthless",
        "slug": "networking-myth-professional-relationships-worthless",
        "meta_title": "Networking Reality: Quantity vs Quality",
        "meta_description": "Why 500+ LinkedIn connections mean nothing. Real networking strategies that actually create career value.",
        "target_persona": "You attend networking events, collect business cards, add people on LinkedIn, but nothing ever comes from it. You follow advice to network more but see no results.",
        "who_should_avoid": "If networking has directly gotten you jobs or clients, you already know what works. This is for people doing it wrong.",
        "common_expectation": """**The Networking Fantasy:**
- More connections = More opportunities
- Attend events = Get referred
- LinkedIn connections = Professional network
- Your network is your net worth

**What Gurus Say:**
Network relentlessly. Add everyone. Stay connected. Opportunities will flow.""",
        "actual_reality": """**The Numbers:**

<div class="chart-container">
<h4>📊 Networking Activity vs Outcomes</h4>
<table class="data-table">
<tr><th>Activity</th><th>Time Spent/Month</th><th>Actual Referrals/Year</th></tr>
<tr><td>Random LinkedIn adding</td><td>5 hours</td><td>0</td></tr>
<tr><td>Networking events</td><td>10 hours</td><td>0-1</td></tr>
<tr><td>Deep 1-on-1 relationships</td><td>5 hours</td><td>3-5</td></tr>
<tr><td>Helping others publicly</td><td>3 hours</td><td>2-4</td></tr>
</table>
</div>

**Why Most Networking Fails:**
You contact people only when you need something. That is not networking. That is begging.""",
        "salary_reality": """**Where Real Career Value Comes From:**

<div class="chart-container">
<h4>💰 Career Opportunities by Source</h4>
<table class="data-table">
<tr><th>Source</th><th>% of Great Opportunities</th></tr>
<tr><td>Close professional friends (5-10 people)</td><td>40%</td></tr>
<tr><td>Direct application</td><td>25%</td></tr>
<tr><td>Weak ties (acquaintances)</td><td>20%</td></tr>
<tr><td>Random LinkedIn</td><td>5%</td></tr>
<tr><td>Networking events</td><td>5%</td></tr>
</table>
</div>

5-10 deep relationships beat 500 shallow connections.""",
        "stuck_point": """**The Networking Trap:**
1. Collect contacts, never nurture them
2. Only reach out when job hunting
3. Take but never give
4. Quantity over quality

**Real Networking:**
- Help 5 people before asking for 1 thing
- Stay in touch when you do not need anything
- Create value before extracting value
- Depth over breadth""",
        "verdict": """**The Truth:**
Your network matters, but 90% of what people call networking is useless activity theater. Build 10 real relationships instead of 1000 fake ones."""
    },
    {
        "category_slug": "software-engineering",
        "title": "The 10x Developer Myth: Why Productivity Worship Is Killing Careers",
        "slug": "10x-developer-myth-productivity-killing-careers",
        "meta_title": "10x Developer Myth: Hustle Culture Reality",
        "meta_description": "The truth about developer productivity myths. Why obsessing over output destroys sustainable careers.",
        "target_persona": "You feel inadequate comparing yourself to Twitter developers who ship 5 side projects. You work overtime but still feel behind. You need perspective.",
        "who_should_avoid": "If you have healthy work boundaries and do not compare yourself to internet personalities, you are fine.",
        "common_expectation": """**The 10x Myth:**
- Some developers are 10x more productive
- Hustle harder to compete
- Side projects prove passion
- Always be coding

**Tech Twitter Reality:**
Everyone shipping features, launching products, posting threads about productivity.""",
        "actual_reality": """**The Research Says:**

<div class="chart-container">
<h4>📊 Developer Productivity Reality</h4>
<table class="data-table">
<tr><th>Metric</th><th>Top 20%</th><th>Average</th><th>Difference</th></tr>
<tr><td>Lines of Code</td><td>200/day</td><td>100/day</td><td>2x not 10x</td></tr>
<tr><td>Bugs Shipped</td><td>3/month</td><td>8/month</td><td>2.5x better</td></tr>
<tr><td>Features Delivered</td><td>4/sprint</td><td>2/sprint</td><td>2x not 10x</td></tr>
</table>
</div>

The 10x number comes from extreme outliers in specific contexts, not general reality.""",
        "salary_reality": """**What Actually Gets Paid:**

<div class="chart-container">
<h4>💰 Developer Salary vs Productivity Style</h4>
<table class="data-table">
<tr><th>Style</th><th>Salary</th><th>Burnout Risk</th></tr>
<tr><td>Sustainable Performer</td><td>Rs 25 LPA</td><td>Low</td></tr>
<tr><td>Chronic Hustler</td><td>Rs 28 LPA</td><td>High</td></tr>
<tr><td>Strategic Communicator</td><td>Rs 35 LPA</td><td>Low</td></tr>
</table>
</div>

The developer who communicates well earns more than the one who codes more.""",
        "stuck_point": """**The Hustle Trap:**
1. Compare to curated internet personas
2. Work overtime, burn out, repeat
3. Side projects over rest
4. Productivity guilt on weekends

**The Fix:** Consistent moderate effort beats burnout cycles. Sleep, exercise, and relationships make better developers.""",
        "verdict": """**Reality Check:**
10x developers are mostly a myth used to justify exploitation. Build sustainable habits. The developers with 20-year careers did not burn bright and flame out at 30."""
    },
    {
        "category_slug": "product-management",
        "title": "The PM Prestige Trap: Why Product Management Is Not Your Escape From Engineering",
        "slug": "pm-prestige-trap-escape-from-engineering",
        "meta_title": "PM Reality: Escape From Engineering?",
        "meta_description": "Why switching to PM often disappoints. The grass is not greener on the product side.",
        "target_persona": "You are an engineer tired of coding, thinking PM is the answer. Or you are considering PM because it seems more prestigious. You need reality.",
        "who_should_avoid": "If you genuinely love customer problems and strategy over building things, PM might be right for you.",
        "common_expectation": """**The PM Dream:**
- Lead without managing people
- More money than engineering
- Strategic, high-level work
- Escape from coding

**What PM Courses Sell:**
Be the CEO of the product. Make the big decisions. Engineers build what you envision.""",
        "actual_reality": """**PM Reality:**

<div class="chart-container">
<h4>📊 PM Time Breakdown</h4>
<table class="data-table">
<tr><th>Activity</th><th>Expectation</th><th>Reality</th></tr>
<tr><td>Strategy</td><td>40%</td><td>10%</td></tr>
<tr><td>Meetings</td><td>20%</td><td>50%</td></tr>
<tr><td>Documentation</td><td>10%</td><td>25%</td></tr>
<tr><td>Firefighting</td><td>5%</td><td>15%</td></tr>
</table>
</div>

PM is 50% meetings. If you hate coordination and politics, you will hate PM.""",
        "salary_reality": """**PM vs Engineering Salary:**

<div class="chart-container">
<h4>💰 Career Trajectory Comparison</h4>
<table class="data-table">
<tr><th>Years</th><th>Engineer</th><th>PM</th></tr>
<tr><td>0-3</td><td>Rs 10-18 LPA</td><td>Rs 12-20 LPA</td></tr>
<tr><td>4-7</td><td>Rs 20-35 LPA</td><td>Rs 25-40 LPA</td></tr>
<tr><td>8+</td><td>Rs 35-60 LPA</td><td>Rs 40-70 LPA</td></tr>
</table>
</div>

The premium is not dramatic. And engineering has consulting and freelance options PM does not.""",
        "stuck_point": """**Common PM Regrets:**
1. No concrete output - harder to see your impact
2. Responsibility without authority frustrates
3. Politics is higher, not lower
4. Hard to switch back to engineering

**Before Switching:** Try internal PM rotation first. Talk to 5 PMs about daily reality.""",
        "verdict": """**Honest Take:**
PM is great for people who love customers and coordination. It is terrible for people escaping engineering. The problems are different, not fewer."""
    },
    {
        "category_slug": "marketing",
        "title": "The Digital Marketing Illusion: Why Your Instagram Ads Are Burning Money",
        "slug": "digital-marketing-illusion-instagram-ads-burning-money",
        "meta_title": "Digital Marketing Reality: ROI Truth",
        "meta_description": "Why most digital marketing spend is wasted. Data on what actually works and what is theater.",
        "target_persona": "You are boosting posts, running ads, tracking vanity metrics, but sales are flat. You need to understand what is actually working.",
        "who_should_avoid": "If you have clear attribution and proven ROI, you know your numbers already.",
        "common_expectation": """**The Marketing Promise:**
- Digital is measurable unlike traditional
- Scale with ad spend
- Viral potential
- Attribution clarity

**What Agencies Sell:**
Impressions, reach, engagement, followers. Dashboards full of growing numbers.""",
        "actual_reality": """**The Reality:**

<div class="chart-container">
<h4>📊 Marketing Channel ROI (Actual Data)</h4>
<table class="data-table">
<tr><th>Channel</th><th>Claimed ROI</th><th>Typical Actual ROI</th></tr>
<tr><td>Instagram Boosting</td><td>5-10x</td><td>0.5-2x</td></tr>
<tr><td>Google Ads (SMBs)</td><td>4x</td><td>1-3x</td></tr>
<tr><td>Influencer Marketing</td><td>10x</td><td>0-3x</td></tr>
<tr><td>Content/SEO</td><td>5x</td><td>3-8x (long term)</td></tr>
</table>
</div>

Most ad spend is wasted on awareness that never converts.""",
        "salary_reality": """**Marketing Career Reality:**

<div class="chart-container">
<h4>💰 Marketing Salary by Specialty</h4>
<table class="data-table">
<tr><th>Role</th><th>Entry</th><th>Mid</th><th>Senior</th></tr>
<tr><td>Social Media</td><td>Rs 4 LPA</td><td>Rs 8 LPA</td><td>Rs 15 LPA</td></tr>
<tr><td>Performance Mktg</td><td>Rs 6 LPA</td><td>Rs 12 LPA</td><td>Rs 25 LPA</td></tr>
<tr><td>Growth Lead</td><td>Rs 10 LPA</td><td>Rs 20 LPA</td><td>Rs 40 LPA</td></tr>
</table>
</div>

Performance and growth roles pay more because they tie to revenue.""",
        "stuck_point": """**Marketing Traps:**
1. Vanity metrics that feel good but do not convert
2. Platform lock-in with zero owned audience
3. Agency reports designed to justify their fee
4. Following trends instead of testing

**Focus On:** Revenue attribution, owned channels, long-term content.""",
        "verdict": """**The Bottom Line:**
80% of marketing spend is wasted. The winners know exactly which 20% works. Build measurement first, then scale what proves ROI."""
    },
    {
        "category_slug": "design",
        "title": "The UX Salary Myth: Why Design Careers Plateau Faster Than You Think",
        "slug": "ux-salary-myth-design-careers-plateau",
        "meta_title": "UX Design Salary Reality Check",
        "meta_description": "Why design careers hit ceiling early. Data on design salaries, paths forward, and the management trap.",
        "target_persona": "You are 5 years into design wondering why salaries seem stuck while engineering friends keep growing. You want honest data.",
        "who_should_avoid": "If you are at a FAANG making Staff Designer money, you have already cleared the plateau.",
        "common_expectation": """**The Design Dream:**
- Creative work that pays well
- Growing demand for UX
- Path to VP of Design
- Design is valued as much as engineering

**What Design Courses Say:**
UX is booming. Companies need designers. Six-figure salaries. Creative and lucrative.""",
        "actual_reality": """**Salary Reality:**

<div class="chart-container">
<h4>📊 Design vs Engineering Salary Curves</h4>
<table class="data-table">
<tr><th>Years</th><th>Designer</th><th>Engineer</th></tr>
<tr><td>0-3</td><td>Rs 6 LPA</td><td>Rs 8 LPA</td></tr>
<tr><td>4-7</td><td>Rs 12 LPA</td><td>Rs 22 LPA</td></tr>
<tr><td>8-12</td><td>Rs 18 LPA</td><td>Rs 35 LPA</td></tr>
<tr><td>13+</td><td>Rs 25 LPA</td><td>Rs 50 LPA</td></tr>
</table>
</div>

The gap widens with experience. Design teams are smaller, so fewer senior roles exist.""",
        "salary_reality": """**Where Design Money Is:**

<div class="chart-container">
<h4>💰 Design Specialization Salaries</h4>
<table class="data-table">
<tr><th>Specialty</th><th>Junior</th><th>Senior</th><th>Lead</th></tr>
<tr><td>Visual/UI</td><td>Rs 5 LPA</td><td>Rs 12 LPA</td><td>Rs 18 LPA</td></tr>
<tr><td>UX/Research</td><td>Rs 6 LPA</td><td>Rs 15 LPA</td><td>Rs 24 LPA</td></tr>
<tr><td>Product Design</td><td>Rs 8 LPA</td><td>Rs 18 LPA</td><td>Rs 30 LPA</td></tr>
<tr><td>Design Management</td><td>-</td><td>Rs 25 LPA</td><td>Rs 45 LPA</td></tr>
</table>
</div>""",
        "stuck_point": """**Design Career Traps:**
1. Staying pure IC when management pays more
2. Generalist at companies that need specialists
3. Portfolio polish over business impact
4. Design purist in business-first companies

**Moving Up:** Learn business metrics. Show revenue impact. Consider management.""",
        "verdict": """**The Reality:**
Design careers plateau earlier than engineering. To break through: specialize in high-demand areas, show business impact, or move into management. Pure design IC roles have lower ceilings."""
    },
    {
        "category_slug": "financial-reality",
        "title": "The Home Loan Trap: Why Your Dream House Might Be Your Financial Prison",
        "slug": "home-loan-trap-dream-house-financial-prison",
        "meta_title": "Home Loan Reality: Dream or Trap?",
        "meta_description": "The math on home ownership nobody shows you. When buying makes sense and when it destroys wealth.",
        "target_persona": "Parents pressuring you to buy. EMI calculators showing affordable numbers. You need someone to show you the complete picture.",
        "who_should_avoid": "If you bought at the right time, right price, and can afford it easily, this is not about you.",
        "common_expectation": """**The Home Ownership Dream:**
- Rent is throwing money away
- Real estate always appreciates
- Own home = Financial security
- It is what responsible adults do

**What EMI Calculators Show:**
Rs 50,000/month for a Rs 80 lakh house. Affordable on your Rs 1.2 lakh salary. Done.""",
        "actual_reality": """**The Hidden Costs:**

<div class="chart-container">
<h4>📊 True Cost of Rs 80 Lakh Home</h4>
<table class="data-table">
<tr><th>Cost Component</th><th>Amount</th></tr>
<tr><td>Property Price</td><td>Rs 80 lakhs</td></tr>
<tr><td>Registration/Stamp Duty</td><td>Rs 6 lakhs</td></tr>
<tr><td>Interest (20 yrs 8.5%)</td><td>Rs 78 lakhs</td></tr>
<tr><td>Maintenance (20 yrs)</td><td>Rs 12 lakhs</td></tr>
<tr><td>Furnishing</td><td>Rs 5 lakhs</td></tr>
<tr><th>TOTAL COST</th><th>Rs 1.81 Cr</th></tr>
</table>
</div>

Your Rs 80 lakh house costs Rs 1.81 crores. That is the number nobody shows you.""",
        "salary_reality": """**Rent vs Buy Math (20 Year Comparison):**

<div class="chart-container">
<h4>💰 Financial Outcome Scenarios</h4>
<table class="data-table">
<tr><th>Scenario</th><th>Monthly Cost</th><th>Wealth at Year 20</th></tr>
<tr><td>Buy (EMI 50k)</td><td>Rs 50,000</td><td>Rs 1.2 Cr (house value)</td></tr>
<tr><td>Rent + Invest</td><td>Rs 25k rent, 25k invest</td><td>Rs 2.4 Cr (portfolio)</td></tr>
</table>
</div>

If you rent cheaper and invest the difference, you often end up wealthier.""",
        "stuck_point": """**When People Get Trapped:**
1. Buying at peak prices due to FOMO
2. Stretching EMI to 50% of salary
3. Buying before career is stable
4. Buying in city they might leave

**Smart Home Buying:**
- EMI under 30% of take-home
- 5+ years in same city planned
- 20% downpayment saved
- Emergency fund intact after purchase""",
        "verdict": """**The Truth:**
Home ownership is emotional, not always financial. The math often favors renting. Buy when you genuinely want stability and can comfortably afford it. Not because parents or society pressures you."""
    }
]

print("Creating batch 3 articles (7 remaining categories)...")
for data in articles:
    cat = Category.objects.get(slug=data["category_slug"])
    if Article.objects.filter(slug=data["slug"]).exists():
        print(f"  Skip: {data['title'][:40]}...")
        continue
    Article.objects.create(
        title=data["title"], slug=data["slug"], author=author, category=cat,
        status="published", target_persona=data["target_persona"],
        who_should_avoid=data["who_should_avoid"],
        common_expectation=data["common_expectation"],
        actual_reality=data["actual_reality"],
        salary_reality=data["salary_reality"],
        stuck_point=data["stuck_point"], verdict=data["verdict"],
        meta_title=data["meta_title"], meta_description=data["meta_description"],
        published_at=timezone.now()
    )
    print(f"  Created: {data['title'][:40]}...")
print("Batch 3 done!")
print(f"\nTotal articles: {Article.objects.count()}")
