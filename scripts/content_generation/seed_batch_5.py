"""
Seed batch 5: Articles 13-17 (Final batch)
Job Hopping, Culture Fit, HR Conversations, Passion Fallacy, Work-Life Balance
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

# ARTICLE 13: Job Hopping After 35
create_article(
    author=author2,
    cat_name="Career Strategy",
    slug="job-hopping-stops-working-after-35",
    title="Why Job Hopping Stops Working After 35",
    persona="Mid-career professionals (32-40) who've relied on job-hopping for salary growth and find it slowing down.",
    avoid="""
<p>If you've switched jobs every 18 months and don't understand why it's not working anymore, this explains why.</p>
<p>If you think loyalty is for suckers at any age, this might change your mind.</p>
""",
    expect="""
<p>Job-hopping worked brilliantly in your 20s:</p>
<ul>
<li>Switch every 2 years, get 30-50% jumps.</li>
<li>Build a resume of brand names.</li>
<li>"Loyalty doesn't pay"—everyone said so.</li>
<li>By 35, you'd be earning ₹80 LPA at this trajectory.</li>
</ul>
<p>The strategy was optimal when you were young. The question is why it stops.</p>
""",
    reality="""
<p>After 35, the job market changes its relationship with you.</p>

<p><strong>The Stability Question:</strong> Hiring managers at senior levels look for evidence you can commit. A resume with 6 jobs in 10 years raises questions at junior levels—but it's often a hard "no" for Director+ roles. They're hiring someone to build something over years, not optimize their salary.</p>

<p><strong>The Age Math:</strong> When you're 26 and hopping, you're "ambitious." When you're 38 and hopping, you're "unstable" or "difficult." The same behavior is interpreted differently. Fair? No. Real? Yes.</p>

<p><strong>The Network Decay:</strong> Job hoppers build wide but shallow networks. The relationships that matter for senior roles—people who will stake their reputation on you—take years to build. Constant departures leave a trail of acquaintances, not advocates.</p>

<p><strong>The Skill Depth Illusion:</strong> Each short stint gives you exposure but not mastery. By your 5th company, you've "done" the same things over and over without ever seeing a initiative through to completion. Your breadth is impressive; your depth is questionable.</p>

<p><strong>The Diminishing Returns:</strong> At ₹40-60 LPA, the supply of candidates is larger. Companies have options. The 50% jumps become 15-20% becomes lateral. The arbitrage shrinks as you move up the pay curve.</p>
""",
    salary="""
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 25%">Age/Stage</th>
            <th style="width: 25%">Job-Hop Benefit</th>
            <th style="width: 25%">Loyalty Benefit</th>
            <th style="width: 25%">Optimal Strategy</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>22-28</strong></td>
            <td>Very High (30-50%)</td>
            <td>Low</td>
            <td>Hop freely</td>
        </tr>
        <tr>
            <td><strong>29-34</strong></td>
            <td>Medium (20-30%)</td>
            <td>Medium</td>
            <td>Strategic hops</td>
        </tr>
        <tr>
            <td><strong>35-42</strong></td>
            <td>Low (10-20%)</td>
            <td>High</td>
            <td>Build tenure</td>
        </tr>
        <tr>
            <td><strong>43+</strong></td>
            <td>Very Low</td>
            <td>Very High</td>
            <td>Stay put or exit</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*Optimal strategy shifts from mobility to stability as you age.</p>
""",
    stuck_point="""
<p><strong>The "One More Jump" Trap.</strong></p>

<p>Job hoppers in their late 30s often believe one more strategic jump will fix their trajectory. But each jump after 35 raises more questions. The market starts asking: "Why can't this person stay anywhere?"</p>

<p>The trap is not realizing the strategy has expired. What worked at 28 is actively harming you at 38. But admitting that means confronting a career built on optimization that's now working against you.</p>
""",
    verdict="""
<p>If you're over 35 with a hoppy resume:</p>

<ul>
<li><strong>Stop now.</strong> Your next role should be a 4-5 year commitment. Prove you can stay.</li>
<li><strong>Choose carefully.</strong> Since you're committing longer, the choice matters more. Don't chase salary; chase growth trajectory and leadership quality.</li>
<li><strong>Explain the pattern.</strong> In interviews, own the hopping and explain your decision to change. "I optimized for learning in my 20s and am now optimizing for impact" is a better story than hope they don't notice.</li>
<li><strong>Build internal reputation.</strong> The currency at senior levels is "people who will vouch for you." That takes years, not quarters.</li>
</ul>

