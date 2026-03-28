import os
import django
import datetime
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Author, Category, Article

# Ensure Author exists
author, _ = Author.objects.get_or_create(
    name="P. Mishra",
    defaults={
        "display_name": "P. Mishra",
        "bio": "Senior Editor. 12 Years in Tech Strategy.",
        "linkedin_url": "https://linkedin.com/in/example",
        "is_active": True
    }
)

def create_article(cat_name, slug, title, persona, avoid, expect, reality, salary, stuck_point, verdict, seo_desc):
    category, _ = Category.objects.get_or_create(name=cat_name, defaults={"slug":  cat_name.lower().replace(" ", "-"), "order": 1})
    
    Article.objects.update_or_create(
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
            "stuck_point": stuck_point,
            "verdict": verdict,
            "meta_title": title[:60],
            "meta_description": seo_desc[:160],
            "published_at": timezone.now(),
            "last_reality_check": datetime.date.today(),
        }
    )
    print(f"Processed: {title}")

# ==========================================
# 1. GOLD STANDARD ESSAYS (Already Done)
# ==========================================

# 1. The 7-Year Plateau
create_article(
    cat_name="Career Strategy",
    slug="7-year-career-plateau-india",
    title="The 7-Year Career Plateau Nobody Warns You About",
    persona="Mid-level professionals (5-8 years exp) feeling stuck despite good performance.",
    avoid="People who think 'loyalty' to a company pays off in the long run. If you are waiting for a promotion to be 'handed' to you, stop reading.",
    expect="I will keep getting 15-20% hikes, get promoted to Manager, and eventually become a Director by just doing my job well.",
    reality="Growth is not linear; it is logarithmic.<br><br>After 7 years, you hit the 'Seniority Trap'. You are too expensive to do grunt work, but not strategic enough to drive P&L.<br><br>Companies stop paying for 'potential' and start paying only for 'proven impact'. The automatic hikes stop. You are now competing with 24-year-olds who are faster than you and 35-year-olds who are smarter than you.",
    salary="""
    <table class="editorial-table">
        <thead>
            <tr>
                <th style="width: 30%">Role</th>
                <th style="width: 20%">Exp</th>
                <th style="width: 30%">Realistic Pay (LPA)</th>
                <th style="width: 20%">Growth Potential</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Senior Eng</td>
                <td>5-7 Yrs</td>
                <td>
                    25.0 - 45.0
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 60%"></div></div>
                </td>
                <td>High</td>
            </tr>
            <tr>
                <td>Tech Lead</td>
                <td>7-10 Yrs</td>
                <td>
                    30.0 - 55.0
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 80%"></div></div>
                </td>
                <td>Medium</td>
            </tr>
            <tr>
                <td>Plateau Zone</td>
                <td>8+ Yrs</td>
                <td>
                    STAGNANT
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 40%; background: #999;"></div></div>
                </td>
                <td>Low (Inflation Only)</td>
            </tr>
        </tbody>
    </table>
    <p style="font-size: 13px; color: #999; margin-top: 1rem;">*Visual Scale: Relative earning power in current market.</p>
    """,
    stuck_point="The 'Doer' Mindset.<br><br>You are stuck because you are still optimizing for 'Execution' (doing tasks well) when the game has switched to 'Leverage' (enabling others/strategy).",
    verdict="You must choose: Become a deep Specialist (top 1% skills) or a ruthless Politician (Management). The middle ground is a slow death.",
    seo_desc="The truth about the mid-career crisis in Indian tech. Why salaries stagnate after 7 years and how to break the plateau."
)

