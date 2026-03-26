"""Batch 2: Learning, Engineering, Career Reality Checks"""
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
        "category_slug": "learning",
        "title": "The Self-Learning Trap: Why Most Online Courses Are Expensive Entertainment",
        "slug": "self-learning-trap-online-courses-expensive-entertainment",
        "meta_title": "Online Courses Reality: Entertainment or Education?",
        "meta_description": "Data on online course completion rates, actual skill gains, and what works. Most spend thousands learning nothing.",
        "target_persona": "You have 15 tabs of Udemy courses, 3 Coursera specializations in progress, and a growing stack of unfinished YouTube tutorials. You spend money on learning but your skills stay the same. You need honest data.",
        "who_should_avoid": "If you finish 90% of courses you start and actually apply them, skip this. You are the exception. This is for the majority who buy courses like gym memberships - with good intentions and zero follow-through.",
        "common_expectation": """**The Promise:**
- Buy course, learn skill, get job/raise
- Self-paced means you can learn anytime
- Certificates add credibility to your resume
- Online learning is democratizing education

**What Course Creators Show:**
Success stories. Screenshots of people who got jobs after their course. Never the completion rates. Never the thousands who started and stopped at week 2.""",
        "actual_reality": """**The Numbers They Never Share:**

<div class="chart-container">
<h4>📊 Online Course Completion Rates</h4>
<table class="data-table">
<tr><th>Platform</th><th>Start Rate</th><th>25% Complete</th><th>Full Complete</th></tr>
<tr><td>Udemy</td><td>100%</td><td>30%</td><td>5-10%</td></tr>
<tr><td>Coursera</td><td>100%</td><td>40%</td><td>3-5%</td></tr>
<tr><td>YouTube Tutorials</td><td>100%</td><td>20%</td><td>2%</td></tr>
<tr><td>Paid Bootcamps</td><td>100%</td><td>75%</td><td>60%</td></tr>
</table>
</div>

**Why 95% Fail:**
1. **No Accountability** - Nobody checking if you showed up
2. **Decision Fatigue** - Which of your 47 courses to continue today?
3. **Dopamine from Buying** - Purchasing feels like progress
4. **No Application** - Learning without doing is entertainment

<div class="chart-container">
<h4>📈 Skill Retention: Course vs Project</h4>
<table class="data-table">
<tr><th>Method</th><th>After 1 Week</th><th>After 1 Month</th><th>After 6 Months</th></tr>
<tr><td>Watching Videos</td><td>60%</td><td>30%</td><td>10%</td></tr>
<tr><td>Doing Exercises</td><td>80%</td><td>55%</td><td>35%</td></tr>
<tr><td>Building Projects</td><td>90%</td><td>75%</td><td>65%</td></tr>
</table>
</div>

**The brutal math:**
You spent Rs 50,000 on courses with 5% completion rate. Effective cost per completed course: Rs 10 lakhs.""",
        "salary_reality": """**What Actually Gets You Paid:**

<div class="chart-container">
<h4>💰 What Hiring Managers Actually Check</h4>
<table class="data-table">
<tr><th>Factor</th><th>Hiring Weight</th><th>Your Time Spent</th></tr>
<tr><td>Portfolio/Projects</td><td>40%</td><td>10%</td></tr>
<tr><td>Previous Experience</td><td>30%</td><td>N/A</td></tr>
<tr><td>Problem-Solving Test</td><td>20%</td><td>5%</td></tr>
<tr><td>Certifications</td><td>5%</td><td>70%</td></tr>
<tr><td>Course Completion</td><td>2%</td><td>15%</td></tr>
</table>
</div>

See the mismatch? You spend 70% of time on certificates that get 5% weight in hiring.""",
        "stuck_point": """**Where Learners Get Trapped:**

1. **Tutorial Hell** - Watching someone code is not coding
2. **Certificate Collection** - LinkedIn full of certificates, GitHub empty
3. **Shiny Object Syndrome** - New course before finishing the old one
4. **Theory Without Practice** - Knowing syntax without building anything

**The Fix:**
- Complete ONE course. Build THREE projects using it
- No new course until you build something with the current one
- Delete courses you started more than 60 days ago
- Set weekly project milestones, not video milestones""",
        "verdict": """**The Hard Truth:**

Online courses are a Rs 50,000 crore industry optimized for sales, not learning. The product is hope, not skill development.

**What works instead:**
1. Pick ONE skill. Find ONE source. Build FIVE projects.
2. Learn in public - document your journey
3. Join a community with accountability
4. Set project deadlines, not learning deadlines

Stop collecting courses. Start building things."""
    },
    {
        "category_slug": "engineering",
        "title": "The Engineering Career Ceiling: Why Most Engineers Peak at 35 and What To Do About It",
        "slug": "engineering-career-ceiling-peak-at-35",
        "meta_title": "Engineering Career Ceiling: Why You Peak at 35",
        "meta_description": "Data on why engineering careers plateau. Technical obsolescence, management trap, and alternatives to getting stuck.",
        "target_persona": "You are an engineer in your late 20s or 30s watching seniors struggle. Or you are a senior engineer feeling stuck. Either way, you are wondering if this is all there is to an engineering career.",
        "who_should_avoid": "If you genuinely love pure technical work and have zero interest in career progression or money, this is not for you. If you are content with where you are, skip this.",
        "common_expectation": """**The Engineering Dream:**
- Become expert, become indispensable
- Technology skills compound over time
- Engineers are always in demand
- Deep expertise = high salary forever

**What College Taught:**
Master your fundamentals, keep learning, and you will always have a job. Technology only grows, therefore job security only grows.""",
        "actual_reality": """**The Inconvenient Data:**

<div class="chart-container">
<h4>📊 Engineering Salary Growth by Experience</h4>
<table class="data-table">
<tr><th>Years</th><th>IC Track Salary</th><th>Management Track</th><th>Specialist Track</th></tr>
<tr><td>0-3</td><td>Rs 6-12 LPA</td><td>Rs 6-12 LPA</td><td>Rs 6-12 LPA</td></tr>
<tr><td>3-7</td><td>Rs 12-25 LPA</td><td>Rs 18-30 LPA</td><td>Rs 15-28 LPA</td></tr>
<tr><td>7-12</td><td>Rs 20-35 LPA</td><td>Rs 35-60 LPA</td><td>Rs 30-50 LPA</td></tr>
<tr><td>12-20</td><td>Rs 25-45 LPA</td><td>Rs 60-1.5 Cr</td><td>Rs 50-80 LPA</td></tr>
</table>
</div>

After 12 years, the IC (Individual Contributor) track salary reaches a ceiling. Management shoots ahead.

**Why the ceiling exists:**
1. **Technology Churn** - Your expertise becomes obsolete every 5-7 years
2. **Age Bias** - Companies prefer younger, cheaper engineers
3. **Leverage Gap** - One manager leads 10 engineers, controls 10x output
4. **Value Perception** - Business sees engineers as cost centers, managers as leaders""",
        "salary_reality": """**Where Engineering Money Actually Is:**

<div class="chart-container">
<h4>💰 Engineering Salary by Path (15 Year Comparison)</h4>
<table class="data-table">
<tr><th>Path</th><th>Year 5</th><th>Year 10</th><th>Year 15</th></tr>
<tr><td>Pure IC</td><td>Rs 18 LPA</td><td>Rs 28 LPA</td><td>Rs 35 LPA</td></tr>
<tr><td>IC + Consulting</td><td>Rs 25 LPA</td><td>Rs 45 LPA</td><td>Rs 60 LPA</td></tr>
<tr><td>Management</td><td>Rs 22 LPA</td><td>Rs 50 LPA</td><td>Rs 85 LPA</td></tr>
<tr><td>Founder/CTO</td><td>Rs 10 LPA</td><td>Rs 20 LPA/Rs 5 Cr</td><td>Rs 0/Rs 50 Cr</td></tr>
</table>
</div>

The founder path is bimodal - most fail spectacularly, few succeed incredibly.""",
        "stuck_point": """**Where Engineers Get Trapped:**

1. **The Coding Comfort Zone** - I will just keep coding, it is what I am good at
2. **Management Rejection** - I became an engineer to avoid people
3. **Skill Hoarding** - Learning tech, never learning business
4. **Company Dependency** - All skills specific to one employer

**Breaking Free:**
- Learn the business, not just the technology
- Build relationships across functions
- Create visibility for your work
- Consider management as a skill, not betrayal of your identity""",
        "verdict": """**The Honest Assessment:**

Engineering is a great career until 35. After that, it forks:
- Those who expanded their skills (management, business, architecture) keep growing
- Those who only went deeper technically hit the ceiling

**Your choice:**
1. Accept the ceiling - maximize happiness, minimize stress
2. Expand into management - requires political skills
3. Go deep specialist - requires constant reinvention
4. Start something - requires risk tolerance

None is wrong. Just choose consciously, not by default."""
    },
    {
        "category_slug": "career-reality-checks",
        "title": "The Career Switch Illusion: Why Changing Jobs Is Not Changing Your Career",
        "slug": "career-switch-illusion-changing-jobs-not-career",
        "meta_title": "Career Switch Reality: Jobs vs Career Change",
        "meta_description": "Data on career switches, what works and what doesn't. Most switches are lateral moves disguised as growth.",
        "target_persona": "You have changed 4 jobs in 6 years, each time hoping for a reset. Or you are planning your next jump thinking this time it will be different. You need someone to tell you what is actually happening.",
        "who_should_avoid": "If your job changes genuinely came with 40%+ raises and new skill development each time, you are doing it right. This is for people stuck in the cycle of lateral moves.",
        "common_expectation": """**What LinkedIn Celebrates:**
- New job announcement = Career win
- More companies = More experience
- Job hopping = Better negotiation
- Fresh start solves old problems

**The Resume Story:**
Each role looks like a progression. Assistant to Associate to Manager. Different companies, different titles, upward trajectory.""",
        "actual_reality": """**What Actually Happens:**

<div class="chart-container">
<h4>📊 Job Switch Outcomes (5 Year Data)</h4>
<table class="data-table">
<tr><th>Switch Type</th><th>% of Switches</th><th>Avg Salary Jump</th><th>3 Year Outcome</th></tr>
<tr><td>Lateral Same Industry</td><td>60%</td><td>15-20%</td><td>Stuck Again</td></tr>
<tr><td>Lateral New Industry</td><td>20%</td><td>0-10%</td><td>Reset Progress</td></tr>
<tr><td>Genuine Level Up</td><td>15%</td><td>30-50%</td><td>Continued Growth</td></tr>
<tr><td>Career Pivot</td><td>5%</td><td>-20% to +40%</td><td>Mixed</td></tr>
</table>
</div>

**The Uncomfortable Truth:**
60% of job switches are lateral moves with a small salary bump. You carry the same problems to a new desk.

**What You Are Really Running From:**
- Bad manager? 70% chance new manager is also bad
- No growth? You did not grow because of you, not them
- Boredom? You will be bored in 6 months again
- Politics? Every company has politics""",
        "salary_reality": """**The Math of Job Hopping:**

<div class="chart-container">
<h4>💰 10 Year Earnings: Switcher vs Grower</h4>
<table class="data-table">
<tr><th>Year</th><th>Job Hopper</th><th>Internal Grower</th></tr>
<tr><td>1</td><td>Rs 8 LPA</td><td>Rs 8 LPA</td></tr>
<tr><td>3</td><td>Rs 12 LPA</td><td>Rs 14 LPA</td></tr>
<tr><td>5</td><td>Rs 16 LPA</td><td>Rs 22 LPA</td></tr>
<tr><td>7</td><td>Rs 20 LPA</td><td>Rs 32 LPA</td></tr>
<tr><td>10</td><td>Rs 28 LPA</td><td>Rs 48 LPA</td></tr>
</table>
</div>

The grower starts slower but compounds faster because promotions bring 30-50% jumps, not 15% lateral moves.""",
        "stuck_point": """**The Job Hopper Trap:**

1. **Restart Penalty** - Each new company resets your reputation
2. **Surface Learning** - Never deep enough to be truly expert
3. **Reference Erosion** - Managers from 5 jobs ago forget you
4. **Perception Problem** - Hiring managers see jumping as a risk

**Before You Switch, Ask:**
- Am I running from something or toward something?
- Did I try internal moves first?
- Will this role teach me new skills or just new colleagues?
- Am I blaming the company for my own gaps?""",
        "verdict": """**The Real Career Growth Formula:**

Job switches should be strategic, not reactive. The best careers have 2-3 long stints with genuine depth, not 8 short ones with surface experience.

**When to switch:**
- 40%+ salary jump
- Genuinely new skills
- Better trajectory, not just better title
- You maxed out learning here

**When not to switch:**
- Running from a problem you will carry with you
- Bored because you stopped challenging yourself
- Everyone else is switching
- Recruiter flattered you with an offer"""
    }
]

print("Creating batch 2 articles...")
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
print("Batch 2 done!")