<p>The game changes. Adapt or stagnate.</p>
""",
    seo_desc="Why job-hopping stops working in your late 30s. How the market treats career mobility differently as you age, and when to switch strategies."
)

# ARTICLE 14: Culture Fit Trap
create_article(
    author=author1,
    cat_name="Career Strategy",
    slug="culture-fit-trap-hiring-reality",
    title="The 'Culture Fit' Trap: What Interviewers Actually Mean",
    persona="Job seekers who've been rejected for 'culture fit' without understanding what that actually means.",
    avoid="""
<p>If you believe culture fit is about whether you'd be friends with the team, you're missing the point.</p>
<p>If you think technical skills alone should get you hired, this explains why they don't.</p>
""",
    expect="""
<p>When you hear about "culture fit," it sounds reasonable:</p>
<ul>
<li>"We want people who share our values."</li>
<li>"It's about working well with the team."</li>
<li>"Skills matter, but so does being a good colleague."</li>
</ul>
<p>It seems fair. Companies want cohesive teams. What could be wrong with that?</p>
""",
    reality="""
<p>"Culture fit" is often code for things companies can't legally say.</p>

<p><strong>The Likeability Filter:</strong> Culture fit frequently means "people like you in the interview." Interviewers are asked "Would you want to work with this person?" The answer reflects personal affinity as much as professional assessment.</p>

<p><strong>The Conformity Test:</strong> In many companies, "culture fit" means you think, speak, and act like the existing team. Diversity of thought is threatening. The candidate who challenges assumptions is "not a fit." The one who mirrors the interviewer is "perfect."</p>

<p><strong>The Bias Laundering:</strong> Studies consistently show "culture fit" disproportionately screens out underrepresented groups. It's a socially acceptable way to reject people who seem "different" without articulating why. Age, background, education, accent—all can be rejected as "not a fit" without legal consequence.</p>

<p><strong>The Moving Target:</strong> Unlike technical skills, culture fit has no rubric. Different interviewers apply different standards. A candidate might "fit" with one team and not another in the same company. It's inherently subjective.</p>

<p><strong>What It Sometimes Means:</strong> Sometimes culture fit is legitimate—someone who thrives in startups might struggle in enterprise, or vice versa. But this is the minority of cases. More often, it's a judgment call dressed as a principle.</p>
""",
    salary="""
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 35%">What They Say</th>
            <th style="width: 65%">What It Often Means</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>"Not a culture fit"</td>
            <td>I didn't personally like them / They seemed different</td>
        </tr>
        <tr>
            <td>"Overqualified"</td>
            <td>Too expensive / Will leave soon / Makes me uncomfortable</td>
        </tr>
        <tr>
            <td>"Not senior enough"</td>
            <td>Didn't perform confidence well / Seems too junior</td>
        </tr>
        <tr>
            <td>"Communication concerns"</td>
            <td>Accent / Speaking style / Not assertive enough</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*This is not universal—some feedback is genuine. But "culture fit" is frequently a cover.</p>
""",
    stuck_point="""
<p><strong>Changing Yourself to Fit.</strong></p>

<p>After multiple "culture fit" rejections, some candidates start suppressing their personality: talking less, hedging opinions, mirroring interviewers. They become inauthentic to pass the filter.</p>

<p>The trap is that even if this works, you've joined a company that doesn't accept who you are. The culture that rejected your authentic self will do so again in performance reviews, promotions, and daily interactions.</p>

<p>The alternative—finding companies where you genuinely fit—is harder but sustainable.</p>
""",
    verdict="""
<p>How to navigate the culture fit game:</p>

<ul>
<li><strong>Research the actual culture.</strong> Glassdoor, Blind, LinkedIn messages to employees. Understand who thrives there before interviewing.</li>
<li><strong>Ask what culture fit means to them.</strong> In interviews, ask: "What does culture fit mean here specifically?" Vague answers are a red flag.</li>
<li><strong>Observe the interviewers.</strong> If they're all similar (background, style, demographics), "culture fit" likely means conformity.</li>
<li><strong>Don't contort yourself.</strong> If you have to fundamentally suppress who you are to pass, you'll be miserable if you succeed.</li>
<li><strong>Interpret rejections carefully.</strong> "Culture fit" rejection often says more about them than you. Don't internalize it.</li>
</ul>