# 2. 20 LPA Reality
create_article(
    cat_name="Money Reality",
    slug="what-20-LPA-feels-like-india",
    title="What ₹20 LPA Actually Feels Like in India",
    persona="Young professionals chasing the '20 LPA' milestone thinking it means wealth.",
    avoid="Anyone who thinks earning ₹1.5L/month means you can buy a luxury car and a 3BHK simultaneously.",
    expect="I will be rich. I will fly business class, eat out daily, and save huge amounts for early retirement.",
    reality="₹20 LPA is the new ₹10 LPA.<br><br>In-hand is ~₹1.2L after taxes. <br>- Rent (Metro City): ₹35k <br>- EMIs (Car/Edu): ₹25k <br>- Lifestyle/Food: ₹30k <br><br>You are left with ₹30k savings. One medical emergency or family obligation wipes it out.<br><br>You are comfortable, but you are not rich. You are strictly middle class with better Instagram photos.",
    salary="""
    <table class="editorial-table">
        <thead>
            <tr>
                <th style="width: 25%">CTC</th>
                <th style="width: 25%">In-Hand</th>
                <th style="width: 50%">Lifestyle Tier</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>10 LPA</td>
                <td>₹70k</td>
                <td>
                    Survival (Metro)
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 30%"></div></div>
                </td>
            </tr>
            <tr>
                <td>20 LPA</td>
                <td>₹1.2L</td>
                <td>
                    Comfortable Middle
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 60%"></div></div>
                </td>
            </tr>
            <tr>
                <td>50 LPA</td>
                <td>₹2.8L</td>
                <td>
                    Upper Middle
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 100%"></div></div>
                </td>
            </tr>
        </tbody>
    </table>
    <p style="font-size: 13px; color: #999; margin-top: 1rem;">*Real wealth starts at ₹50 LPA or equity ownership.</p>
    """,
    stuck_point="Lifestyle Inflation.<br><br>As soon as you hit 20 LPA, you upgrade your flat, buy an iPhone Pro, and get a car. Your savings rate often *drops* because your desires grow faster than your post-tax income.",
    verdict="Stop celebrating the CTC number. Calculate your 'Savings Rate'. If you aren't saving 50% of your in-hand, you are poor.",
    seo_desc="Breaking the illusion of the 20 LPA salary in India. Taxes, cost of living, and why it doesn't feel like wealth anymore."
)

# 3. Upskilling Trap
create_article(
    cat_name="Learning",
    slug="why-upskilling-stops-working",
    title="Why 'Upskilling' Stops Working After a Point",
    persona="Course-collectors with 25 certifications on LinkedIn but no promotion.",
    avoid="People who think completing a Coursera course counts as 'experience'.",
    expect="If I learn AI, Blockchain, and Rust, my market value will double instantly.",
    reality="In the first 3 years, skills matter. In the next 20 years, **Judgment** matters.<br><br>No CTO hires a Senior Architect because they have a Udemy certificate. They hire them because they know *when not to use* a technology.<br><br>Upskilling becomes a procrastination tool to avoid doing the hard work of solving messy, ambiguous business problems.",
    salary="""
    <table class="editorial-table">
        <thead>
            <tr>
                <th style="width: 30%">Career Stage</th>
                <th style="width: 40%">Impact of 'Upskilling'</th>
                <th style="width: 30%">Market Value</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Years 0-3</td>
                <td>High (Critical)</td>
                <td>
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 90%"></div></div>
                </td>
            </tr>
            <tr>
                <td>Years 4-10</td>
                <td>Low (Diminishing)</td>
                <td>
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 40%"></div></div>
                </td>
            </tr>
            <tr>
                <td>Years 10+</td>
                <td>Zero (Outcomes only)</td>
                <td>
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 10%"></div></div>
                </td>
            </tr>
        </tbody>
    </table>
    """,
    stuck_point="The 'Student' Identity.<br><br>You keep trying to 'learn' your way to a promotion, but your boss wants you to 'lead' your way to one. They are different skill sets.",
    verdict="Stop taking courses. Start shipping projects. Real learning happens in production, not in a sandbox.",
    seo_desc="Why certifications and upskilling lose value as you grow senior. The shift from hard skills to judgment."
)

