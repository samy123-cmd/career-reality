"""
Seed batch 3: Articles 7-9
Networking, Freelancing, Senior Developer Ceiling
"""
import os
import django
import datetime
from django.utils import timezone

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

# ARTICLE 7: Networking Reality
create_article(
    author=author2,
    cat_name="Career Strategy",
    slug="networking-reality-india-introverts",
    title="Why 'Networking' Doesn't Work the Way You're Told",
    persona="Professionals who hate networking events but know they 'should' network more.",
    avoid="""
<p>If you enjoy collecting LinkedIn connections and calling it networking, this isn't for you.</p>
<p>If you believe showing up to events and exchanging cards creates relationships, keep reading.</p>
""",
    expect="""
<p>The networking advice is constant:</p>
<ul>
<li>"Your network is your net worth."</li>
<li>"Attend industry events—you never know who you'll meet."</li>
<li>"Connect with 10 people every week on LinkedIn."</li>
<li>"Coffee chats are career accelerators."</li>
</ul>
<p>Introverts force themselves to events. Extroverts collect contacts. Everyone believes they're "building their network."</p>
""",
    reality="""
<p>Most networking is performative activity that produces nothing.</p>

<p><strong>The Event Illusion:</strong> Conference networking is the least effective form. You meet 20 people, exchange pleasantries, collect cards—and a week later, neither party remembers the other. These are contacts, not connections.</p>

<p><strong>The LinkedIn Fallacy:</strong> Having 5,000 LinkedIn connections means nothing if you can't ask 5 of them for a meaningful favor. Connection count is a vanity metric that doesn't convert to career capital.</p>

<p><strong>What Actually Works:</strong> Real professional relationships form through shared work, not shared drinks. The strongest connections come from:</p>
<ul>
<li>Working on projects together (even side projects)</li>
<li>Helping someone when you don't need anything back</li>
<li>Being genuinely useful to someone's problems</li>
<li>Consistent, low-pressure contact over years (not quarterly "catching up")</li>
</ul>

<p><strong>The Asymmetry:</strong> Networking works best for people who least need it—those already successful enough to offer value. Junior people "networking" with senior people are usually extracting, not exchanging. The senior person knows this.</p>
""",
    salary="""
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 35%">Networking Method</th>
            <th style="width: 25%">Time Investment</th>
            <th style="width: 20%">Conversion Rate</th>
            <th style="width: 20%">Quality</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Conferences/Events</strong></td>
            <td>High (4-8 hrs)</td>
            <td>~2%</td>
            <td>Low</td>
        </tr>
        <tr>
            <td><strong>Cold LinkedIn Outreach</strong></td>
            <td>Medium (1-2 hrs/wk)</td>
            <td>~5%</td>
            <td>Low-Medium</td>
        </tr>
        <tr>
            <td><strong>Warm Introductions</strong></td>
            <td>Low (as needed)</td>
            <td>~40%</td>
            <td>High</td>
        </tr>
        <tr>
            <td><strong>Shared Projects/Work</strong></td>
            <td>High (ongoing)</td>
            <td>~60%</td>
            <td>Highest</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*Conversion = relationship that produces career value within 2 years.</p>
""",
    stuck_point="""
<p><strong>The Activity Trap.</strong></p>

<p>Many people "network" constantly but never convert activity into relationships. They attend every event, message every speaker, and feel productive—but when they need help, they have no one to call.</p>

<p>The mistake is optimizing for volume over depth. 10 genuine relationships beat 1,000 LinkedIn connections. But building 10 genuine relationships takes years, not events.</p>

<p>The trap is believing that networking is a task to complete rather than relationships to maintain over decades.</p>
""",
    verdict="""
<p>Stop networking like you're supposed to. Start building relationships like a human.</p>

<ul>
<li><strong>Depth over breadth:</strong> Invest heavily in 20-30 relationships rather than maintaining 500 shallow ones.</li>
<li><strong>Give before you take:</strong> Help three people before asking one for help. The ratio matters.</li>
<li><strong>Skip the events:</strong> Unless you genuinely enjoy them, your time is better spent doing excellent work that people notice.</li>
<li><strong>Play the long game:</strong> The best professional relationships are 5-10 years in the making.</li>
</ul>

<p>The people who get the most from their "network" rarely call it networking. They call it friendship, mentorship, and professional respect—earned over years, not collected at events.</p>
""",
    seo_desc="Why traditional networking advice fails and what actually builds career-changing relationships. Reality check for introverts and event-avoiders."
)

