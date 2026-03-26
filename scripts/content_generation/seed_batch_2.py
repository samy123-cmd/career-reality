"""
Seed batch 2: Articles 4-6
Equity Trap, Manager vs IC, Layoff Recovery
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

author1 = Author.objects.get(id=1)
author2 = Author.objects.get(id=2)

def create_article(author, cat_name, slug, title, persona, avoid, expect, reality, salary, stuck_point, verdict, seo_desc):
    category, _ = Category.objects.get_or_create(
        name=cat_name, 
        defaults={"slug": cat_name.lower().replace(" ", "-"), "order": 1}
    )
    article, created = Article.objects.update_or_create(
        slug=slug,
        defaults={
            "title": title, "author": author, "category": category,
            "status": "published", "target_persona": persona,
            "who_should_avoid": avoid, "common_expectation": expect,
            "actual_reality": reality, "salary_reality": salary,
            "stuck_point": stuck_point, "verdict": verdict,
            "meta_title": title[:60], "meta_description": seo_desc[:160],
            "published_at": timezone.now(), "last_reality_check": datetime.date.today(),
        }
    )
    print(f"{'Created' if created else 'Updated'}: {title}")

# ARTICLE 4: The Equity Trap
create_article(
    author=author1,
    cat_name="Money Reality",
    slug="startup-equity-esop-reality-india",
    title="The Equity Trap: When Your Stock Options Are Worthless Paper",
    persona="Startup employees holding ESOPs expecting a windfall when the company IPOs or gets acquired.",
    avoid="""
<p>If you joined a startup specifically for the equity and accepted a salary cut for it, this will sting.</p>
<p>If you think your ESOP grant letter is a promise of wealth, you haven't read the fine print.</p>
""",
    expect="""
<p>The startup equity dream goes like this:</p>
<ul>
<li>"Take a 30% salary cut now, but your equity will be worth ₹2-3 Crore at exit."</li>
<li>"Join early, own 0.1% of a future unicorn."</li>
<li>"We had an employee who retired at 35 after our Series D."</li>
<li>"Equity aligns your incentives with the company's success."</li>
</ul>
<p>Founders share stories of early employees who became millionaires. The math looks compelling.</p>
""",
    reality="""
<p>Indian startup equity is, statistically, worthless for most employees.</p>

<p><strong>The Dilution Reality:</strong> Your 0.1% stake gets diluted with every funding round. By the time there's an exit, you might own 0.02%. That ₹2 Crore dream is now ₹40 lakhs—before taxes and preference stacks.</p>

<p><strong>The Vesting Cliff:</strong> Most ESOPs vest over 4 years with a 1-year cliff. If you leave (or are laid off) before the cliff, you get nothing. After the cliff, you get 25%. Most people don't stay 4 years.</p>

<p><strong>The Liquidity Problem:</strong> Even if your equity has "value," you can't sell it. There's no secondary market. You're holding paper until an IPO or acquisition—which may never come, or may come at a valuation where your shares are worthless due to liquidation preferences.</p>

<p><strong>The Preference Stack:</strong> Investors get paid first. If the company raised ₹500 Cr and exits at ₹600 Cr, the investors take their ₹500 Cr (often with a premium). Employees split what's left—which is often nothing after legal fees.</p>

<p><strong>The Tax Nightmare:</strong> In India, you pay tax when you exercise options (on the FMV minus strike price) even if you can't sell the shares. People have faced tax bills they couldn't pay on paper gains that never materialized.</p>
""",
    salary="""
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 30%">Stage When Joined</th>
            <th style="width: 25%">Typical Grant</th>
            <th style="width: 25%">Exit Reality</th>
            <th style="width: 20%">Outcome</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Seed/Early</strong></td>
            <td>0.05-0.25%</td>
            <td>Heavy dilution, high risk</td>
            <td>Usually ₹0</td>
        </tr>
        <tr>
            <td><strong>Series A/B</strong></td>
            <td>0.01-0.05%</td>
            <td>Moderate dilution</td>
            <td>₹5-30L (if lucky)</td>
        </tr>
        <tr>
            <td><strong>Series C+</strong></td>
            <td>0.005-0.02%</td>
            <td>Small upside, lower risk</td>
            <td>₹10-50L (if IPO)</td>
        </tr>
        <tr>
            <td><strong>Pre-IPO</strong></td>
            <td>0.001-0.01%</td>
            <td>Limited upside</td>
            <td>₹5-25L</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*90%+ of startup employees receive ₹0 from equity. These figures assume a successful exit.</p>
""",
    stuck_point="""
<p><strong>The Sunk Cost Identity.</strong></p>

<p>After accepting lower salary for 2-3 years for "equity," people become emotionally invested in the narrative. They can't admit the equity might be worthless because it would mean they were underpaid for years.</p>

<p>They stay longer, hoping for an exit that justifies the sacrifice. Each year, the market salary gap widens while their equity value remains theoretical.</p>

<p>The psychological trap is treating unvested equity as "lost money" if you leave, when in reality it was never money at all.</p>
""",
    verdict="""