# 4. IT Services Cost
create_article(
    cat_name="Career Strategy",
    slug="hidden-cost-it-services-india",
    title="The Hidden Cost of Staying in IT Services Too Long",
    persona="Employees at TCS/Infosys/Wipro/Accenture with 5+ years tenure.",
    avoid="People who value 'Job Safety' above all else and fear interviews.",
    expect="This job is safe. I have on-site opportunities. I will retire here comfortably.",
    reality="Service companies optimize for 'Billability', not 'Capability'.<br><br>You are likely using legacy tech (Java 8, older .NET) that the rest of the world abandoned 5 years ago.<br><br>The longer you stay, the more 'unhirable' you become to product companies. You are building 'Tenure', not 'Experience'.",
    salary="""
    <table class="editorial-table">
        <thead>
            <tr>
                <th style="width: 30%">Year</th>
                <th style="width: 35%">Service Co Hike</th>
                <th style="width: 35%">Product Co Hike</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Year 1</td>
                <td>3-5%</td>
                <td>15-30% <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 30%"></div></div></td>
            </tr>
            <tr>
                <td>Year 5</td>
                <td>5-8%</td>
                <td>20-50% <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 50%"></div></div></td>
            </tr>
            <tr>
                <td>Year 10</td>
                <td>Stagnant</td>
                <td>High Variance <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 100%"></div></div></td>
            </tr>
        </tbody>
    </table>
    """,
    stuck_point="The 'On-Site' Carrot.<br><br>Managers dangle the US/Europe visa to keep you cheap. You wait 4 years for a visa that never comes, while your market value rots.",
    verdict="Leave before Year 6. If you stay longer, accept that you are likely a 'Lifer' and make peace with lower growth.",
    seo_desc="The danger of staying in Indian IT service companies (WITCH) for too long. Legacy tech traps and salary stagnation."
)

# 5. Career Switching at 30
create_article(
    cat_name="Career Strategy",
    slug="career-switching-after-30-india",
    title="Career Switching After 30: The Trade-Offs Nobody Posts About",
    persona="30-somethings wanting to jump from Sales/Support to Product/Tech.",
    avoid="Dreamers who think they can switch industries without taking a pay cut.",
    expect="I will do a 6-month bootcamp and land a Senior role in a new field because I have 'transferable skills'.",
    reality="The market doesn't care about your past life.<br><br>If you switch at 30, you are a *Junior* again. You will report to a 24-year-old lead. Your salary might drop by 40%.<br><br>Your 'transferable skills' (communication, maturity) only pay off *after* you prove you can do the hard technical work.",
    salary="""
    <table class="editorial-table">
        <thead>
            <tr>
                <th style="width: 40%">Path</th>
                <th style="width: 60%">Financial Impact</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Stay (Safe)</td>
                <td>
                    Slow growth, high boredom
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 40%; background: #ccc;"></div></div>
                </td>
            </tr>
            <tr>
                <td>Switch (Risky)</td>
                <td>
                    -30% to -50% initial drop
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 20%; background: #d93025;"></div></div>
                </td>
            </tr>
        </tbody>
    </table>
    """,
    stuck_point="Ego Death.<br><br>The hardest part isn't learning Python; it's being the oldest intern in the room and being corrected by someone whose first phone was an iPhone 11.",
    verdict="Do it only if you can survive 2 years of financial and social humility. The upside is huge, but the valley of death is deep.",
    seo_desc="Realities of changing careers after 30 in India. Salary cuts, ego management, and the long road to recovery."
)

# ==========================================
# 2. LEGACY ARTICLES (Phase 6 Content)
# ==========================================