<p>The goal isn't to fit every culture—it's to find the ones where you actually belong.</p>
""",
    seo_desc="What 'culture fit' really means in hiring. How it's used, abused, and how to navigate rejection for being 'not the right fit.'"
)

# ARTICLE 15: HR Conversations Reality
create_article(
    author=author2,
    cat_name="Career Strategy",
    slug="hr-conversations-what-matters-india",
    title="HR Conversations That Actually Matter (And Ones That Don't)",
    persona="Employees trying to navigate HR—performance issues, salary negotiations, complaints—and not understanding HR's true role.",
    avoid="""
<p>If you think HR is your advocate, this will calibrate your expectations.</p>
<p>If you've been burned by trusting HR with sensitive information, you'll understand why.</p>
""",
    expect="""
<p>HR positions itself as employee-friendly:</p>
<ul>
<li>"We're here to support you."</li>
<li>"HR is a safe space to raise concerns."</li>
<li>"We advocate for fair treatment."</li>
<li>"Come to us with any issues."</li>
</ul>
<p>Many employees believe HR exists to help them. This belief often survives until they need help.</p>
""",
    reality="""
<p>HR exists to protect the company, not you. Understanding this changes how you interact with them.</p>

<p><strong>The Fundamental Allegiance:</strong> HR is paid by the company, reports to leadership, and exists to mitigate legal and operational risk for the organization. When your interests and the company's interests conflict, HR serves the company.</p>

<p><strong>What HR Protects Against:</strong> Lawsuits, PR disasters, regulatory violations, and managers who create legal liability. If your complaint threatens any of these, HR will act—to protect the company's exposure, not necessarily to get you justice.</p>

<p><strong>When HR Helps You:</strong> When helping you also helps the company. Negotiating a smooth exit? They want you to sign a clean separation. Addressing harassment that could become a lawsuit? They'll act. Requesting reasonable accommodations required by law? They'll comply.</p>

<p><strong>When HR Doesn't Help:</strong> Complaints about unfair treatment that don't create legal exposure. Conflicts with high-value managers. Concerns about culture that aren't actionable. These often get documented, nodded at, and forgotten.</p>

<p><strong>The Documentation Trap:</strong> Every conversation with HR is documented and can be used in future actions—including against you. That "confidential" concern you raised is now in a file that your manager might access during a performance issue.</p>
""",
    salary="""
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 35%">Conversation Type</th>
            <th style="width: 35%">HR's Actual Role</th>
            <th style="width: 30%">Your Strategy</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Harassment/Discrimination</strong></td>
            <td>Minimize company liability</td>
            <td>Document externally first</td>
        </tr>
        <tr>
            <td><strong>Manager Conflicts</strong></td>
            <td>Protect the higher-value asset</td>
            <td>Assume it reaches your manager</td>
        </tr>
        <tr>
            <td><strong>Salary Negotiation</strong></td>
            <td>Stay within budget constraints</td>
            <td>Have an external offer</td>
        </tr>
        <tr>
            <td><strong>Exit/Layoff</strong></td>
            <td>Clean separation, no lawsuits</td>
            <td>Everything is negotiable</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*HR helps when your interests align with the company's. Otherwise, protect yourself.</p>
""",
    stuck_point="""
<p><strong>The "Just Venting" Mistake.</strong></p>

<p>Many employees treat HR as a therapist. They share frustrations, concerns about managers, or doubts about their role—expecting empathy and confidentiality.</p>

<p>But HR is documenting. That "casual" conversation about your manager might become evidence that you have attitude problems. The frustration you vented is now part of your file.</p>

<p>The trap is treating a professional function as a personal one. HR professionals may be individually kind, but their job is not to be your friend.</p>
""",
    verdict="""
<p>Rules for dealing with HR:</p>

<ul>
<li><strong>Never complain without documentation.</strong> If you're raising an issue, have your own records first. Emails, dates, witnesses.</li>
<li><strong>Assume everything is on the record.</strong> Say only what you'd be comfortable reading in a termination document later.</li>
<li><strong>Understand their incentives.</strong> Ask yourself: "Does fixing my problem help or hurt the company?" That answers whether HR will help.</li>
<li><strong>Use HR for transactional things.</strong> Benefits, paperwork, formal processes. They're excellent for these.</li>
<li><strong>Find allies elsewhere.</strong> For actual career advice and support, build relationships with mentors and peers—not HR.</li>
</ul>

<p>This isn't cynicism. It's clarity about the role HR plays. They're not villains. They're just not your advocates.</p>
""",
    seo_desc="What HR actually does vs. what employees expect. When to involve HR, when to avoid them, and how to protect yourself in workplace issues."
)

# ARTICLE 16: Passion as Career Strategy
create_article(
    author=author1,
    cat_name="Career Strategy",
    slug="passion-luxury-not-strategy-india",
    title="Why 'Follow Your Passion' Is Advice for the Privileged",
    persona="Professionals feeling guilty that they don't love their jobs, wondering if they should quit to pursue passion.",
    avoid="""
