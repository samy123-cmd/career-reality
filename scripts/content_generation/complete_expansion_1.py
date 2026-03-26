"""
Complete content expansion for ALL remaining thin articles (IDs 4, 16-28)
Adding full content to all article fields to reach 1500+ words
"""
import os
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from content.models import Article
import re

def count_words(text):
    if not text:
        return 0
    clean = re.sub(r'<[^>]+>', ' ', text)
    return len(clean.split())

# Full expansions for articles still under 1000 words
full_content = {
    4: {  # Digital Marketing - 907 words, need ~600 more
        "who_should_avoid": """<p><strong>Digital Marketing Is Wrong For You If:</strong></p>

<ul>
<li><strong>You want creative control</strong>: Client and data dictate what you create</li>
<li><strong>You dislike constant platform changes</strong>: Meta and Google update weekly</li>
<li><strong>You want deep expertise in one thing</strong>: Marketing requires generalist breadth</li>
<li><strong>You expect work-life balance at agencies</strong>: 60-hour weeks are common</li>
<li><strong>You think "creative" means "artistic freedom"</strong>: It means "effective at conversion"</li>
</ul>

<p><strong>Digital Marketing Might Work If:</strong></p>

<ul>
<li><strong>You enjoy data-driven optimization</strong>: Testing beats intuition</li>
<li><strong>You like variety</strong>: No two campaigns are identical</li>
<li><strong>You're comfortable with constant change</strong>: Platform updates excite, not stress you</li>
<li><strong>You're okay with roles that are undervalued by tech culture</strong>: Marketing isn't engineering</li>
<li><strong>You plan to specialize</strong>: SEO, CRO, or analytics focus leads to real expertise</li>
</ul>

<p><strong>The Skills That Actually Matter:</strong></p>

<div class="chart-container">
<h4>📊 Digital Marketing Skill Value</h4>
<table class="data-table">
<tr><th>Skill</th><th>Market Demand</th><th>Salary Premium</th><th>Replaceability</th></tr>
<tr><td>Performance ads execution</td><td>High</td><td>Low (+5%)</td><td>Very High</td></tr>
<tr><td>SEO (technical depth)</td><td>High</td><td>Medium (+15%)</td><td>Medium</td></tr>
<tr><td>Marketing analytics/SQL</td><td>Very High</td><td>High (+25%)</td><td>Low</td></tr>
<tr><td>Marketing automation</td><td>High</td><td>High (+20%)</td><td>Medium</td></tr>
<tr><td>CRO/experimentation</td><td>Medium-High</td><td>High (+20%)</td><td>Low</td></tr>
</table>
</div>

<p>The marketers who learn to code SQL queries and understand attribution modeling command premiums. The ones who only know how to push buttons in Facebook Ads Manager are replaceable.</p>""",

        "verdict": """<p><strong>The Digital Marketing Reality Check:</strong></p>

<p>Digital marketing is legitimate work but rarely what the courses sell. You'll spend more time in spreadsheets than on creative briefs. You'll optimize performance metrics, not brand narratives. The "creative" work happens occasionally between reporting cycles.</p>

<p><strong>The Uncomfortable Question:</strong></p>

<p>Are you drawn to marketing because you genuinely enjoy data-driven optimization, or because you thought it was the creative path that didn't require technical skills? If it's the latter, you may be in for a rude awakening.</p>

<p><strong>What Actually Works:</strong></p>

<ol>
<li>Start agency to learn fast, but set a 2-3 year timer</li>
<li>Move to in-house or product marketing by year 4</li>
<li>Build data skills early (SQL, analytics, attribution)</li>
<li>Specialize in one high-value area (SEO, CRO, automation)</li>
<li>Consider growth roles that blend marketing with product</li>
<li>Don't stay past year 3 if you're still just an "executor"</li>
</ol>

<p>Digital marketing CAN lead to good careers. The path requires intentionality—not just showing up and running ads.</p>"""
    },

    16: {  # Upskilling - 890 words, need ~400 more
        "who_should_avoid": """<p><strong>The Upskilling Warning Signs:</strong></p>

<ul>
<li><strong>You have 15+ certifications but no senior role</strong>: The problem isn't skills</li>
<li><strong>You buy courses to feel productive</strong>: Learning becomes procrastination</li>
<li><strong>Your resume lists skills, not accomplishments</strong>: Certification collection is a red flag</li>
<li><strong>You're more comfortable learning than leading</strong>: Comfort zone avoidance</li>
<li><strong>Each course feels urgent</strong>: Anxiety, not strategy, drives your learning</li>
</ul>

<p><strong>What Actually Moves Careers After Year 5:</strong></p>

<div class="chart-container">
<h4>📊 Career Drivers by Stage</h4>
<table class="data-table">
<tr><th>Stage</th><th>Primary Career Driver</th><th>Secondary Driver</th></tr>
<tr><td>Years 0-3</td><td>Technical skills</td><td>Execution speed</td></tr>
<tr><td>Years 3-7</td><td>Technical depth + soft skills</td><td>Track record</td></tr>
<tr><td>Years 7-12</td><td>Leadership + influence</td><td>Business impact</td></tr>
<tr><td>Years 12+</td><td>Judgment + relationships</td><td>Reputation</td></tr>
</table>
</div>

<p>After year 7, technical courses provide diminishing returns. What you need is executive presence, stakeholder management, and strategic thinking—skills no Udemy course teaches effectively.</p>""",

        "verdict": """<p><strong>The Upskilling Truth:</strong></p>

<p>Upskilling is the right answer in years 0-7. After that, it's often an avoidance mechanism. The skills that matter most—leadership, influence, business judgment—aren't learned in courses. They're practiced in rooms, in hard conversations, in visible initiatives.</p>

<p><strong>The Uncomfortable Question:</strong></p>

<p>When did you last invest time in developing your leadership presence, communication skills, or business acumen? If your professional development budget goes 90% to technical skills after year 7, you're optimizing the wrong axis.</p>

<p><strong>What Actually Works:</strong></p>

<ol>
<li>Stop taking technical courses after year 7-8 unless genuinely needed for a specific project</li>
<li>Invest in leadership, communication, and presentation skills instead</li>
<li>Spend time with people 1-2 levels above you—observe how they operate</li>
<li>Lead initiatives that give you cross-functional visibility</li>
<li>Learn the business, not just the technology</li>
<li>Replace certificate collecting with relationship building</li>
</ol>"""
    },

    17: {  # IT Services - 903 words, need ~400 more
        "who_should_avoid": """<p><strong>Signs You're Staying Too Long in IT Services:</strong></p>

<ul>
<li><strong>You've been "comfortable" for 2+ years</strong>: Comfort is stagnation in disguise</li>
<li><strong>Your technical skills are legacy-focused</strong>: Still working with technologies from 2015</li>
<li><strong>You haven't designed anything end-to-end</strong>: Only implemented client specs</li>
<li><strong>Product company interviews intimidate you</strong>: System design questions feel alien</li>
<li><strong>Your network is all services colleagues</strong>: No connections to product world</li>
</ul>

<p><strong>Comparison: IT Services Career vs Product Career</strong></p>

<div class="chart-container">
<h4>📊 Career Value Accumulation</h4>
<table class="data-table">
<tr><th>Factor</th><th>IT Services (10 years)</th><th>Product (10 years)</th></tr>
<tr><td>Technical depth</td><td>Shallow (many tech, none deeply)</td><td>Deep (mastery of few)</td></tr>
<tr><td>Design experience</td><td>Minimal (implement specs)</td><td>Extensive (own systems)</td></tr>
<tr><td>Ownership mindset</td><td>Resource/hour mindset</td><td>Product owner mindset</td></tr>
<tr><td>Future career options</td><td>Narrowing</td><td>Expanding</td></tr>
<tr><td>Interview performance</td><td>Struggles with design rounds</td><td>Strong design foundation</td></tr>
</table>
</div>""",

        "verdict": """<p><strong>The IT Services Reality:</strong></p>

<p>IT services is a valid starting point but a dangerous long-term destination. The skills you build stop compounding around year 4-5. The resume perception shifts from "experienced" to "stuck." The salary gap to product companies widens irreversibly.</p>

<p><strong>The Uncomfortable Question:</strong></p>

<p>If you're 5+ years into IT services, what's your concrete plan to leave? "I'll apply next year" is what you said last year. Without a plan, you're defaulting to a services career ceiling.</p>

<p><strong>What Actually Works:</strong></p>

<ol>
<li>Set a firm exit deadline: 3 years max, 4 years absolute max</li>
<li>Build a portfolio with side projects in modern stack</li>
<li>Practice system design interviews specifically</li>
<li>Network into product companies through events and connections</li>
<li>Accept lateral moves if needed—getting in matters more than getting in at top salary</li>
<li>Consider smaller startups that value hustle over pedigree</li>
</ol>"""
    },

    18: {  # Career Switching - 965 words, need ~300 more  
        "who_should_avoid": """<p><strong>Don't Switch Careers If:</strong></p>

<ul>
<li><strong>You're running from, not running to</strong>: Escape isn't strategy</li>
<li><strong>You haven't tested the new path</strong>: Moonlighting or projects first</li>
<li><strong>You can't survive 3+ years of lower income</strong>: Financial reality check</li>
<li><strong>Your current career can be fixed</strong>: Role change vs. career change</li>
<li><strong>You're romanticizing the new field</strong>: Grass looks greener until you're standing on it</li>
</ul>""",

        "verdict": """<p><strong>The Career Switch Reality:</strong></p>

<p>Career switches after 30 are possible but carry a 4-6 year financial and psychological cost. Some switches make that worthwhile. Many don't. The success stories are survivorship bias; most switchers struggle quietly.</p>

<p><strong>The Uncomfortable Question:</strong></p>

<p>Are you switching because you genuinely want the new career, or because you're avoiding what's broken in your current one? If your current job's problems follow a pattern (toxic manager, burnout, boredom), will switching careers or companies fix that pattern?</p>

<p><strong>What Actually Works:</strong></p>

<ol>
<li>Switch earlier if you're going to switch—25-28 is ideal, 30-32 is doable, 35+ is hard</li>
<li>Test the new career before committing (side projects, freelance, courses)</li>
<li>Build bridge roles—don't leap across chasms</li>
<li>Have 12-18 months of runway saved before making the jump</li>
<li>Accept the seniority reset and the 3-4 year recovery timeline</li>
<li>Network aggressively—hiring switchers requires trust that resumes don't build</li>
</ol>"""
    },

    19: {  # Data Science - 828 words, need ~450 more
        "who_should_avoid": """<p><strong>Data Science Is Wrong For You If:</strong></p>

<ul>
<li><strong>You only want to build ML models</strong>: 70% of the job isn't that</li>
<li><strong>You hate SQL and data cleaning</strong>: That's most of the work</li>
<li><strong>You expect research-style work</strong>: Production constraints rule</li>
<li><strong>You joined because of course hype</strong>: Reality doesn't match marketing</li>
<li><strong>You want clear deliverables</strong>: DS projects are often ambiguous and fail</li>
</ul>

<p><strong>The Data Role Clarification:</strong></p>

<div class="chart-container">
<h4>📊 What Each Data Role Actually Does</h4>
<table class="data-table">
<tr><th>Title</th><th>Reality</th><th>ML Portion</th><th>Salary Trajectory</th></tr>
<tr><td>Data Analyst</td><td>SQL + dashboards + reporting</td><td>0-5%</td><td>Rs 8-28 LPA</td></tr>
<tr><td>Data Scientist</td><td>SQL + analysis + occasional ML</td><td>10-30%</td><td>Rs 12-50 LPA</td></tr>
<tr><td>ML Engineer</td><td>Building + deploying models</td><td>50-70%</td><td>Rs 15-65 LPA</td></tr>
<tr><td>Data Engineer</td><td>Pipelines + infrastructure</td><td>5-10%</td><td>Rs 12-50 LPA</td></tr>
</table>
</div>

<p>If you want ML, target ML Engineering. If you're okay with analytics + occasional ML, Data Scientist works. If you want pure analytics, save yourself the ML courses and own the Data Analyst identity.</p>""",

        "verdict": """<p><strong>The Data Science Truth:</strong></p>

<p>The "Data Science" title covers a wide spectrum of work, most of which isn't machine learning. If you joined expecting research and models, you'll find SQL and dashboards. The mismatch causes disillusionment, but it's not the field's fault—it's expectations vs. reality.</p>

<p><strong>The Uncomfortable Question:</strong></p>

<p>How much of your current role is actual ML vs. data manipulation? If it's 80%+ data work, you're a Data Analyst with an inflated title. Accept that, or actively seek ML Engineering roles at ML-first companies.</p>

<p><strong>What Actually Works:</strong></p>

<ol>
<li>Set realistic expectations—analytics first, ML maybe later</li>
<li>Target companies where ML is the product, not a nice-to-have</li>
<li>Consider ML Engineering if you want to build models professionally</li>
<li>Build independent ML portfolio if your job doesn't provide ML opportunities</li>
<li>Embrace the Data Analyst role if that matches your actual work</li>
<li>Specialize in ML infrastructure (MLOps) for better positioning</li>
</ol>"""
    },

    20: {  # Frontend - 709 words, need ~550 more
        "who_should_avoid": """<p><strong>Frontend Development Is Wrong For You If:</strong></p>

<ul>
<li><strong>You want stable, long-lasting expertise</strong>: Frameworks change every 3 years</li>
<li><strong>You want tech respect at any company</strong>: Frontend is undervalued at many orgs</li>
<li><strong>You dislike visual pixel-perfection</strong>: Matching designs exactly is the job</li>
<li><strong>You want pure engineering work</strong>: Frontend is UX + engineering blend</li>
<li><strong>You want the highest salary ceiling</strong>: Backend/infra pays more long-term</li>
</ul>

<p><strong>The Frontend Career Math:</strong></p>

<div class="chart-container">
<h4>📊 10-Year Financial Projection</h4>
<table class="data-table">
<tr><th>Path</th><th>Year 1</th><th>Year 5</th><th>Year 10</th><th>10-Year Total</th></tr>
<tr><td>Pure Frontend</td><td>Rs 8 LPA</td><td>Rs 22 LPA</td><td>Rs 38 LPA</td><td>Rs 2.3 Cr</td></tr>
<tr><td>Frontend → Full Stack</td><td>Rs 8 LPA</td><td>Rs 26 LPA</td><td>Rs 48 LPA</td><td>Rs 2.8 Cr</td></tr>
<tr><td>Backend Focus</td><td>Rs 9 LPA</td><td>Rs 28 LPA</td><td>Rs 55 LPA</td><td>Rs 3.2 Cr</td></tr>
</table>
</div>

<p>Pure frontend leaves Rs 50-90 lakh on the table over 10 years compared to full-stack or backend tracks.</p>""",

        "verdict": """<p><strong>The Frontend Reality:</strong></p>

<p>Frontend development is valid work, but React expertise has a shelf life. The market demands constant re-learning. The salary ceiling is lower than backend. The perception gap is real even if unfair.</p>

<p><strong>The Uncomfortable Question:</strong></p>

<p>If React disappeared tomorrow, what transferable skills would remain? If your answer is "I'd learn the next thing," you're perpetually at the market's mercy. Build skills that transcend frameworks.</p>

<p><strong>What Actually Works:</strong></p>

<ol>
<li>Build strong JavaScript/TypeScript fundamentals that transfer across frameworks</li>
<li>Add backend or infrastructure skills—full-stack is more valuable than pure frontend</li>
<li>Focus on performance expertise—harder to commoditize</li>
<li>Consider Design Engineering for UX-focused career path</li>
<li>Stay current but don't chase every new framework</li>
<li>Target platform engineering roles (design systems, dev tools) for higher ceiling</li>
</ol>"""
    },

    21: {  # PM - 717 words, need ~550 more
        "who_should_avoid": """<p><strong>Product Management Is Wrong For You If:</strong></p>

<ul>
<li><strong>You want to be "the decider"</strong>: Real authority is rare until senior levels</li>
<li><strong>You hate meetings</strong>: 40-60% of PM time is meetings</li>
<li><strong>You want clear ownership</strong>: PMs own outcomes but not resources</li>
<li><strong>You dislike ambiguity</strong>: PM work is constantly uncertain</li>
<li><strong>You want technical deep work</strong>: PM is breadth, not depth</li>
</ul>

<p><strong>The PM Career Path Reality:</strong></p>

<div class="chart-container">
<h4>📊 PM Career Progression</h4>
<table class="data-table">
<tr><th>Level</th><th>Years Experience</th><th>Actual Role</th><th>Strategy Work %</th></tr>
<tr><td>APM</td><td>0-2</td><td>Ticket writer + coordinator</td><td>5%</td></tr>
<tr><td>PM</td><td>2-5</td><td>Feature owner + stakeholder manager</td><td>15%</td></tr>
<tr><td>Senior PM</td><td>5-8</td><td>Product area owner + some strategy</td><td>30%</td></tr>
<tr><td>Director/GPM</td><td>8-12</td><td>Strategy + team leadership</td><td>50%</td></tr>
<tr><td>VP/CPO</td><td>12+</td><td>Full strategic ownership</td><td>70%+</td></tr>
</table>
</div>

<p>The "CEO of the product" work happens at Director+ level. Before that, you're a very well-paid Jira manager with some user insight.</p>""",

        "verdict": """<p><strong>The PM Truth:</strong></p>

<p>Product Management is real and valuable. But most PM jobs, especially junior to mid-level, are execution and coordination with occasional product thinking. The strategic, visionary PM role that courses sell is rare until you reach Director level at a PM-mature company.</p>

<p><strong>The Uncomfortable Question:</strong></p>

<p>How much of your time this month was strategic thinking vs. backlog grooming and stakeholder updates? If it's 80%+ execution, you're doing the job most PMs do—but not the job the internet sells.</p>

<p><strong>What Actually Works:</strong></p>

<ol>
<li>Accept that Jira management is foundational PM work</li>
<li>Target PM-mature companies where product is genuinely empowered</li>
<li>Build data and technical skills to differentiate from "idea" PMs</li>
<li>Create strategic work if your company doesn't provide it (research, proposals)</li>
<li>Plan for 8-10 years before reaching "real" strategic PM roles</li>
<li>Consider Technical PM, PMM, or Growth as alternative product-adjacent paths</li>
</ol>"""
    },

    22: {  # Agency vs Brand - 515 words, need ~750 more
        "salary_reality": """<p><strong>The Financial Reality Across Marketing Environments:</strong></p>

<div class="chart-container">
<h4>💰 Detailed Salary Comparison</h4>
<table class="data-table">
<tr><th>Experience</th><th>Large Agency</th><th>D2C Brand</th><th>Enterprise</th><th>Tech Company</th></tr>
<tr><td>0-2 years</td><td>Rs 4-7 LPA</td><td>Rs 6-10 LPA</td><td>Rs 7-12 LPA</td><td>Rs 8-14 LPA</td></tr>
<tr><td>2-5 years</td><td>Rs 7-14 LPA</td><td>Rs 12-22 LPA</td><td>Rs 14-25 LPA</td><td>Rs 18-30 LPA</td></tr>
<tr><td>5-8 years</td><td>Rs 14-25 LPA</td><td>Rs 22-38 LPA</td><td>Rs 28-45 LPA</td><td>Rs 35-55 LPA</td></tr>
</table>
</div>

<p><strong>Hourly Reality Check:</strong></p>
<ul>
<li>Agency at Rs 14 LPA / 60 hours/week = Rs 225/hour</li>
<li>D2C at Rs 18 LPA / 50 hours/week = Rs 350/hour</li>
<li>Tech at Rs 25 LPA / 45 hours/week = Rs 535/hour</li>
</ul>

<p>Agency looks worse when normalized for actual hours worked. Tech marketing pays 2.4x agency hourly rate at similar experience levels.</p>""",

        "stuck_point": """<p><strong>Where Marketers Get Trapped:</strong></p>

<p><strong>The Agency Lifestyle Trap:</strong></p>
<p>You love the chaos, multiple clients, creative energy. But by 30, the 60-hour weeks stop being "hustle" and start being exhausting. You want out, but your network is all agency people.</p>

<p><strong>The Brand-Side Bubble:</strong></p>
<p>You've been at one D2C brand for 4 years. Your skills are deep in "our way of doing things." Interview at other companies exposes gaps. Your expertise doesn't transfer cleanly.</p>

<p><strong>Escape Routes That Work:</strong></p>

<ol>
<li><strong>Agency to Brand at Year 3</strong>: Sweet spot for transition—enough experience to be valuable, not so much that lifestyle expectations are too different.</li>

<li><strong>Brand to Tech Marketing</strong>: Tech companies pay more and often have better processes. Worth targeting explicitly.</li>

<li><strong>Product Marketing Path</strong>: More strategic, better paid, clearer career ladder than traditional digital marketing.</li>

<li><strong>Growth Roles</strong>: Growth marketing/growth product blends marketing with product thinking. Rising path with strong demand.</li>

<li><strong>Consulting After 10 Years</strong>: Specialist consultants can charge Rs 5-15K/hour. But requires genuine expertise and reputation.</li>
</ol>""",

        "who_should_avoid": """<p><strong>Agency Side Is Wrong For You If:</strong></p>

<ul>
<li>You need predictable hours for family/health reasons</li>
<li>You prefer depth over breadth</li>
<li>Client management drains you</li>
<li>You want to see long-term impact of your work</li>
<li>High-pressure, fast-turnaround work stresses you</li>
</ul>

<p><strong>Brand Side Is Wrong For You If:</strong></p>

<ul>
<li>You get bored with one industry quickly</li>
<li>You learn best through variety and challenge</li>
<li>You want rapid skill development</li>
<li>You prefer creative intensity to corporate process</li>
<li>Politics and slow decision-making frustrate you</li>
</ul>""",

        "verdict": """<p><strong>The Agency vs Brand Reality:</strong></p>

<p>Neither is universally better. Agency provides fast learning but extracts high lifestyle cost. Brand provides stability but risks narrowing your expertise. The right path depends on your life stage and priorities.</p>

<p><strong>The Optimal Strategy:</strong></p>

<ol>
<li>Start agency for 2-3 years maximum</li>
<li>Move brand-side before burnout hits</li>
<li>Target tech companies for the best of both worlds</li>
<li>Build specialized expertise that transcends environment</li>
<li>Keep agency options open for consulting at senior levels</li>
</ol>"""
    },

    23: {  # American Dream - 573 words, need ~700 more
        "salary_reality": """<p><strong>The Complete US vs India Financial Model:</strong></p>

<div class="chart-container">
<h4>💰 15-Year Wealth Accumulation Model</h4>
<table class="data-table">
<tr><th>Factor</th><th>US Path</th><th>India Path</th></tr>
<tr><td>Starting salary (Year 1)</td><td>$120K</td><td>Rs 25 LPA</td></tr>
<tr><td>Peak salary (Year 15)</td><td>$280K</td><td>Rs 85 LPA</td></tr>
<tr><td>Annual savings rate</td><td>25%</td><td>40%</td></tr>
<tr><td>15-year savings</td><td>~$800K</td><td>~Rs 2.5 Cr (~$310K)</td></tr>
<tr><td>Visa stress</td><td>High</td><td>None</td></tr>
<tr><td>Career flexibility</td><td>Limited</td><td>Full</td></tr>
<tr><td>Family proximity</td><td>Annual visits</td><td>Daily</td></tr>
</table>
</div>

<p>US builds more wealth in absolute dollars. But the gap isn't 5x after costs. And the non-financial factors—family, stress, freedom—don't show up in spreadsheets.</p>""",

        "stuck_point": """<p><strong>Where US-Based Indians Get Trapped:</strong></p>

<p><strong>The Sunk Cost Fallacy:</strong></p>
<p>"I've invested 10 years here. I can't go back now." But sunk costs are sunk. The question is: what's the best path forward from today?</p>

<p><strong>The Return Fear:</strong></p>
<p>"What will people think if I return?" Social pressure keeps people in situations that no longer serve them. The US narrative is internalized deep.</p>

<p><strong>The Decision Framework:</strong></p>

<ol>
<li><strong>If Green Card timeline is 40+ years</strong>: The math has fundamentally changed. India offers comparable wealth with full freedom.</li>

<li><strong>If you have L1A pathway</strong>: This is different—EB-1C can be 2-3 years. Evaluate separately.</li>

<li><strong>If career is suffering due to visa limits</strong>: The inability to switch jobs, start companies, or negotiate freely has a real cost.</li>

<li><strong>If family needs are increasing</strong>: Aging parents, kids wanting to know grandparents—these get harder with distance.</li>

<li><strong>If savings are the goal</strong>: Compare 10-year projection of US savings vs. India savings. The gap may not justify the lifestyle cost.</li>
</ol>""",

        "who_should_avoid": """<p><strong>The US Path Is Wrong For You If:</strong></p>

<ul>
<li>You have elderly parents who need regular care</li>
<li>Family proximity is a core value</li>
<li>You want to start a company someday</li>
<li>Visa uncertainty will cause you chronic anxiety</li>
<li>You're optimizing for freedom, not just dollars</li>
</ul>

<p><strong>The US Path Might Still Work If:</strong></p>

<ul>
<li>You have L1A or other faster immigrant path</li>
<li>You're in a field that truly has no equivalent in India (specialized research)</li>
<li>You've already built a life (spouse, kids school, community)</li>
<li>Your GC is filed before the backlog got extreme</li>
<li>The career opportunity genuinely can't exist in India</li>
</ul>""",

        "verdict": """<p><strong>The American Dream 2024 Reality:</strong></p>

<p>The American Dream made sense when Green Cards took 5 years. At 50+ years wait time for India-born, the calculus has completely changed. India now offers Rs 1 Cr+ salaries at senior levels, full entrepreneurial freedom, family access, and a fraction of the living costs.</p>

<p><strong>The Uncomfortable Question:</strong></p>

<p>If someone offered you $150K/year with no visa and full freedom in India, vs. $200K/year with 50 years of visa anxiety in the US, which is actually the better deal?</p>

<p><strong>What Actually Works:</strong></p>

<ol>
<li>Evaluate the math honestly, including non-financial factors</li>
<li>If GC timeline exceeds 30 years, seriously reconsider</li>
<li>Explore L1A or other accelerated paths if committed to US</li>
<li>Build India connections even while in US (easier return)</li>
<li>Make decision based on your values, not social expectations</li>
</ol>"""
    }
}

print("Adding comprehensive content to thin articles...")
for article_id, updates in full_content.items():
    try:
        article = Article.objects.get(id=article_id)
        for field, content in updates.items():
            setattr(article, field, content)
        article.save()
        
        # Count total words now
        total = sum(count_words(getattr(article, f, '')) for f in 
                   ['common_expectation', 'actual_reality', 'salary_reality', 
                    'stuck_point', 'who_should_avoid', 'verdict'])
        print(f"  ID {article_id}: Now {total} words")
    except Exception as e:
        print(f"  Error with ID {article_id}: {e}")

print("\nBatch 1 fix complete!")