# 6. Junior Data Scientist (Seed 1)
create_article(
    cat_name="Data Science",
    slug="junior-data-scientist-reality-india",
    title="The Reality of 'Junior Data Scientist' Jobs in India",
    persona="New grads expecting to build LLMs on Day 1.",
    avoid="People who think Python notebooks = Production Engineering.",
    expect="I will work on AI models, fine-tune GPT-4, and get paid 18 LPA.",
    reality="90% of Data Science is data cleaning (SQL + Pandas).<br><br>Startups don't need 'Modelers', they need 'Data Engineers' who can move CSVs to a warehouse. You will spend 2 years writing scripts to fix messy Excel sheets.",
    salary="""
    <table class="editorial-table">
        <thead>
            <tr>
                <th style="width: 30%">Role Type</th>
                <th style="width: 30%">Reality (LPA)</th>
                <th style="width: 40%">Work Nature</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Real DS Job</td>
                <td>12.0 - 18.0</td>
                <td>
                    Math/Modeling
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 70%"></div></div>
                </td>
            </tr>
            <tr>
                <td>Analyst (Fake DS)</td>
                <td>4.5 - 7.0</td>
                <td>
                    Excel/Dashboarding
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 30%"></div></div>
                </td>
            </tr>
        </tbody>
    </table>
    """,
    stuck_point="The 'Kaggle' Trap.<br><br>Winning Kaggle competitions means you are good at modeling on clean data. It means nothing for real-world messy pipelines.",
    verdict="Learn SQL and Data Engineering. Pure modeling jobs are only for PhDs or minimal openings.",
    seo_desc="The truth about Data Science jobs for freshers in India. Why most roles are actually Data Analyst positions."
)

# 7. Frontend Developer (Phase 6)
create_article(
    cat_name="Engineering",
    slug="frontend-developer-reality-2025",
    title="The Frontend Developer Reality (2025)",
    persona="Bootcamp graduates and 'React enthusiasts'.",
    avoid="People who think knowing 'useEffect' makes you an engineer.",
    expect="I'll build cool 3D websites, use Next.js 15, and earn 15 LPA comfortably.",
    reality="The market is flooded.<br><br>AI tools (v0, Cursor) are lowering the barrier for UI construction. Companies now expect Full Stack (DB + Backend) or deep performance expertise.<br><br>Just 'centering divs' is no longer a career.",
    salary="""
    <table class="editorial-table">
        <thead>
            <tr>
                <th style="width: 30%">Skill Level</th>
                <th style="width: 30%">Pay (LPA)</th>
                <th style="width: 40%">Employability</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>React Only</td>
                <td>4.0 - 8.0</td>
                <td>
                    Low (Saturated)
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 30%"></div></div>
                </td>
            </tr>
            <tr>
                <td>Full Stack (T3)</td>
                <td>12.0 - 20.0</td>
                <td>
                    High
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 80%"></div></div>
                </td>
            </tr>
        </tbody>
    </table>
    """,
    stuck_point="The 'Tutorial Hell'.<br><br>You can build a Todo app following a video, but you panic when asked to optimize a large DOM tree or handle complex state without guidance.",
    verdict="Only proceed if you can solve business logic, not just UI tickets. Learn the backend.",
    seo_desc="Frontend development in 2025 is crowded. React is not enough. Why Full Stack is the new baseline."
)