<p>If you believe everyone should love their work, this challenges that assumption.</p>
<p>If you're financially secure and wondering about passion, this isn't about you.</p>
""",
    expect="""
<p>The passion narrative is everywhere:</p>
<ul>
<li>"Do what you love and you'll never work a day in your life."</li>
<li>"Find your passion and the money will follow."</li>
<li>"Life's too short for a job you don't love."</li>
<li>"The most successful people are passionate about their work."</li>
</ul>
<p>These quotes adorn LinkedIn posts from CEOs, entrepreneurs, and people who've already made it.</p>
""",
    reality="""
<p>Passion as career advice is survivorship bias wrapped in privilege.</p>

<p><strong>The Safety Net Reality:</strong> People who "follow their passion" successfully often have safety nets: family money, working spouses, savings, or connections. The struggling musician whose parents pay rent isn't taking the same risk as someone supporting their family.</p>

<p><strong>The Passion-for-Pay Paradox:</strong> Fields that people love (art, writing, music, sports) are flooded with talent, which suppresses wages. Passionate people will work for less. Your passion is often someone else's leverage.</p>

<p><strong>The Developing Mastery Path:</strong> Research shows passion often follows skill, not the other way around. People become passionate about things they're good at. "Find your passion" has it backwards—get skilled, and passion may emerge.</p>

<p><strong>The Indian Middle-Class Reality:</strong> For most Indian families, work exists to provide stability—children's education, parents' healthcare, housing security. Asking "am I passionate?" when your parents depend on your income is a luxury not everyone has.</p>

<p><strong>The Reframe:</strong> Work doesn't have to be passion. Work can be: interesting enough, paying well enough, leaving enough time for things you actually love. This is a valid, even admirable, life design.</p>
""",
    salary="""
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 35%">Career Philosophy</th>
            <th style="width: 35%">Financial Requirement</th>
            <th style="width: 30%">Middle-Class Viability</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>"Follow Your Passion"</strong></td>
            <td>3-5 years runway or family support</td>
            <td>Low</td>
        </tr>
        <tr>
            <td><strong>"Build Skills, Then Pivot"</strong></td>
            <td>6-12 months savings</td>
            <td>Medium</td>
        </tr>
        <tr>
            <td><strong>"Optimize for Balance"</strong></td>
            <td>Stable income with boundaries</td>
            <td>High</td>
        </tr>
        <tr>
            <td><strong>"Work Funds Life"</strong></td>
            <td>Sustainable income, pursue passion outside</td>
            <td>Highest</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*The advice you should take depends on your financial reality, not Instagram wisdom.</p>
""",
    stuck_point="""
<p><strong>The Guilt of Not Loving Your Job.</strong></p>

<p>The passion narrative creates shame. If you're not passionate about your work, something must be wrong with you. You're "settling." You're not "living your best life."</p>

<p>This guilt drives people to quit stable jobs for passion projects that fail within 18 months. The passion-shame-impulse-regret cycle destroys careers and finances.</p>

<p>The healthier reframe: You are not your job. It's okay for work to be work. What matters is whether you're building the life you want, not whether your job is your calling.</p>
""",
    verdict="""
<p>Passion is not required for a good career. Here's a more realistic framework:</p>

<ul>
<li><strong>Can you tolerate the work?</strong> Not love—tolerate. Most days shouldn't feel like suffering.</li>
<li><strong>Does it pay what you need?</strong> Enough to meet obligations and save for the future.</li>
<li><strong>Does it leave room for life?</strong> Energy and time for family, hobbies, rest.</li>
<li><strong>Is there growth?</strong> Learning something, even if slowly.</li>
</ul>

<p>If you answer yes to these four, you have a good job. Whether you're "passionate" is irrelevant. Many of the happiest people work jobs they find merely fine and build rich lives around them.</p>

<p>Passion as career advice is for people who can afford to fail. For everyone else, sustainability beats intensity.</p>
""",
    seo_desc="Why 'follow your passion' is bad advice for most people. The privilege behind passion narratives and more realistic career frameworks."
)

# ARTICLE 17: Work-Life Balance Myth
create_article(
    author=author2,
    cat_name="Career Strategy",
    slug="work-life-balance-myth-high-performers",
    title="The Work-Life Balance Lie: What High Performers Don't Tell You",
    persona="Professionals struggling to achieve 'work-life balance' while watching high performers seem to have it all.",
    avoid="""
