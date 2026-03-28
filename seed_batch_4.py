"""
Seed batch 4: Articles 10-12
DevOps Reality, Tech Lead Trap, Performance Reviews
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

# ARTICLE 10: DevOps Reality
create_article(
    author=author1,
    cat_name="Software Engineering",
    slug="devops-sre-reality-india-oncall",
    title="The DevOps Reality: You're On-Call, Not In-Demand",
    persona="Engineers considering or already in DevOps/SRE roles expecting better work-life balance and higher demand.",
    avoid="""
<p>If you moved to DevOps to escape coding, you're in for a rude awakening.</p>
<p>If you believe DevOps means 9-5 with no production fires, read on.</p>
""",
    expect="""
<p>The DevOps/SRE promise is attractive:</p>
<ul>
<li>"DevOps engineers are in high demand—shortage everywhere."</li>
<li>"Automation means less repetitive work."</li>
<li>"SRE at Google pays $300K+ and you just write Python scripts."</li>
<li>"It's the future—every company needs DevOps."</li>
</ul>
<p>The certifications (AWS, Kubernetes, Terraform) feel like a clear path to career security.</p>
""",
    reality="""
<p>DevOps in India is often a different job than the Silicon Valley version.</p>

<p><strong>The On-Call Reality:</strong> Most DevOps/SRE roles come with on-call rotations. When production breaks at 3 AM, you're the one getting paged. The "automation" you build doesn't eliminate fires—it just means you're responsible for more systems when they burn.</p>

<p><strong>The Title Inflation:</strong> In many Indian companies, "DevOps Engineer" means "the person who manages Jenkins and deploys code." It's often glorified operations work without the architecture influence that makes SRE interesting.</p>

<p><strong>The Skill Trap:</strong> DevOps skills are simultaneously in demand and commoditized. Everyone knows Kubernetes basics. The differentiation is narrow: either you're deeply specialized in performance engineering and distributed systems, or you're competing with thousands of certified generalists.</p>

<p><strong>The Invisibility:</strong> When infrastructure works, nobody notices. When it breaks, everyone's angry. DevOps gets blamed for outages but rarely credited for uptime. The psychological toll of being the last line of defense is real.</p>

<p><strong>The Career Path Ambiguity:</strong> What comes after Senior DevOps? Platform Engineering Manager? Infrastructure Architect? The path is less defined than software engineering, and many DevOps engineers plateau at Staff-equivalent levels.</p>
""",
    salary="""
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 30%">Role</th>
            <th style="width: 25%">Experience</th>
            <th style="width: 25%">Salary Range (LPA)</th>
            <th style="width: 20%">On-Call?</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>DevOps Engineer</strong></td>
            <td>2-4 years</td>
            <td>₹10-20 LPA</td>
            <td>Usually yes</td>
        </tr>
        <tr>
            <td><strong>Senior DevOps/SRE</strong></td>
            <td>5-8 years</td>
            <td>₹20-40 LPA</td>
            <td>Almost always</td>
        </tr>
        <tr>
            <td><strong>Platform Engineer</strong></td>
            <td>6-10 years</td>
            <td>₹30-55 LPA</td>
            <td>Usually reduced</td>
        </tr>
        <tr>
            <td><strong>Infrastructure Architect</strong></td>
            <td>10+ years</td>
            <td>₹50-80 LPA</td>
            <td>Rarely</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*Product companies in major metros. On-call often comes with extra compensation (₹20-50K/month).</p>
""",
    stuck_point="""
<p><strong>The Certification Hamster Wheel.</strong></p>

<p>Many DevOps engineers collect certifications thinking each one increases their value. AWS → Kubernetes → Terraform → Azure → GCP. But certifications prove you learned, not that you can solve production problems at 3 AM.</p>

<p>The trap is spending weekends on certification prep while ignoring the incidents that would build real expertise. The best DevOps engineers are forged in production fires, not exam centers.</p>
""",
    verdict="""
<p>DevOps can be a strong career path, but go in with realistic expectations:</p>

<ul>
<li><strong>On-call is the job.</strong> If you hate being paged, hate DevOps. There's no version of this role without production responsibility.</li>
<li><strong>Specialize or compete.</strong> Generalist DevOps is crowded. Deep expertise in observability, security, or performance engineering differentiates you.</li>
<li><strong>Negotiate on-call compensation.</strong> Many companies underpay for on-call. It should add ₹20-50K/month to your package.</li>
<li><strong>Have an exit path.</strong> Platform engineering, infrastructure architecture, or moving into product engineering are common next moves.</li>
</ul>

