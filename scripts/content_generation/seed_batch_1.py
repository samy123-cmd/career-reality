"""
Seed 17 new articles for CareerReality.in
Articles 1-6: MBA, Remote Work, Side Hustles, Equity, Manager vs IC, Layoff Recovery
"""
import os
import django
import datetime
from django.utils import timezone

import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Author, Category, Article

# Get authors
author1 = Author.objects.get(id=1)  # P. Mishra
author2 = Author.objects.get(id=2)  # Shiv Mishra

def create_article(author, cat_name, slug, title, persona, avoid, expect, reality, salary, stuck_point, verdict, seo_desc):
    category, _ = Category.objects.get_or_create(
        name=cat_name, 
        defaults={"slug": cat_name.lower().replace(" ", "-"), "order": 1}
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
            "stuck_point": stuck_point,
            "verdict": verdict,
            "meta_title": title[:60],
            "meta_description": seo_desc[:160],
            "published_at": timezone.now(),
            "last_reality_check": datetime.date.today(),
        }
    )
    status = "Created" if created else "Updated"
    print(f"{status}: {title}")

# ============================================================
# ARTICLE 1: The MBA Reality
# ============================================================
create_article(
    author=author1,
    cat_name="Education",
    slug="mba-reality-india-worth-it-2026",
    title="The MBA Reality in India: Is It Still Worth the ₹25 Lakh Bet?",
    persona="Working professionals considering an MBA to accelerate their career or pivot industries.",
    avoid="""
<p>If you believe an MBA from any institute will guarantee a high-paying job, this article will disappoint you.</p>
<p>If you're running away from a bad job rather than running toward a clear goal, an MBA won't save you.</p>
""",
    expect="""
<p>The MBA promise is seductive and specific:</p>
<ul>
<li>Take 2 years off. Pay ₹20-30 lakhs.</li>
<li>Exit with a ₹25-40 LPA job in consulting, product management, or investment banking.</li>
<li>Build a "network for life" that opens doors forever.</li>
<li>The degree pays for itself within 3 years.</li>
</ul>
<p>Campus placements show impressive salary figures. Alumni share success stories. The ROI calculation looks simple.</p>
""",
    reality="""
<p>The MBA market in India is brutally bifurcated.</p>

<p><strong>Tier 1 (IIM A/B/C, ISB, XLRI):</strong> The promise mostly holds. Median packages of ₹25-35 LPA are real. Consulting and banking recruiters show up. The network has value.</p>

<p><strong>Tier 2-3 (Everyone else):</strong> The median placement drops to ₹12-18 LPA. Many graduates take jobs they could have gotten without the MBA. The "consulting" placements are often glorified sales roles at small firms.</p>

<p>The gap between Tier 1 and Tier 2 is wider than ever. Companies that pay premium salaries recruit almost exclusively from the top 10 schools. They use the MBA as a filter, not a qualification.</p>

<p>For career switchers, the math is worse. A 30-year-old with 7 years of experience pays the same fee but competes with 23-year-olds who are cheaper and more moldable. The "experience premium" rarely materializes in starting salaries.</p>

<p>The network value is also overstated. Most meaningful business relationships come from working together, not sharing a hostel. The alumni network helps with referrals, but so does LinkedIn.</p>
""",
    salary="""
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 30%">MBA Tier</th>
            <th style="width: 25%">Investment (₹)</th>
            <th style="width: 25%">Median CTC (LPA)</th>
            <th style="width: 20%">Break-even</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>IIM A/B/C</strong></td>
            <td>₹25-30 Lakh</td>
            <td>₹30-40 LPA</td>
            <td>2-3 Years</td>
        </tr>
        <tr>
            <td><strong>Tier 1 (ISB, XLRI, IIM-LCK)</strong></td>
            <td>₹20-28 Lakh</td>
            <td>₹22-30 LPA</td>
            <td>3-4 Years</td>
        </tr>
        <tr>
            <td><strong>Tier 2 (New IIMs, MDI)</strong></td>
            <td>₹15-22 Lakh</td>
            <td>₹14-20 LPA</td>
            <td>4-6 Years</td>
        </tr>
        <tr>
            <td><strong>Tier 3 (Private/State)</strong></td>
            <td>₹8-15 Lakh</td>
            <td>₹8-14 LPA</td>
            <td>5-8+ Years</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*Break-even includes opportunity cost of 2 years' lost salary.</p>
""",
    stuck_point="""
<p><strong>The "Any MBA is Good" Delusion.</strong></p>

<p>Many professionals convince themselves that "any" MBA will open doors because they've seen it work for others. What they don't see is the survivorship bias—the successful MBA graduates are visible precisely because they succeeded.</p>

<p>The harder truth: If you can't get into a top 20 school, the MBA is likely a consumption expense disguised as an investment. You're paying for an experience, not an asset.</p>

<p>The most dangerous trap is the career-switcher who joins a Tier 2 program expecting to pivot from sales to product management. They often exit with more debt and the same job options.</p>
""",
    verdict="""
<p>The MBA is binary: worth it at the top, questionable everywhere else.</p>

<p>Before you apply, calculate the <strong>true opportunity cost</strong>: 2 years of salary (₹15-30 lakh) + fees (₹15-30 lakh) + living expenses (₹5-10 lakh) = ₹35-70 lakh total bet.</p>

<p>If you can get into a top 15 program with a clear career goal, the bet often pays off. If you're looking at anything below that tier, you should have a very specific reason—and "I need to take a break" isn't one.</p>

<p>The MBA is not a reset button. It's a multiplier. It multiplies what you already have—or exposes what you don't.</p>
""",
    seo_desc="Is an MBA worth it in India in 2026? Real ROI analysis across IIMs, ISB, and Tier 2-3 schools. Salary data, break-even timelines, and the hard truth."
)

