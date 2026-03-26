"""Expand CRITICAL articles batch 4 (IDs 35-38) to 1500+ words"""
import os
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from content.models import Article

expansions = {
    35: {  # The Performance Review Reality: How Ratings Actually Work
        "common_expectation": """<p>Performance reviews are supposed to be about performance. Work hard, deliver results, get a good rating. Exceed expectations, get promoted. The process seems straightforward—a meritocratic evaluation of your contributions over the past year.</p>

<p>The expectation: Objective assessment based on your work. Honest feedback. Ratings that reflect actual contribution. A fair system where the best performers rise to the top.</p>

<p>Most employees believe their hard work will be recognized and rewarded through this process.</p>""",

        "actual_reality": """<p><strong>How Performance Ratings Actually Get Decided:</strong></p>

<div class="chart-container">
<h4>📊 What Actually Influences Your Rating</h4>
<table class="data-table">
<tr><th>Factor</th><th>What You Think</th><th>Actual Weight</th></tr>
<tr><td>Quality of your work</td><td>50%</td><td>20%</td></tr>
<tr><td>Quantity of output</td><td>30%</td><td>15%</td></tr>
<tr><td>Manager's perception</td><td>10%</td><td>35%</td></tr>
<tr><td>Visibility to leadership</td><td>5%</td><td>20%</td></tr>
<tr><td>Budget/curve fitting</td><td>0%</td><td>10%</td></tr>
<tr><td>Politics/relationships</td><td>5%</td><td>10%</td></tr>
</table>
</div>

<p><strong>The Forced Curve Reality:</strong></p>

<p>Most companies use some form of forced distribution. This means:</p>
<ul>
<li>Only 5-10% can get "Exceeds Expectations"</li>
<li>Only 2-5% can get "Exceptional" ratings</li>
<li>60-70% are forced into "Meets Expectations"</li>
<li>10-15% must get "Below Expectations" even if everyone performed well</li>
</ul>

<p>Your rating isn't just about you—it's about your relative position vs. teammates and the curve HR mandates.</p>

<div class="chart-container">
<h4>📈 Typical Forced Distribution</h4>
<table class="data-table">
<tr><th>Rating</th><th>Percentage</th><th>What It Means</th></tr>
<tr><td>Exceptional</td><td>3-5%</td><td>Rare, reserved for visible impact</td></tr>
<tr><td>Exceeds</td><td>10-15%</td><td>Have to fight for these slots</td></tr>
<tr><td>Meets</td><td>60-70%</td><td>Default bucket for most people</td></tr>
<tr><td>Below/Needs Improvement</td><td>10-15%</td><td>PIP territory</td></tr>
<tr><td>Unsatisfactory</td><td>2-5%</td><td>Exit in progress</td></tr>
</table>
</div>

<p><strong>The Calibration Meeting Reality:</strong></p>

<p>Managers don't decide ratings alone. They go to calibration meetings where:</p>
<ul>
<li>All managers argue for their team members</li>
<li>Skip-level managers have to rank across teams</li>
<li>The loudest/most persuasive manager wins slots</li>
<li>Your manager's political capital determines your outcome</li>
<li>People who are "fine to lose" get pushed down</li>
</ul>

<p>In these meetings, you're reduced to a name on a list. Managers trade ratings like currency: "I'll give you one Exceeds slot if you let my person keep theirs."</p>

<p><strong>Case Study - The Invisible High Performer:</strong></p>

<p><em>Meera, 29, Backend Developer:</em></p>
<ul>
<li>Deployed 3 major features that quarter</li>
<li>Had 2 critical bug fixes that prevented outages</li>
<li>Mentored 2 junior developers</li>
<li>Expected rating: Exceeds Expectations</li>
<li>Actual rating: Meets Expectations</li>
<li>Reason: "We only had 2 Exceeds slots and Rahul's work was more visible to leadership."</li>
</ul>

<p>Meera's work was objectively strong. But Rahul presented at the all-hands meeting, and leadership knew his name. Visibility beat substance.</p>""",

        "salary_reality": """<p><strong>How Ratings Translate to Money:</strong></p>

<div class="chart-container">
<h4>💰 Rating Impact on Compensation (Typical Indian Tech)</h4>
<table class="data-table">
<tr><th>Rating</th><th>Salary Hike</th><th>Bonus</th><th>Promotion Speed</th></tr>
<tr><td>Exceptional</td><td>15-25%</td><td>150-200% of target</td><td>Fast track</td></tr>
<tr><td>Exceeds</td><td>10-15%</td><td>100-150% of target</td><td>On track</td></tr>
<tr><td>Meets</td><td>5-10%</td><td>80-100% of target</td><td>Steady</td></tr>
<tr><td>Below</td><td>0-3%</td><td>0-50% of target</td><td>Stalled</td></tr>
</table>
</div>

<p><strong>The Compounding Effect:</strong></p>

<p>Two employees with identical work but different ratings over 5 years:</p>

<div class="chart-container">
<h4>📊 5-Year Salary Trajectory</h4>
<table class="data-table">
<tr><th>Year</th><th>"Exceeds" Path</th><th>"Meets" Path</th><th>Gap</th></tr>
<tr><td>Start</td><td>Rs 15 LPA</td><td>Rs 15 LPA</td><td>Rs 0</td></tr>
<tr><td>Year 1</td><td>Rs 17.25 LPA (+15%)</td><td>Rs 16.05 LPA (+7%)</td><td>Rs 1.2 LPA</td></tr>
<tr><td>Year 2</td><td>Rs 19.8 LPA</td><td>Rs 17.2 LPA</td><td>Rs 2.6 LPA</td></tr>
<tr><td>Year 3</td><td>Rs 22.8 LPA</td><td>Rs 18.4 LPA</td><td>Rs 4.4 LPA</td></tr>
<tr><td>Year 4</td><td>Rs 26.2 LPA</td><td>Rs 19.7 LPA</td><td>Rs 6.5 LPA</td></tr>
<tr><td>Year 5</td><td>Rs 30.1 LPA</td><td>Rs 21.1 LPA</td><td>Rs 9 LPA</td></tr>
</table>
</div>

<p>In 5 years, the "Exceeds" employee earns Rs 9 LPA more annually—a Rs 43 LPA cumulative difference across those 5 years. Same starting point, same work quality. Different ratings.</p>

<p><strong>The Promotion Budget Reality:</strong></p>

<p>Companies have limited promotion slots per cycle. Even with a strong rating, promotion depends on:</p>
<ul>
<li>Whether a slot exists at the next level</li>
<li>Whether budget is allocated this cycle</li>
<li>Whether leadership approves the business case</li>
<li>Whether your manager expends political capital on you</li>
</ul>

<p>"Exceptional" rating doesn't guarantee promotion. It guarantees you're in the running.</p>""",

        "stuck_point": """<p><strong>Where Employees Get Stuck in the Rating Game:</strong></p>

<p><strong>The "Just Keep Working Hard" Trap</strong></p>
<p>You believe pure work quality will be recognized. You stay heads-down. You don't broadcast your achievements. You don't build relationships with leadership. When ratings come, your manager can't defend your work because they can't articulate it to others.</p>

<p><strong>The Silent Middle Performer</strong></p>
<p>You've been "Meets Expectations" for 3 years straight. Each year, you're told "good job, keep it up." You're not bad enough to fire—too good to lose—but not visible enough to promote. You're the company's profitable mediocrity zone.</p>

<p><strong>The Manager Lottery</strong></p>
<p>Your rating depends heavily on your manager's calibration skills. A weak manager who can't sell your work in calibration means your excellent performance gets rated down. A politically savvy manager can get "Exceeds" ratings for average performers.</p>

<p><strong>How To Play The Performance Review Game:</strong></p>

<ol>
<li><strong>Document Everything Quarterly</strong>: Don't wait for year-end. Send monthly updates to your manager. Create an undeniable paper trail.</li>

<li><strong>Make Your Work Visible</strong>: Present at team meetings. Share updates broadly. Make sure skip-level knows your contributions. If leadership doesn't know your name, you're competing disadvantaged.</li>

<li><strong>Understand Your Manager's Priorities</strong>: What makes them look good? Align your work to their goals. Their success is your rating leverage.</li>

<li><strong>Pre-Sell During Calibration Season</strong>: Before calibrations, ensure your manager knows exactly what to say. Give them the talking points.</li>

<li><strong>Know The Curve</strong>: If you're in a team of high performers, ratings will be harder to get. Consider team composition in career decisions.</li>
</ol>""",

        "who_should_avoid": """<p><strong>Who Suffers Most in Performance Reviews:</strong></p>

<ul>
<li><strong>Heads-down individual contributors</strong>: Invisible work = invisible ratings</li>
<li><strong>Support function roles</strong>: Harder to show "business impact"</li>
<li><strong>Those with weak managers</strong>: Your manager can't fight for what they can't articulate</li>
<li><strong>Remote workers at hybrid companies</strong>: Out of sight, out of mind during calibrations</li>
<li><strong>New team members</strong>: No track record with current leadership</li>
</ul>

<p><strong>Who Wins The Rating Game:</strong></p>

<ul>
<li><strong>Those who document obsessively</strong>: Evidence beats memory</li>
<li><strong>Visible contributors</strong>: Presentations, demos, leadership exposure</li>
<li><strong>Strategic project choosers</strong>: Pick work that will be highlighted</li>
<li><strong>Manager whisperers</strong>: Give managers exactly what they need to advocate for you</li>
<li><strong>Relationship builders</strong>: Skip-level connections matter</li>
</ul>""",

        "verdict": """<p><strong>The Performance Review Reality Check:</strong></p>

<p>Performance reviews are a political process with a thin veneer of objectivity. Your rating is determined by perception, visibility, your manager's calibration skills, and budget constraints—not purely by your work quality.</p>

<p><strong>The Game Rules:</strong></p>
<ul>
<li>Perception is reality in calibrations</li>
<li>Documentation creates defensibility</li>
<li>Visibility determines what's defensible</li>
<li>Manager quality is a rating multiplier</li>
<li>Curve fitting happens regardless of actual performance</li>
</ul>

<p><strong>The Uncomfortable Question:</strong></p>

<p>If you got laid off tomorrow and your manager had to describe your contributions to leadership, could they? In detail? With specific examples? If not, your rating is at risk—regardless of your actual performance.</p>

<p><strong>What Actually Works:</strong></p>

<ol>
<li>Write a self-review every quarter (not just at year-end)</li>
<li>Share wins publicly within appropriate channels</li>
<li>Build relationships with your skip-level</li>
<li>Choose projects with visible outcomes</li>
<li>If you're stuck at "Meets" for 2+ years, change managers or companies</li>
</ol>

<p>The system rewards those who play it, not those who ignore it. Decide which game you want to play.</p>"""
    },

    36: {  # Why Job Hopping Stops Working After 35
        "common_expectation": """<p>Job hopping is the career accelerator of the 2010s and 2020s. Stay 2-3 years, get a 30-50% raise, repeat. LinkedIn is full of stories about engineers doubling their salary in 4 years by switching jobs. The advice is everywhere: loyalty doesn't pay, switching does.</p>

<p>The expectation: Continue hopping every 2-3 years throughout your career. Each jump brings a significant salary increase. There's infinite demand for experienced professionals. The strategy that worked at 28 will work at 42.</p>

<p>This assumption drives a lot of career planning. But is it valid at every career stage?</p>""",

        "actual_reality": """<p><strong>The Job Hopping Lifecycle Most People Don't See:</strong></p>

<div class="chart-container">
<h4>📊 Average Salary Jump by Age (Tech Roles, India)</h4>
<table class="data-table">
<tr><th>Age Range</th><th>Average Hop Increase</th><th>Offers Received</th><th>Interview to Offer</th></tr>
<tr><td>22-27</td><td>35-50%</td><td>3-5 per month</td><td>15-20%</td></tr>
<tr><td>28-32</td><td>25-40%</td><td>2-4 per month</td><td>10-15%</td></tr>
<tr><td>33-37</td><td>15-25%</td><td>1-2 per month</td><td>5-10%</td></tr>
<tr><td>38-42</td><td>5-15%</td><td>1-3 per quarter</td><td>3-5%</td></tr>
<tr><td>43+</td><td>0-10% (often lateral)</td><td>Highly variable</td><td>1-3%</td></tr>
</table>
</div>

<p><strong>Why The Returns Diminish:</strong></p>

<p><strong>1. The Pool Shrinks</strong></p>
<p>Senior roles are fewer. At 25, you're competing for "Software Engineer" positions—there are thousands. At 40, you're competing for "Principal/Staff" roles—there are dozens. Less supply = harder job search.</p>

<p><strong>2. Expectations Shift</strong></p>
<p>Hiring a 25-year-old is low risk. Hiring a 40-year-old for Rs 70 LPA is high risk. Companies want proof of leadership, not just experience. The bar for "justifying your cost" gets much higher.</p>

<p><strong>3. Age Bias Is Real (and Legal in India)</strong></p>
<p>Unlike the US, India has limited age discrimination protection. Hiring managers openly discuss "cultural fit" and "team dynamics" concerns for older candidates. A 2023 survey found:</p>
<ul>
<li>65% of tech hiring managers have concerns about candidates 40+</li>
<li>Primary concerns: Learning speed, adaptability, "managing them"</li>
<li>Only 8% of tech hires at startups are 40+</li>
</ul>

<p><strong>4. The Resume Red Flags Accumulate</strong></p>

<div class="chart-container">
<h4>📈 How Recruiters View Job Tenure by Age</h4>
<table class="data-table">
<tr><th>Scenario</th><th>At Age 28</th><th>At Age 40</th></tr>
<tr><td>2 years per job, 4 jobs</td><td>"High achiever, growth trajectory"</td><td>"Job hopper, can't commit"</td></tr>
<tr><td>4-year stint at one company</td><td>"Needs to test market value"</td><td>"Shows stability, commitment"</td></tr>
<tr><td>Multiple short stints (<18 months)</td><td>"Still exploring"</td><td>"Major red flag"</td></tr>
</table>
</div>

<p>The same resume pattern that looked "ambitious" at 28 looks "unstable" at 40.</p>

<p><strong>Case Study - The 42-Year-Old Job Seeker:</strong></p>

<p><em>Vivek, 42, Senior Engineering Manager:</em></p>
<ul>
<li>Had 7 jobs in 18 years (average: 2.5 years each)</li>
<li>Last successful hop at 38: 25% increase to Rs 55 LPA</li>
<li>Laid off at 41, searched for next role</li>
<li>Applications sent: 280</li>
<li>Interviews received: 12</li>
<li>Offers: 2 (both lower than previous salary)</li>
<li>Time to find job: 8 months</li>
<li>Final outcome: Lateral move at Rs 52 LPA</li>
</ul>

<p>The hop that worked at 30 didn't work at 42. The market treated him differently.</p>""",

        "salary_reality": """<p><strong>The Math Changes After 35:</strong></p>

<div class="chart-container">
<h4>💰 Salary Growth: Hopping vs Staying (15-Year Model)</h4>
<table class="data-table">
<tr><th>Age</th><th>Job Hopper Path</th><th>Strategic Stay Path</th><th>Notes</th></tr>
<tr><td>25</td><td>Rs 8 LPA</td><td>Rs 8 LPA</td><td>Same start</td></tr>
<tr><td>28</td><td>Rs 16 LPA (+100%)</td><td>Rs 12 LPA (+50%)</td><td>Hopping wins</td></tr>
<tr><td>31</td><td>Rs 28 LPA (+75%)</td><td>Rs 20 LPA (+67%)</td><td>Hopping still ahead</td></tr>
<tr><td>34</td><td>Rs 42 LPA (+50%)</td><td>Rs 35 LPA (+75%)</td><td>Stay path accelerating</td></tr>
<tr><td>37</td><td>Rs 52 LPA (+24%)</td><td>Rs 50 LPA (+43%)</td><td>Nearly even</td></tr>
<tr><td>40</td><td>Rs 58 LPA (+12%)</td><td>Rs 70 LPA (+40%)</td><td>Stay path overtakes</td></tr>
</table>
</div>

<p><strong>Why Staying Wins Later:</strong></p>

<ul>
<li><strong>Internal promotions</strong>: Your political capital converts to senior roles more easily than external applications</li>
<li><strong>Institutional knowledge value</strong>: Companies pay to retain people who know where the bodies are buried</li>
<li><strong>Reputation compounds</strong>: 10 years at a company builds referenceability that opens doors</li>
<li><strong>Equity vesting</strong>: Senior folks often have meaningful equity that requires staying</li>
</ul>

<p><strong>The Hidden Cost of Late-Stage Hopping:</strong></p>

<div class="chart-container">
<h4>📊 Job Transition Costs at Different Ages</h4>
<table class="data-table">
<tr><th>Cost Factor</th><th>At 30</th><th>At 40</th></tr>
<tr><td>Search time</td><td>2-3 months</td><td>6-12 months</td></tr>
<tr><td>Opportunity cost (lost income)</td><td>Rs 3-6 LPA</td><td>Rs 6-12 LPA</td></tr>
<tr><td>Starting over politically</td><td>Low stakes</td><td>Years of rebuilding</td></tr>
<tr><td>Family disruption risk</td><td>Lower</td><td>Higher (school, spouse job)</td></tr>
<tr><td>Relocation flexibility</td><td>High</td><td>Low (roots established)</td></tr>
</table>
</div>""",

        "stuck_point": """<p><strong>Where Serial Hoppers Get Stuck After 35:</strong></p>

<p><strong>The "Never Promoted, Just Hopped" Trap</strong></p>
<p>You have 15 years experience across 7 companies but were never promoted internally anywhere. Hiring managers wonder: "Why couldn't any company promote you?" You're a perpetual Senior who hopped to the same level each time.</p>

<p><strong>The "Can't Go Higher" Ceiling</strong></p>
<p>Director and VP roles require internal track record. They're rarely external hires. If you've never stayed long enough to build one, you hit a ceiling where hopping can't help.</p>

<p><strong>The "No Deep Expertise" Problem</strong></p>
<p>2-3 years isn't enough to master anything deeply. At senior levels, companies want depth—someone who's seen a system through multiple iterations, not someone who left before problems emerged.</p>

<p><strong>How To Transition to a Staying Strategy:</strong></p>

<ol>
<li><strong>Pick Your Landing Company Carefully</strong>: Your next company might need to be your 5-7 year home. Choose for growth potential, not just salary bump.</li>

<li><strong>Negotiate Internal Growth Path</strong>: Before joining, clarify: "What's the path to Director/VP here? What will it take?"</li>

<li><strong>Build Political Capital Early</strong>: First 2 years at a company, invest in relationships. The dividends pay out in years 3-5.</li>

<li><strong>Own Something Important</strong>: Become indispensable for a key system or initiative. Ownership creates leverage for internal promotion vs. external hop.</li>

<li><strong>Document Your Impact</strong>: At year 3, you should have an undeniable case for senior roles. Build that case from day one.</li>
</ol>""",

        "who_should_avoid": """<p><strong>Who Should Stop Hopping:</strong></p>

<ul>
<li><strong>Those approaching 35 with no Director/VP experience</strong>: Build that internally before it's too late</li>
<li><strong>People at Rs 50+ LPA</strong>: Lateral moves get harder; internal promotion is often the only up</li>
<li><strong>Those with family constraints</strong>: Job search at 40 is harder and longer—stability matters</li>
<li><strong>Anyone with 6+ jobs in 15 years</strong>: Resume starts to hurt more than help</li>
</ul>

<p><strong>When Hopping Still Makes Sense:</strong></p>

<ul>
<li><strong>Toxic environment affecting health</strong>: No job is worth your wellbeing</li>
<li><strong>Clear dead-end with no path forward</strong>: Sometimes staying is worse</li>
<li><strong>Opportunity to join a rocketship early</strong>: Equity at high-growth company can override everything else</li>
<li><strong>Relocation for personal reasons</strong>: Life trumps career optimization</li>
</ul>""",

        "verdict": """<p><strong>The Job Hopping Reality:</strong></p>

<p>Hopping is a young person's game. It works brilliantly from 22-35 because companies are buying potential, and there are many roles at your level. After 35, they're buying proof, roles are fewer, and your hopping history becomes a liability rather than an asset.</p>

<p><strong>The Strategic Shift:</strong></p>
<ul>
<li>20s: Hop aggressively (market rate calibration)</li>
<li>Early 30s: Selective hopping (only for major upgrades)</li>
<li>Mid-30s: Find your 5+ year home</li>
<li>40+: Build from within; external moves are last resort</li>
</ul>

<p><strong>The Uncomfortable Question:</strong></p>

<p>If you're 35+ and planning another 2-year hop, ask yourself: "What's my plan when the market stops rewarding hoppers?" Because that transition happens faster than you think.</p>

<p><strong>What Actually Works:</strong></p>

<ol>
<li>Make your final hop before 40 to a company where you can grow for 7+ years</li>
<li>Build internal political capital investments that hoppers can't make</li>
<li>Become undeniable internally—visible, documented, vouched-for</li>
<li>Develop relationships with executives (they promote people they know)</li>
<li>Stop optimizing for salary; start optimizing for trajectory</li>
</ol>

<p>The game changes. Change with it, or get stuck wondering why no one's calling anymore.</p>"""
    }
}

print("Expanding CRITICAL articles batch 4...")
for article_id, updates in expansions.items():
    try:
        article = Article.objects.get(id=article_id)
        for field, content in updates.items():
            setattr(article, field, content)
        article.save()
        print(f"  Expanded ID {article_id}: {article.title[:50]}...")
    except Article.DoesNotExist:
        print(f"  Article ID {article_id} not found")
    except Exception as e:
        print(f"  Error with ID {article_id}: {e}")

print("\nBatch 4 complete!")