# ARTICLE 8: Freelancing Reality
create_article(
    author=author1,
    cat_name="Money Reality",
    slug="freelancing-reality-india-freedom-myth",
    title="The Freelancing Reality: Freedom vs Financial Instability",
    persona="Employed professionals dreaming of quitting to freelance for 'freedom' and 'better hourly rates.'",
    avoid="""
<p>If you think freelancing is a pay raise with extra vacation, this will disillusion you.</p>
<p>If you believe your employer's hourly bill rate is what you'll earn freelancing, do the math below.</p>
""",
    expect="""
<p>The freelancing fantasy:</p>
<ul>
<li>"My company bills me at $100/hr but pays me $30/hr. I'll keep the difference!"</li>
<li>"I'll work 4 days a week and earn the same money."</li>
<li>"No more office politics—just me and my craft."</li>
<li>"I'll travel and work from anywhere."</li>
</ul>
<p>The Instagram freelancers make it look effortless. Laptop on a beach. "Client work done, hiking now."</p>
""",
    reality="""
<p>Freelancing is running a business while doing the work of an employee. Most people underestimate the overhead.</p>

<p><strong>The Billable Hours Reality:</strong> A full-time employee works ~2,000 hours/year and gets paid for all of them. A freelancer might bill 1,000-1,400 hours if they're lucky. The rest is spent on:</p>
<ul>
<li>Finding clients (sales, outreach, proposals)</li>
<li>Admin (invoicing, taxes, contracts)</li>
<li>Unbillable gaps between projects</li>
<li>Client management and communication</li>
</ul>

<p><strong>The Rate Math:</strong> If you need ₹20 LPA equivalent, you need to bill ₹2,400/hr (not ₹1,000/hr) because you'll only bill 40-50% of your time. Most freelancers undercharge and overwork.</p>

<p><strong>The Stability Fallacy:</strong> One client is not freelancing—it's contracting. True freelancing means multiple clients. But multiple clients mean multiple bosses, multiple fires, and constant context switching.</p>

<p><strong>The Loneliness Tax:</strong> No team, no water cooler, no shared wins. Depression and burnout rates for freelancers are significantly higher than employees. The "freedom" often feels like isolation.</p>

<p><strong>The Benefits Gap:</strong> No health insurance, no PF, no paid leave, no learning budget. These cost 20-30% of a salary package that freelancers must self-fund.</p>
""",
    salary="""
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 30%">Comparison</th>
            <th style="width: 35%">Employee (20 LPA)</th>
            <th style="width: 35%">Freelancer (Equivalent)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Hours Paid</strong></td>
            <td>2,000 hrs/year</td>
            <td>1,200 hrs billed</td>
        </tr>
        <tr>
            <td><strong>Rate Needed</strong></td>
            <td>~₹1,000/hr (implicit)</td>
            <td>₹2,200-2,800/hr</td>
        </tr>
        <tr>
            <td><strong>Benefits</strong></td>
            <td>20-30% extra value</td>
            <td>Self-funded</td>
        </tr>
        <tr>
            <td><strong>Income Stability</strong></td>
            <td>Monthly paycheck</td>
            <td>Variable, delayed</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*To match ₹20 LPA, a freelancer needs ₹30-35 LPA in billings to cover gaps, taxes, and self-funded benefits.</p>
""",
    stuck_point="""
<p><strong>The Feast-or-Famine Cycle.</strong></p>

<p>Freelancers often alternate between overwhelming work and terrifying silence. When busy, there's no time to find new clients. When slow, desperation leads to underpricing.</p>

<p>The trap is accepting any work during famine phases, which leads to burnout during feast—and no time to build a sustainable pipeline. Many freelancers are perpetually 2-3 months from crisis.</p>

<p>Breaking the cycle requires saying no to work during busy periods (to protect time for sales) and charging enough during work to survive the gaps. Most don't.</p>
""",
    verdict="""
<p>Freelancing can work, but it's a different job than employment—not an upgrade to it.</p>

<p>It works best when:</p>
<ul>
<li>You have 6-12 months of savings before starting</li>
<li>You enjoy sales and client management (not just the craft)</li>
<li>You can charge 2-3x your implicit employee hourly rate</li>
<li>You have a network that can generate referrals</li>
</ul>

<p>For most, the better path is: negotiate remote work at your employer, build leverage through skills, and use employment stability to fund your life. Freelancing looks like freedom until it feels like precarity.</p>
""",
    seo_desc="The hidden costs of freelancing in India. Why your hourly rate is wrong, the billable hours trap, and when freelancing is a downgrade."
)