<p>If you love systems, tolerate being woken at 3 AM, and find satisfaction in reliability, DevOps is a career. If you want predictable hours and visible impact, look elsewhere.</p>
""",
    seo_desc="The reality of DevOps and SRE roles in India. On-call burden, certification trap, and why it's different from the Silicon Valley version."
)

# ARTICLE 11: Tech Lead Trap
create_article(
    author=author2,
    cat_name="Software Engineering",
    slug="tech-lead-trap-responsibility-authority",
    title="The Tech Lead Trap: Responsibility Without Authority",
    persona="Senior engineers who became Tech Leads expecting more influence and finding more frustration.",
    avoid="""
<p>If you think becoming a Tech Lead means people listen to your technical opinions, prepare for disappointment.</p>
<p>If you believe the title comes with power, this is your reality check.</p>
""",
    expect="""
<p>The Tech Lead promotion seems like validation:</p>
<ul>
<li>"Finally, I'll have say in architecture decisions."</li>
<li>"I'll mentor the team and set technical direction."</li>
<li>"This is step one toward becoming an Engineering Manager or Architect."</li>
<li>"The title means my expertise is recognized."</li>
</ul>
<p>You imagine leading technical discussions, making design decisions that stick, and growing the next generation of engineers.</p>
""",
    reality="""
<p>The Tech Lead role is often the most frustrating position in engineering.</p>

<p><strong>The Authority Gap:</strong> You're responsible for technical outcomes but don't control hiring, firing, performance reviews, or prioritization. When a junior engineer underperforms, you can't fix it—but you're blamed for the team's output.</p>

<p><strong>The Meeting Tax:</strong> Your calendar fills with syncs, planning, and stakeholder alignment. The coding time that made you good at your job evaporates. You become less technical as the role demands more of it.</p>

<p><strong>The Sandwich Position:</strong> Engineering Managers push deadlines. Product Managers change requirements. Senior leadership wants faster delivery. The Tech Lead absorbs pressure from all directions with no authority to push back.</p>

<p><strong>The Career Ambiguity:</strong> Is Tech Lead a stepping stone to management? To Principal Engineer? To Architect? Companies rarely clarify. Many Tech Leads get stuck in the role for years, neither progressing toward management nor deepening as ICs.</p>

<p><strong>The Burnout Pattern:</strong> The combination of responsibility without authority, declining technical skills, and constant context-switching makes Tech Lead one of the highest burnout roles in engineering.</p>
""",
    salary="""
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 30%">Role</th>
            <th style="width: 25%">Salary (LPA)</th>
            <th style="width: 25%">Authority</th>
            <th style="width: 20%">Stress</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Senior Engineer</strong></td>
            <td>₹25-40 LPA</td>
            <td>Technical scope</td>
            <td>Medium</td>
        </tr>
        <tr>
            <td><strong>Tech Lead</strong></td>
            <td>₹35-55 LPA</td>
            <td>Technical + team quality</td>
            <td>High</td>
        </tr>
        <tr>
            <td><strong>Engineering Manager</strong></td>
            <td>₹45-70 LPA</td>
            <td>People + delivery</td>
            <td>High</td>
        </tr>
        <tr>
            <td><strong>Staff Engineer</strong></td>
            <td>₹50-80 LPA</td>
            <td>Technical strategy</td>
            <td>Medium-High</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*The Tech Lead salary bump is often 10-20%, while the responsibility increase is 50-100%.</p>
""",
    stuck_point="""
<p><strong>The "Prove You Can Manage" Trap.</strong></p>

<p>Many companies use Tech Lead as a trial period for management without giving management authority. You're expected to "prove" you can lead without the tools to actually lead.</p>

<p>The trap is accepting this indefinitely, hoping for promotion to Engineering Manager. But if you're doing well as Tech Lead, there's no incentive to promote you—you're already doing the work without the title.</p>

<p>The stuck Tech Lead waits for recognition that never comes while their technical skills erode and their patience depletes.</p>
""",
    verdict="""
<p>Before accepting a Tech Lead role, negotiate explicitly:</p>

<ul>
<li><strong>What authority comes with the responsibility?</strong> Influence on hiring? Input on performance reviews? Veto on technical decisions?</li>
<li><strong>What's the career path?</strong> Is this a step toward Engineering Manager? Staff Engineer? Get it in writing.</li>
<li><strong>What percentage of your time should be coding?</strong> Less than 30% means you'll lose technical depth. Is that what you want?</li>
<li><strong>What's the timeline?</strong> If you're "proving yourself," when is the evaluation?</li>
</ul>