# 8. Product Manager (Phase 6)
create_article(
    cat_name="Product Management",
    slug="product-manager-reality-india",
    title="The Product Manager Reality (India)",
    persona="Engineers/MBAs wanting to be 'CEO of the Product'.",
    avoid="People with thin skin or a need to be 'liked' by everyone.",
    expect="I will make strategy, boss people around, and be a visionary Steve Jobs.",
    reality="You are the 'Janitor of Jira'.<br><br>You have all the responsibility but *zero* authority. You spend 6 hours a day on alignment calls, begging engineers to fix bugs.<br><br>Ideas are cheap; execution is the only currency.",
    salary="""
    <table class="editorial-table">
        <thead>
            <tr>
                <th style="width: 30%">Role</th>
                <th style="width: 25%">Exp</th>
                <th style="width: 25%">Pay (LPA)</th>
                <th style="width: 20%">Stress</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>APM</td>
                <td>0-2 Yrs</td>
                <td>
                    12.0 - 18.0
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 40%"></div></div>
                </td>
                <td>High</td>
            </tr>
            <tr>
                <td>PM 2</td>
                <td>3-5 Yrs</td>
                <td>
                    22.0 - 35.0
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 70%"></div></div>
                </td>
                <td>Extreme</td>
            </tr>
        </tbody>
    </table>
    """,
    stuck_point="The 'Feature Factory'.<br><br>You become a ticket-pusher delivering features nobody uses, just to meet a quarterly roadmap deadline.",
    verdict="A high-stress, high-politics role. Not for those seeking 'work-life balance' or artistic freedom.",
    seo_desc="Product Management in India is mostly execution, not strategy. The reality of being a Jira Janitor."
)

# 9. Digital Marketing (Phase 6)
create_article(
    cat_name="Marketing",
    slug="digital-marketing-reality",
    title="The Digital Marketing Reality",
    persona="Creative folks thinking marketing is about 'viral reels'.",
    avoid="People who hate math and spreadsheets.",
    expect="I'll make cool content, work with influencers, and get famous.",
    reality="It's 90% spreadsheet work.<br><br>Real marketing is CAC analysis, ROAS optimization, and SEO technicals. Agency life is a burnout factory (12-hour days) for low pay.",
    salary="""
    <table class="editorial-table">
        <thead>
            <tr>
                <th style="width: 40%">Sector</th>
                <th style="width: 30%">Pay (LPA)</th>
                <th style="width: 30%">Burnout Risk</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Agency</td>
                <td>3.6 - 6.0</td>
                <td>
                    Extreme
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 90%; background: #d93025;"></div></div>
                </td>
            </tr>
            <tr>
                <td>In-House / B2B</td>
                <td>8.0 - 15.0</td>
                <td>
                    Moderate
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 50%"></div></div>
                </td>
            </tr>
        </tbody>
    </table>
    """,
    stuck_point="The 'Agency Trap'.<br><br>You get stuck executing low-level social posts for clients who treat you like a servant. You learn nothing about strategy.",
    verdict="Go In-House or B2B SaaS. Avoid generic social media agencies at all costs.",
    seo_desc="Digital Marketing is data, not art. Why agencies burn you out and where the real money is (B2B)."
)

# 10. UX Design (Phase 6)
create_article(
    cat_name="Design",
    slug="ux-design-reality-india",
    title="The UX Design Reality",
    persona="Switchers from Graphic Design / Architecture.",
    avoid="People who fall in love with their own art.",
    expect="I will do deep user research, empathy mapping, and solve human problems.",
    reality="Most Indian startups just want a 'UI Painter'.<br><br>They want you to copy Airbnb or Cred. Research budgets are non-existent. You will spend your days moving pixels by 2px because the Founder 'doesn't like the vibe'.",
    salary="""
    <table class="editorial-table">
        <thead>
            <tr>
                <th style="width: 40%">Role Focus</th>
                <th style="width: 30%">Demand</th>
                <th style="width: 30%">Pay</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Pure Research</td>
                <td>Very Low</td>
                <td>
                    High (Rare)
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 80%"></div></div>
                </td>
            </tr>
            <tr>
                <td>UI / Visual</td>
                <td>High</td>
                <td>
                    Medium
                    <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 50%"></div></div>
                </td>
            </tr>
        </tbody>
    </table>
    """,
    stuck_point="The 'Dribbble' Portfolio.<br><br>Your portfolio looks pretty but solves no business problem. You can't explain *why* you chose that button color other than 'it looks nice'.",
    verdict="Learn Figma speed and basic frontend. Pure research roles are unicorns.",
    seo_desc="UX Design in India is mostly UI production. The lack of research roles and the demand for visual speed."
)