# ARTICLE 9: Senior Developer Ceiling
create_article(
    author=author2,
    cat_name="Software Engineering",
    slug="senior-developer-salary-ceiling-india",
    title="The Senior Developer Ceiling: Why Salaries Plateau at ₹40 LPA",
    persona="Senior engineers (6-10 years) wondering why their salary growth has slowed dramatically.",
    avoid="""
<p>If you believe technical skills alone determine compensation at senior levels, this will challenge that.</p>
<p>If you think switching companies will solve the ceiling, read on.</p>
""",
    expect="""
<p>The early career trajectory sets unrealistic expectations:</p>
<ul>
<li>Year 1: ₹6 LPA. Year 3: ₹15 LPA. Year 5: ₹28 LPA.</li>
<li>"At this rate, I'll hit ₹50 LPA by Year 7 and ₹1 Crore by Year 10."</li>
<li>The compound growth feels inevitable.</li>
</ul>
<p>Then something strange happens around Year 6-7. The automatic 20-30% hikes become 10-12%. Then 5-8%. The curve bends.</p>
""",
    reality="""
<p>The salary ceiling for individual contributors in India is structural, not personal.</p>

<p><strong>The Supply-Demand Imbalance:</strong> India produces enormous numbers of engineers at every level. At ₹40-50 LPA, companies can find excellent senior engineers easily. There's no shortage. The wage compression happens because the supply doesn't thin out the way it does at ₹80LPA+ leadership roles.</p>

<p><strong>The Leverage Problem:</strong> Senior ICs don't control budgets, teams, or strategy. They produce code—which, no matter how excellent, is valued less than the ability to make other people produce code. The ceiling reflects leverage, not skill.</p>

<p><strong>The Company Hierarchy:</strong> Most companies have rigid bands. Senior Engineer: ₹30-50 LPA. Staff Engineer: ₹50-75 LPA. But Staff roles are rare—maybe 1 for every 20 Senior Engineers. If your company doesn't have a Staff ladder, you've reached the local ceiling.</p>

<p><strong>The Job-Hopping Diminishing Returns:</strong> At junior levels, switching every 2 years generates 30-50% jumps. By senior level, it generates 15-25%—and companies start to question your stability. The arbitrage shrinks.</p>

<p><strong>The Ageism Factor:</strong> Whether spoken or not, a 40-year-old competing for Senior roles faces different dynamics than a 28-year-old. The industry's preference for younger engineers creates subtle headwinds.</p>
""",
    salary="""
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 25%">Experience</th>
            <th style="width: 25%">Typical Range</th>
            <th style="width: 25%">Growth Rate</th>
            <th style="width: 25%">Ceiling Factor</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Years 0-3</strong></td>
            <td>₹6-18 LPA</td>
            <td>25-40%/year</td>
            <td>Skill-limited</td>
        </tr>
        <tr>
            <td><strong>Years 4-6</strong></td>
            <td>₹18-35 LPA</td>
            <td>15-25%/year</td>
            <td>Role-limited</td>
        </tr>
        <tr>
            <td><strong>Years 7-10</strong></td>
            <td>₹32-50 LPA</td>
            <td>8-15%/year</td>
            <td>Leverage-limited</td>
        </tr>
        <tr>
            <td><strong>Years 10+</strong></td>
            <td>₹40-60 LPA (IC)</td>
            <td>5-10%/year</td>
            <td>Structurally capped</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*Product companies in Bangalore/Hyderabad. Service companies significantly lower.</p>
""",
    stuck_point="""
<p><strong>The "One More Skill" Delusion.</strong></p>

<p>Many developers facing the ceiling believe that learning Kubernetes, or Rust, or ML will break them through. It rarely does. The ceiling isn't about technical skills—it's about organizational leverage.</p>

<p>The trap is continually upskilling in technical areas while ignoring the visibility, influence, and relationships that create Staff-level impact.</p>

<p>Breaking the ceiling requires either: (1) joining a company with a real IC ladder against massive competition, (2) transitioning to management, or (3) accepting the ceiling and optimizing for work-life balance instead of salary growth.</p>
""",
    verdict="""
<p>The ceiling is real. Fighting it requires clarity about your path:</p>

<p><strong>To break through as IC:</strong></p>
<ul>
<li>Target the 5-10 companies in India with real Staff/Principal ladders</li>
<li>Build visible influence—internal tech talks, architecture decisions, mentorship</li>
<li>Specialize in areas with genuine scarcity (not just framework popularity)</li>
</ul>

<p><strong>To accept and optimize:</strong></p>
<ul>
<li>Recognize that ₹40-50 LPA is, objectively, an excellent income in India</li>
<li>Shift focus to work-life balance, interesting problems, and non-financial rewards</li>
<li>Stop the endless job-hopping for marginal gains that damage long-term prospects</li>
</ul>

<p>The ceiling isn't failure. It's reality. What matters is choosing consciously rather than fighting it blindly.</p>
""",
    seo_desc="Why senior developer salaries plateau at ₹40-50 LPA in India. The structural ceiling, leverage problem, and paths to break through or accept."
)

print("\n✅ Batch 3 (3 articles) created successfully!")