<p>If the answers are vague, the role is a trap. You're being handed accountability without the means to fulfill it. Either negotiate real authority or stay as a Senior Engineer until a real opportunity emerges.</p>
""",
    seo_desc="The Tech Lead trap explained. Why responsibility without authority leads to burnout, and what to negotiate before accepting the role."
)

# ARTICLE 12: Performance Reviews
create_article(
    author=author1,
    cat_name="Career Strategy",
    slug="performance-review-reality-ratings-india",
    title="The Performance Review Reality: How Ratings Actually Work",
    persona="Employees who work hard expecting fair performance ratings and are confused when ratings don't match effort.",
    avoid="""
<p>If you believe performance reviews are objective assessments of your work, this will disturb you.</p>
<p>If you think working hard guarantees a good rating, read on.</p>
""",
    expect="""
<p>The meritocracy narrative says:</p>
<ul>
<li>"Do great work, get great ratings."</li>
<li>"Your manager will advocate for you."</li>
<li>"The system rewards top performers."</li>
<li>"Ratings directly determine raises and promotions."</li>
</ul>
<p>So you work hard, hit your goals, and expect the review cycle to recognize it.</p>
""",
    reality="""
<p>Performance reviews are political negotiations, not objective assessments.</p>

<p><strong>The Curve:</strong> Most companies use forced distribution (bell curve). Only 10-15% can get "Exceeds Expectations." Your rating isn't about your absolute performance—it's about your performance relative to others AND your manager's ability to argue for you against other managers.</p>

<p><strong>The Manager's Stack:</strong> Before calibration meetings, your manager ranks their team. If you're #4 in a team of 6, you're getting "Meets Expectations" regardless of your actual performance. Your rating is partly determined by your teammates, not just you.</p>

<p><strong>The Visibility Game:</strong> Quiet excellence is underrated. The person who presents at all-hands gets higher visibility than the one who fixed the critical production issues at 2 AM. Performance reviews measure perceived impact, which correlates imperfectly with actual impact.</p>

<p><strong>The Recency Bias:</strong> Reviews disproportionately weight the last 2-3 months. A strong finish matters more than consistent performance. The system rewards those who time their visible work near review cycles.</p>

<p><strong>The Budget Reality:</strong> Raises are budgeted before reviews happen. The total pool is fixed. Even if everyone "exceeds expectations," the money is the same. Ratings are often reverse-engineered from budget constraints.</p>
""",
    salary="""
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 25%">Rating</th>
            <th style="width: 25%">% of Employees</th>
            <th style="width: 25%">Typical Raise</th>
            <th style="width: 25%">Promotion?</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Exceptional</strong></td>
            <td>5-10%</td>
            <td>15-25%</td>
            <td>Usually</td>
        </tr>
        <tr>
            <td><strong>Exceeds</strong></td>
            <td>15-25%</td>
            <td>10-15%</td>
            <td>Sometimes</td>
        </tr>
        <tr>
            <td><strong>Meets</strong></td>
            <td>50-60%</td>
            <td>5-8%</td>
            <td>Rarely</td>
        </tr>
        <tr>
            <td><strong>Below</strong></td>
            <td>10-15%</td>
            <td>0-3%</td>
            <td>Never</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*Typical large tech company. Percentages are forced distribution, not earned.</p>
""",
    stuck_point="""
<p><strong>The "Work Harder" Fallacy.</strong></p>

<p>When you get a disappointing rating, the instinct is to work harder. But if the problem was visibility, politics, or your manager's negotiating power—more hard work doesn't fix it.</p>

<p>The trap is doubling down on effort when the system flaw is elsewhere. People burn out chasing ratings that were never determined by effort alone.</p>

<p>The fix requires understanding the game: building relationships with skip-levels, timing visible work around reviews, and choosing managers who advocate well—not just working harder.</p>
""",
    verdict="""
<p>To navigate reviews effectively:</p>

<ul>
<li><strong>Manage up.</strong> Your manager's perception matters more than reality. Make your work visible to them specifically.</li>
<li><strong>Build skip-level relationships.</strong> Your manager's manager participates in calibration. They should know who you are.</li>
<li><strong>Time your big wins.</strong> Land something visible in the 2 months before reviews. Recency bias is real and exploitable.</li>
<li><strong>Document everything.</strong> Come to self-reviews with a list of accomplishments. Managers forget. You shouldn't.</li>
<li><strong>Understand the curve.</strong> Ask your manager where you rank on their team. If you're not top 2-3, your rating is capped.</li>
</ul>

<p>None of this means "don't work hard." It means work hard AND play the game. Pretending the game doesn't exist just means you lose.</p>
""",
    seo_desc="How performance reviews actually work in Indian tech companies. Bell curves, visibility games, and why hard work alone doesn't guarantee good ratings."
)

print("\n✅ Batch 4 (3 articles) created successfully!")