<p>If you believe you can outperform while working 40 hours, this will challenge that.</p>
<p>If you're already burning out and can't do more, this isn't asking you to—it's explaining what you're competing against.</p>
""",
    expect="""
<p>The work-life balance narrative promises:</p>
<ul>
<li>"Set boundaries and protect your time."</li>
<li>"Productivity matters, not hours."</li>
<li>"Top performers work smarter, not longer."</li>
<li>"You can have a great career and a full personal life."</li>
</ul>
<p>It sounds achievable. Just be efficient. Draw lines. Have it all.</p>
""",
    reality="""
<p>At the highest levels, work-life balance is largely a myth—but it's not talked about for PR reasons.</p>

<p><strong>The Hours Reality:</strong> Almost every successful executive, founder, or senior leader worked unsustainable hours for stretches of their career. The VP of Engineering who talks about balance at 45 didn't have it at 32. They paid the price earlier.</p>

<p><strong>The Selection Bias:</strong> The people at the top are survivors who either (1) didn't burn out, (2) had support systems (nannies, uninvolved partners, family money), or (3) sacrificed things they don't mention. Their "tips for balance" rarely account for this.</p>

<p><strong>The Trade-Off Truth:</strong> Peak career achievement, peak parenting, peak fitness, and peak social life are almost impossible simultaneously. High performers often have one or two things in great shape and everything else in managed neglect.</p>

<p><strong>The "Season" Framework:</strong> Some reframe balance as seasonal. There are career seasons where you push hard (startup years, promotion push). There are life seasons where you pull back (young children, health issues). Trying to balance in every season is often failing at all of them.</p>

<p><strong>What Balance Actually Means:</strong> Real balance isn't equal time—it's intentional trade-offs you've chosen and can live with. The problem isn't imbalance. It's imbalance you didn't choose.</p>
""",
    salary="""
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 30%">Career Stage</th>
            <th style="width: 30%">Typical Hours (High Performers)</th>
            <th style="width: 40%">What Gets Sacrificed</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Early Career (0-5y)</strong></td>
            <td>50-60 hrs/week</td>
            <td>Sleep, hobbies, sometimes relationships</td>
        </tr>
        <tr>
            <td><strong>Growth Years (5-12y)</strong></td>
            <td>55-70 hrs/week</td>
            <td>Fitness, extended family, downtime</td>
        </tr>
        <tr>
            <td><strong>Leadership (12-20y)</strong></td>
            <td>45-60 hrs/week + always on</td>
            <td>Mental peace, hobbies, sometimes health</td>
        </tr>
        <tr>
            <td><strong>Executive (20+y)</strong></td>
            <td>Variable but high</td>
            <td>Privacy, some relationships, normalcy</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*This is descriptive, not prescriptive. It's what happens, not what should happen.</p>
""",
    stuck_point="""
<p><strong>The Comparison Trap.</strong></p>

<p>Social media shows the highlight reels: the VP working out at 6 AM, the MD at their kid's recital, the CTO on vacation. You don't see the missed events, the 11 PM emails from vacation, the nanny who enables it all.</p>

<p>Comparing your behind-the-scenes to their highlights creates despair. They're not balanced—they're curating.</p>

<p>The trap is believing balance is possible for everyone if you just try harder. For many high performers, it wasn't possible—they just don't say so publicly.</p>
""",
    verdict="""
<p>Instead of chasing "balance," try intentional imbalance:</p>

<ul>
<li><strong>Choose your season.</strong> Are you in a push season or a recovery season? Act accordingly without guilt.</li>
<li><strong>Pick your 2-3 priorities.</strong> Career, health, family, social, hobbies—you can excel at 2-3, not all 5. Choose consciously.</li>
<li><strong>Reject the false choice.</strong> You don't have to either burn out OR give up ambition. Find sustainable intensity for your season.</li>
<li><strong>Define your own success.</strong> Maybe Director is enough. Maybe working 40 hours is enough. Define your enough before society does.</li>
</ul>

<p>The goal isn't balance. It's alignment between your life and your values. If you're working hard for things you care about, that's not imbalance—that's purpose.</p>

<p>The problem is when you're sacrificing for things you don't actually want. Fix that, not the hours.</p>
""",
    seo_desc="The truth about work-life balance at senior levels. What high performers sacrifice, seasonal thinking, and achieving alignment over balance."
)

print("\n✅ Final batch (5 articles) created successfully!")
print("Total new articles created: 17")