# ============================================================
# ARTICLE 2: Remote Work Salary Trap
# ============================================================
create_article(
    author=author2,
    cat_name="Money Reality",
    slug="remote-work-salary-trap-india",
    title="The Remote Work Salary Trap: When Geographic Arbitrage Cuts Both Ways",
    persona="Indian professionals working for US/European companies remotely, or considering remote roles.",
    avoid="""
<p>If you believe remote work for a US company means US-level wealth in India forever, you haven't seen the 2023-2025 correction yet.</p>
<p>If you're celebrating your "dollar salary" without calculating the volatility, read on.</p>
""",
    expect="""
<p>The promise of remote work for foreign companies seemed like a cheat code:</p>
<ul>
<li>Earn $80-150K while living in India.</li>
<li>Save 70%+ of your income due to low cost of living.</li>
<li>Build wealth faster than any local job could offer.</li>
<li>Retire early with a portfolio built on geographic arbitrage.</li>
</ul>
<p>For a few golden years (2020-2022), this was reality for a select few. The math was undeniable.</p>
""",
    reality="""
<p>The correction came quietly, then all at once.</p>

<p><strong>The Layoff Wave (2023-2025):</strong> Remote Indian workers were often the first to go in layoffs. "Cost optimization" meant replacing $100K remote Indians with $60K remote Indians in other countries, or eliminating the role entirely.</p>

<p><strong>The Salary Compression:</strong> Companies realized they were overpaying for Indian talent relative to local alternatives. New remote offers now come at 50-70% of what they were in 2021. The arbitrage window is closing.</p>

<p><strong>The Isolation Tax:</strong> Remote workers miss the visibility that builds careers. Promotions go to people who are physically present. Your amazing output is invisible compared to the person who eats lunch with the VP.</p>

<p><strong>The Tax Complexity:</strong> Many remote workers discover (too late) that their tax situation is a nightmare. Double taxation treaties are complex. Some have faced unexpected tax bills that wiped out years of savings.</p>

<p>The dream of permanent geographic arbitrage is fading. Companies are getting smarter about paying "local market rates" regardless of where you sit.</p>
""",
    salary="""
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 35%">Remote Role</th>
            <th style="width: 25%">2021 Pay (USD)</th>
            <th style="width: 25%">2025 Pay (USD)</th>
            <th style="width: 15%">Change</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Senior Engineer</strong></td>
            <td>$100-150K</td>
            <td>$60-100K</td>
            <td style="color: #d93025;">-35%</td>
        </tr>
        <tr>
            <td><strong>Staff/Principal</strong></td>
            <td>$150-220K</td>
            <td>$100-160K</td>
            <td style="color: #d93025;">-30%</td>
        </tr>
        <tr>
            <td><strong>Product Manager</strong></td>
            <td>$90-140K</td>
            <td>$55-90K</td>
            <td style="color: #d93025;">-40%</td>
        </tr>
        <tr>
            <td><strong>Designers</strong></td>
            <td>$70-120K</td>
            <td>$45-80K</td>
            <td style="color: #d93025;">-35%</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*Salary ranges for Indian remote workers. Excludes FAANG outliers.</p>
""",
    stuck_point="""
<p><strong>The "I'm Special" Fallacy.</strong></p>

<p>High performers on remote salary often believe they'll be the exception in the next layoff wave. They won't. Remote workers are, by definition, more replaceable because the company already proved it doesn't need you in an office.</p>

<p>The second trap is lifestyle inflation. Earning ₹80L+ per year, you buy the apartment, the car, and the lifestyle—then get laid off with ₹2L/month in EMIs and a job market that now pays half what you made.</p>

<p>Many are stuck in a high-expense lifestyle with skills that are now overpriced for the domestic market and underpriced for the shrinking international one.</p>
""",
    verdict="""
<p>Remote work for foreign companies can still be lucrative, but the golden era is over. The sustainable arbitrage is now 30-40%, not 200%.</p>

<p>If you're in a remote role today, the smart play is:</p>
<ul>
<li><strong>Save aggressively</strong> while the arbitrage lasts. Assume it ends in 2 years.</li>
<li><strong>Build local options</strong>. Keep interviewing for Indian roles to maintain negotiation power.</li>
<li><strong>Stay visible</strong>. Over-communicate. Travel to HQ when possible. Fight the invisibility tax.</li>
</ul>

<p>The remote salary trap is real: it's easy to build a lifestyle on income that can disappear with one Slack message.</p>
""",
    seo_desc="The reality of remote work salaries for Indian tech workers in 2025. Salary compression, layoff risks, and why geographic arbitrage is fading."
)