<p>Startup equity can be valuable, but only under very specific conditions:</p>
<ul>
<li>You joined pre-Series A at a company that actually exits successfully (1-2% of startups)</li>
<li>You stayed 4+ years and fully vested</li>
<li>The exit valuation cleared the preference stack</li>
<li>You could afford the tax bill on exercise</li>
</ul>

<p>For everyone else: <strong>optimize for cash.</strong> Take the higher salary. If equity is offered, treat it as a lottery ticket with a 95% chance of paying zero.</p>

<p>Never take a salary cut for equity unless you can genuinely afford to lose that money forever. Because statistically, you will.</p>
""",
    seo_desc="The truth about startup ESOPs in India. Why most employee stock options are worthless, dilution math, and the liquidation preference trap."
)

# ARTICLE 5: Manager vs IC
create_article(
    author=author2,
    cat_name="Career Strategy",
    slug="manager-vs-ic-career-path-india",
    title="The Manager vs IC Reality: Which Path Actually Pays in India?",
    persona="Senior engineers (5-8 years) deciding between management track and individual contributor (IC/Staff) track.",
    avoid="""
<p>If you think "I'll just become a manager because I'm tired of coding," you're entering management for the wrong reason.</p>
<p>If you believe the IC path is simpler because you avoid "politics," you haven't seen Staff-level dynamics.</p>
""",
    expect="""
<p>The career advice usually frames it as a simple choice:</p>
<ul>
<li><strong>Manager Track:</strong> Lead people, get promoted to Director, VP, eventually CTO. Earn more money at scale.</li>
<li><strong>IC Track:</strong> Become a technical expert, reach Staff/Principal, avoid management headaches. Similar pay, more autonomy.</li>
</ul>
<p>LinkedIn makes it sound like both paths are equally viable and well-compensated at senior levels.</p>
""",
    reality="""
<p>In India, the IC track is structurally disadvantaged in most companies.</p>

<p><strong>The Ceiling Problem:</strong> Most Indian companies don't have real IC tracks beyond Senior/Lead Engineer. "Staff Engineer" and "Principal Engineer" roles exist at a handful of product companies (Google, Microsoft, Flipkart). At 90% of companies, senior ICs hit a ceiling at ₹40-50 LPA while managers continue climbing.</p>

<p><strong>The Compensation Gap:</strong> At the ₹80 LPA+ level, the population is 80% managers and 20% ICs. The path to high compensation in India runs through management for simple reasons: managers control budgets, ICs don't.</p>

<p><strong>The Manager Survival Rate:</strong> But management is brutal. The failure rate is high. Many engineers become managers, fail at people management, and exit to a different company as an IC—having lost years of technical depth.</p>

<p><strong>The IC Invisibility:</strong> ICs who don't actively self-promote become invisible to leadership. Their work gets attributed to managers. Staying IC requires constant visibility management—something most technical people despise.</p>

<p>Neither path is easy. The question is which type of difficulty matches your personality.</p>
""",
    salary="""
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 25%">Level</th>
            <th style="width: 25%">Manager Track</th>
            <th style="width: 25%">IC Track</th>
            <th style="width: 25%">Availability</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Mid (5-7y)</strong></td>
            <td>Eng Manager: 30-50L</td>
            <td>Senior Eng: 25-45L</td>
            <td>Both common</td>
        </tr>
        <tr>
            <td><strong>Senior (8-12y)</strong></td>
            <td>Sr Manager: 45-75L</td>
            <td>Staff Eng: 40-70L</td>
            <td>IC rare outside Big Tech</td>
        </tr>
        <tr>
            <td><strong>Leadership (12+y)</strong></td>
            <td>Director: 70-120L</td>
            <td>Principal: 60-100L</td>
            <td>IC very rare</td>
        </tr>
        <tr>
            <td><strong>Executive</strong></td>
            <td>VP/CTO: 1-3 Cr</td>
            <td>Distinguished: 1-1.5 Cr</td>
            <td>IC unicorn territory</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*Indian market. MNC product companies in Bangalore/Hyderabad.</p>
""",
    stuck_point="""
<p><strong>The "I Hate Both" Trap.</strong></p>

<p>Many people reach 7-8 years of experience and realize they don't want to manage people AND they're not passionate enough about technology to become a world-class IC.</p>

<p>They're stuck in the middle: not technical enough for Staff roles, not interested enough for management roles. This is where careers stagnate.</p>

<p>The uncomfortable truth is that at senior levels, both paths require genuine passion for their respective crafts. You can't phone in either one.</p>
""",
    verdict="""
<p>Choose management if:</p>
<ul>
<li>You get energy from unblocking people, not from solving technical puzzles</li>
<li>You can tolerate ambiguity, politics, and taking blame for others' failures</li>
<li>You want the higher ceiling and are willing to fight for it</li>
</ul>

<p>Choose IC if:</p>
<ul>
<li>You still get excited about architecture and code after 7 years</li>
<li>You're at (or can get to) a company with a real IC ladder</li>
<li>You're willing to actively manage your visibility and influence</li>
</ul>

<p>The worst choice is becoming a manager because you think it's expected or because you're bored. Failed managers rarely recover their previous trajectory.</p>
""",
    seo_desc="Manager vs IC career paths in Indian tech. Salary comparison, ceiling realities, and how to choose the path that fits your personality."
)

# ARTICLE 6: Layoff Recovery
create_article(
    author=author1,
    cat_name="Career Strategy",
    slug="layoff-recovery-timeline-india",
    title="The Layoff Recovery Timeline Nobody Talks About",
    persona="Tech professionals who have been laid off or fear layoffs, trying to understand the realistic recovery path.",
    avoid="""
<p>If you think you'll find a better job within 2 weeks after a layoff, this article will calibrate your expectations.</p>
<p>If you believe "I'll use this time to build my startup," please read the section on sunk cost delusion.</p>
""",
    expect="""
<p>When layoffs happen, the common advice is optimistic:</p>
<ul>
<li>"One door closes, another opens."</li>
<li>"You're talented—you'll land on your feet quickly."</li>
<li>"The market is hot for good engineers."</li>
<li>"This is a blessing in disguise—time to find something better."</li>
</ul>
<p>For some, this is true. For most, recovery is longer and harder than expected.</p>
""",
    reality="""
<p>The layoff recovery timeline in 2024-2026 India looks nothing like 2021.</p>

<p><strong>The Application Numbers:</strong> Where 10 applications once yielded 3 interviews, people now report 100+ applications for 5-10 interviews. The volume of candidates has exploded while positions have contracted.</p>

<p><strong>The Timeline:</strong> Average recovery time has stretched from 2-3 months (2021) to 4-8 months (2024-2026) for mid-senior roles. For Director+ roles, 9-12 months is common.</p>

<p><strong>The Salary Reset:</strong> Most people who are laid off take a 10-20% salary cut in their next role. The leverage has shifted to employers. "I need a job" is a weak negotiating position.</p>

<p><strong>The Psychological Toll:</strong> The first month feels like a vacation. The second month, anxiety sets in. By month four, depression is common. The job search becomes a full-time job that pays rejection.</p>

<p><strong>The Network Advantage:</strong> People with strong networks recover 2-3x faster. Referrals convert at 10x the rate of cold applications. If you didn't build relationships before the layoff, the recovery is much harder.</p>
""",
    salary="""
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 25%">Experience</th>
            <th style="width: 25%">Avg Recovery Time</th>
            <th style="width: 25%">Salary Impact</th>
            <th style="width: 25%">Applications Needed</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>0-3 years</strong></td>
            <td>2-4 months</td>
            <td>-5% to +10%</td>
            <td>50-150</td>
        </tr>
        <tr>
            <td><strong>4-7 years</strong></td>
            <td>3-6 months</td>
            <td>-10% to +5%</td>
            <td>100-250</td>
        </tr>
        <tr>
            <td><strong>8-12 years</strong></td>
            <td>4-8 months</td>
            <td>-15% to -5%</td>
            <td>150-300</td>
        </tr>
        <tr>
            <td><strong>13+ years</strong></td>
            <td>6-12 months</td>
            <td>-20% to -10%</td>
            <td>200-400</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*2024-2026 Indian tech market. Excludes FAANG/top-tier company pedigree.</p>
""",
    stuck_point="""
<p><strong>The "Startup/Break" Delusion.</strong></p>

<p>Many laid-off professionals decide to "take some time off" or "finally build that startup." While rest is valid, extended breaks become resume gaps that concern employers.</p>

<p>The "startup" built during unemployment is often a coping mechanism masquerading as productivity. It rarely produces revenue and often delays the job search by months.</p>

<p>The trap is using the break as an escape from the painful reality of job searching. Rejection is hard. Building something feels productive. But at month six, you have neither a job nor a real business.</p>
""",
    verdict="""
<p>If you're laid off or expect to be:</p>

<ul>
<li><strong>File for unemployment immediately</strong> (if applicable). Many people don't know they're eligible.</li>
<li><strong>Start applying within 1 week.</strong> The "take a break first" advice is luxury advice for people with 12+ months of savings.</li>
<li><strong>Activate your network on day one.</strong> Message 20 people per day with specific asks, not vague "let me know if you hear of anything."</li>
<li><strong>Expect 4-6 months.</strong> Budget accordingly. If you land earlier, celebrate. If not, you're prepared.</li>
<li><strong>Take a slight salary cut if needed</strong> after month 3. The gap on your resume costs more than 10%.</li>
</ul>

<p>The layoff is not a reflection of your worth. But the recovery is a test of your preparation and network. Both can be built, even post-layoff—just more slowly.</p>
""",
    seo_desc="Real layoff recovery timelines in Indian tech 2024-2026. How long job searches actually take, salary impacts, and common traps to avoid."
)

print("\n✅ Batch 2 (3 articles) created successfully!")