# ============================================================
# ARTICLE 3: Side Hustle Reality
# ============================================================
create_article(
    author=author1,
    cat_name="Money Reality",
    slug="side-hustle-myth-india-reality",
    title="Why Side Hustles Don't Scale for Most People",
    persona="Full-time employees trying to build income streams through content, courses, freelancing, or small businesses.",
    avoid="""
<p>If you believe passive income is real and easy, this article will frustrate you.</p>
<p>If you think you'll build a YouTube channel "on the side" while working 50-hour weeks, keep reading.</p>
""",
    expect="""
<p>The side hustle narrative is everywhere:</p>
<ul>
<li>"I make ₹2 Lakhs/month from my side hustle while working full-time."</li>
<li>"Multiple income streams are the key to financial freedom."</li>
<li>"Start a YouTube channel/newsletter/course and watch passive income roll in."</li>
<li>"Your 9-5 is just funding your real dream."</li>
</ul>
<p>The influencers make it look easy. A few hours on weekends. Compound growth. Eventually, quit your job.</p>
""",
    reality="""
<p>Most side hustles fail for a simple reason: <strong>time is finite and energy is even more limited.</strong></p>

<p><strong>The Attention Split:</strong> A demanding full-time job (50+ hours including commute and mental overhead) leaves you with ~15-20 hours of genuine productive time per week for everything else—family, health, hobbies, and your "side hustle." In practice, most people can sustain 5-10 hours/week on a side project before burnout.</p>

<p><strong>The Survivorship Bias:</strong> For every person earning ₹2L/month from their side hustle, there are 500 who made ₹2,000 total before giving up. The successful ones are visible. The failures are silent.</p>

<p><strong>The Time Horizon Problem:</strong> Most side hustles take 2-4 years of consistent effort before they generate meaningful income. Most people quit at 6 months when they've made ₹10K total and spent ₹50K on courses about side hustles.</p>

<p><strong>The "Passive" Lie:</strong> Truly passive income requires massive upfront investment (capital or time). A YouTube channel with ₹50K/month ad revenue requires posting 3x/week for 3+ years. A course that sells while you sleep took 500+ hours to create and market.</p>

<p>The math rarely works if you're not willing to sacrifice either your job performance, your health, or your relationships for 3-5 years.</p>
""",
    salary="""
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 30%">Side Hustle</th>
            <th style="width: 25%">Time to ₹50K/mo</th>
            <th style="width: 25%">Success Rate</th>
            <th style="width: 20%">Sustainability</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>YouTube/Content</strong></td>
            <td>2-4 Years</td>
            <td>~2-5%</td>
            <td>Medium</td>
        </tr>
        <tr>
            <td><strong>Freelancing</strong></td>
            <td>6-18 Months</td>
            <td>~15-20%</td>
            <td>High (Active)</td>
        </tr>
        <tr>
            <td><strong>Online Courses</strong></td>
            <td>1-3 Years</td>
            <td>~5-10%</td>
            <td>Medium</td>
        </tr>
        <tr>
            <td><strong>E-commerce/Dropship</strong></td>
            <td>6-24 Months</td>
            <td>~5-8%</td>
            <td>Low</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*Success rate = % who reach ₹50K/month within 3 years of starting.</p>
""",
    stuck_point="""
<p><strong>The "Opportunity Cost" Blindness.</strong></p>

<p>Many side hustlers don't calculate what they're trading. If you earn ₹30L/year at your job, and your side hustle makes ₹3L/year while costing you a promotion worth ₹5L/year, you've lost money.</p>

<p>The hidden cost is often career stagnation. The person who's "phoning it in" at work because they're exhausted from their side hustle gets passed over for growth opportunities. Their main income suffers while their side income stays marginal.</p>

<p>The trap is the sunk cost: "I've already invested 2 years, I can't quit now." But you can. And often you should.</p>
""",
    verdict="""
<p>Side hustles can work, but they're not for everyone and they're not "passive."</p>

<p>They work best when:</p>
<ul>
<li>You have 15+ hours/week of genuine surplus energy</li>
<li>Your main job is low-stress and doesn't require after-hours attention</li>
<li>You're building something that compounds (audience, software) not trading time for money</li>
<li>You can sustain 3+ years without meaningful returns</li>
</ul>

<p>For most people, the better play is: <strong>get promoted at your main job</strong>. A ₹5L raise achieved by focusing fully on your career often beats a ₹3L/year side hustle that's costing you that raise.</p>

<p>The math only changes when your side hustle reaches escape velocity—usually 50-70% of your salary. Until then, it's often a distraction dressed up as ambition.</p>
""",
    seo_desc="Why most side hustles fail and the hidden costs of splitting your attention. Real success rates, time horizons, and when to quit."
)

print("\n✅ First batch (3 articles) created successfully!")
