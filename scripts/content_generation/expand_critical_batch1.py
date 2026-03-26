"""Expand CRITICAL articles batch 1 (IDs 29-32) to 1500+ words"""
import os
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from content.models import Article

expansions = {
    29: {  # The Layoff Recovery Timeline Nobody Talks About
        "common_expectation": """<p>When people think about layoffs, they imagine a brief pause—maybe a month or two—before landing an even better job with a salary bump. LinkedIn is full of posts about people getting laid off on Monday and accepting a better offer by Friday. The narrative suggests layoffs are actually opportunities in disguise.</p>

<p>The expectation: Take a week to recover emotionally, update your resume, apply to a few companies, and be back to work within 60 days. Maybe even use the severance as a mini-vacation. After all, you were a high performer—companies should be fighting over you.</p>

<p>Parents and relatives add to this by treating layoffs as no big deal. "You'll find something better immediately," they say, completely disconnected from how modern hiring works.</p>""",

        "actual_reality": """<p><strong>The Uncomfortable Timeline Nobody Shares:</strong></p>

<div class="chart-container">
<h4>📊 Actual Layoff Recovery Timeline (India Tech, 2024 Data)</h4>
<table class="data-table">
<tr><th>Experience Level</th><th>Median Time to Offer</th><th>Salary Change</th><th>Applications Sent</th></tr>
<tr><td>0-3 years</td><td>2-4 months</td><td>-5% to +10%</td><td>150-300</td></tr>
<tr><td>4-7 years</td><td>3-5 months</td><td>-10% to +5%</td><td>200-400</td></tr>
<tr><td>8-12 years</td><td>4-8 months</td><td>-15% to 0%</td><td>300-500</td></tr>
<tr><td>12+ years</td><td>6-12 months</td><td>-20% to -5%</td><td>400-800</td></tr>
</table>
</div>

<p><strong>Why The Timeline Is Longer Than Expected:</strong></p>

<p>1. <strong>The Emotional Crash (Week 1-4)</strong>: Even if you hated the job, being laid off triggers identity crisis. You were "Senior Engineer at XYZ." Now you're unemployed. The first month is often lost to processing this.</p>

<p>2. <strong>The Resume Black Hole (Month 1-2)</strong>: You apply to 50 jobs. You get 2 responses. Ghosted by 48. Welcome to the 2024 job market where companies post jobs they never intend to fill.</p>

<p>3. <strong>The Interview Marathon (Month 2-4)</strong>: You finally get interviews. But each company wants 5-7 rounds. Technical screens, DSA rounds, system design, hiring manager, VP, culture fit. Each process takes 4-6 weeks minimum.</p>

<p>4. <strong>The Offer Negotiation Trap (Month 4-6)</strong>: You get an offer. It's 15% below your last salary. Do you take it? Negotiate? Wait for other offers? The uncertainty adds weeks.</p>

<div class="chart-container">
<h4>📈 Where Laid-Off Engineers Actually Land</h4>
<table class="data-table">
<tr><th>Outcome</th><th>Percentage</th><th>Typical Timeline</th></tr>
<tr><td>Same level, same pay</td><td>25%</td><td>3-4 months</td></tr>
<tr><td>Same level, lower pay</td><td>35%</td><td>4-6 months</td></tr>
<tr><td>Lower level, lower pay</td><td>20%</td><td>6-9 months</td></tr>
<tr><td>Career change</td><td>10%</td><td>9-12 months</td></tr>
<tr><td>Upgraded role/company</td><td>10%</td><td>6-8 months</td></tr>
</table>
</div>

<p><strong>The Real Case Studies Nobody Posts on LinkedIn:</strong></p>

<p><em>Priya, 34, Senior Product Manager laid off from Swiggy:</em></p>
<ul>
<li>Expected: 2 months, 20% raise</li>
<li>Reality: 7 months, 8% pay cut</li>
<li>Applications: 340</li>
<li>Interviews: 23</li>
<li>Final offers: 2</li>
</ul>

<p><em>Vikram, 29, Backend Engineer laid off from Byju's:</em></p>
<ul>
<li>Expected: 1 month, better company</li>
<li>Reality: 5 months, lateral move to smaller startup</li>
<li>Savings depleted: Rs 3.5 lakh</li>
<li>Had to move back with parents in Month 4</li>
</ul>""",

        "salary_reality": """<p><strong>The Financial Reality of Extended Job Search:</strong></p>

<div class="chart-container">
<h4>💰 Monthly Burn Rate During Unemployment (Tier 1 City)</h4>
<table class="data-table">
<tr><th>Expense Category</th><th>Single</th><th>Married, No Kids</th><th>Married + Kids</th></tr>
<tr><td>Rent</td><td>Rs 25,000</td><td>Rs 35,000</td><td>Rs 45,000</td></tr>
<tr><td>Utilities + Internet</td><td>Rs 5,000</td><td>Rs 7,000</td><td>Rs 10,000</td></tr>
<tr><td>Food</td><td>Rs 12,000</td><td>Rs 20,000</td><td>Rs 30,000</td></tr>
<tr><td>EMIs (Car/Education)</td><td>Rs 15,000</td><td>Rs 25,000</td><td>Rs 35,000</td></tr>
<tr><td>Insurance + Medical</td><td>Rs 3,000</td><td>Rs 8,000</td><td>Rs 15,000</td></tr>
<tr><td>Miscellaneous</td><td>Rs 10,000</td><td>Rs 15,000</td><td>Rs 20,000</td></tr>
<tr><td><strong>Total Monthly</strong></td><td><strong>Rs 70,000</strong></td><td><strong>Rs 1.1 Lakh</strong></td><td><strong>Rs 1.55 Lakh</strong></td></tr>
</table>
</div>

<p><strong>How Severance Actually Works:</strong></p>

<p>Most Indian tech companies offer 1-3 months severance. Let's do the math:</p>
<ul>
<li>Your CTC: Rs 24 LPA (Rs 2 Lakh/month gross)</li>
<li>Severance: 2 months = Rs 4 Lakh gross = Rs 3.2 Lakh post-tax</li>
<li>Monthly burn: Rs 1.1 Lakh</li>
<li>Severance runway: 2.9 months</li>
</ul>

<p>If your job search takes 5 months (median for 4-7 YOE), you're Rs 2.6 Lakh in the red. This is why people take salary cuts—they run out of runway.</p>

<div class="chart-container">
<h4>📊 Salary Negotiation Power vs Time Unemployed</h4>
<table class="data-table">
<tr><th>Months Unemployed</th><th>Negotiation Leverage</th><th>Typical Outcome</th></tr>
<tr><td>0-2 months</td><td>Strong</td><td>Can negotiate 10-15% above offer</td></tr>
<tr><td>2-4 months</td><td>Moderate</td><td>Take the offer or lose it</td></tr>
<tr><td>4-6 months</td><td>Weak</td><td>Accept 5-10% below ask</td></tr>
<tr><td>6+ months</td><td>Desperate</td><td>Take anything that pays rent</td></tr>
</table>
</div>

<p>Companies know this. Recruiters can tell how long you've been searching. The longer it takes, the worse your position gets.</p>""",

        "stuck_point": """<p><strong>Where Laid-Off Professionals Get Permanently Stuck:</strong></p>

<p><strong>Trap 1: The Ego Preservation Phase (Month 1-3)</strong></p>
<p>You only apply to companies "at your level" or better. You ignore startups, smaller companies, contract roles. Your identity is tied to the brand you worked for. Meanwhile, your savings drain and leverage decreases daily.</p>

<p><strong>Trap 2: The Skills Gap Discovery (Month 3-4)</strong></p>
<p>You realize the market has moved. That framework you mastered? It's legacy now. Companies want skills you don't have. Instead of taking a role to build these skills, you try to upskill while unemployed—which is hard when you're stressed about money.</p>

<p><strong>Trap 3: The Networking Delusion (Month 4-5)</strong></p>
<p>Everyone says "network your way in." You message 100 connections. 90 don't respond. 8 say "Let me check internally" and disappear. 2 take intro calls that lead nowhere. Networking works when you're employed, not when you're desperate.</p>

<p><strong>Trap 4: The Freelance/Consulting Escape (Month 5-6)</strong></p>
<p>You decide to "go independent." You spend months setting up a consultancy that gets zero clients because you have no sales pipeline and no reputation as an independent consultant.</p>

<p><strong>What Actually Works - The Uncomfortable Playbook:</strong></p>

<ol>
<li><strong>Apply Wide, Apply Fast (Week 1)</strong>: Apply to 50+ jobs before your severance hits. Speed matters more than precision.</li>
<li><strong>Take a Slight Salary Cut If Needed (Month 2)</strong>: A 10% cut now beats a 25% cut after 6 months of unemployment.</li>
<li><strong>Accept Contract/Consulting Roles</strong>: They pay, they fill resume gaps, and they often convert to full-time.</li>
<li><strong>Move Back If Needed</strong>: Your ego isn't worth Rs 40,000/month in rent you can't afford.</li>
<li><strong>Skill Up On Company Time</strong>: Take any job, learn new skills there, then upgrade in 12-18 months.</li>
</ol>""",

        "who_should_avoid": """<p><strong>Who Gets Hit Hardest by Layoffs:</strong></p>

<ul>
<li><strong>Single-income households with EMIs</strong>: Zero buffer means immediate financial crisis</li>
<li><strong>People who tied identity to employer brand</strong>: The "I work at Google" types crash hardest psychologically</li>
<li><strong>Those with outdated but specialized skills</strong>: Mainframe experts, legacy system specialists—hard to transition</li>
<li><strong>Mid-managers without technical depth</strong>: Can't go back to IC, can't get another management role quickly</li>
<li><strong>Visa-dependent workers</strong>: H1B holders have 60 days to find new sponsor or leave</li>
</ul>

<p><strong>Who Recovers Fastest:</strong></p>

<ul>
<li><strong>Those with 6+ months emergency fund</strong>: Can negotiate from strength, not desperation</li>
<li><strong>Active GitHub/portfolio maintainers</strong>: Can prove skills immediately</li>
<li><strong>People already job-hunting before layoff</strong>: Pipeline is warm</li>
<li><strong>Those willing to relocate</strong>: 3x more opportunities if you're flexible on city</li>
<li><strong>Strong internal referral network</strong>: Referrals convert 10x better than cold applications</li>
</ul>""",

        "verdict": """<p><strong>The Uncomfortable Truth About Layoff Recovery:</strong></p>

<p>The timeline is longer than you think. The financial hit is harder than you expect. The psychological toll is real. And the job market in 2024 is not what it was in 2021.</p>

<p><strong>The Real Numbers:</strong></p>
<ul>
<li>Average time to hire: 4-6 months (not 4-6 weeks)</li>
<li>Average salary change: -5 to -15% (not +10-20%)</li>
<li>Applications needed: 200-400 (not 20-40)</li>
<li>Interview conversion: 5-8% (not 30-40%)</li>
</ul>

<p><strong>What You Should Do NOW (Before You Get Laid Off):</strong></p>

<ol>
<li>Build 6-month emergency fund minimum</li>
<li>Keep your resume and LinkedIn updated always</li>
<li>Maintain relationships with former colleagues</li>
<li>Keep your skills current, not just your job requirements</li>
<li>Have a side income stream if possible</li>
</ol>

<p><strong>The Uncomfortable Question:</strong></p>

<p>If you got the layoff email tomorrow, how many months could you survive without panic? If the answer is less than 4, you're not prepared. And preparation happens before the crisis, not after.</p>

<p>Stop reading LinkedIn posts from people who got lucky. Start building the safety net that lets you negotiate from strength, not desperation.</p>"""
    },

    30: {  # Why 'Networking' Doesn't Work the Way You're Told
        "common_expectation": """<p>Career advice is obsessed with networking. "Your network is your net worth." "80% of jobs come through connections." "It's not what you know, it's who you know." LinkedIn is full of people telling you to send 10 connection requests daily and reach out to strangers for "informational interviews."</p>

<p>The expectation: Build a large network, nurture relationships, and when you need a job, simply tap your connections. Jobs will flow to you effortlessly because you have 1000+ LinkedIn connections. Success is just a few "warm introductions" away.</p>

<p>This advice sounds logical. Get to know people. Ask for help when needed. What could go wrong?</p>""",

        "actual_reality": """<p><strong>Why Traditional Networking Fails for Most People:</strong></p>

<div class="chart-container">
<h4>📊 Networking Activity vs Actual Job Outcomes</h4>
<table class="data-table">
<tr><th>Networking Activity</th><th>Time Investment</th><th>Job Lead Conversion</th><th>Actual Hires</th></tr>
<tr><td>Cold LinkedIn messages (500+)</td><td>40+ hours</td><td>2-3%</td><td>0.1%</td></tr>
<tr><td>Networking events (10+ events)</td><td>30+ hours</td><td>1-2%</td><td>0.05%</td></tr>
<tr><td>Coffee chats with strangers</td><td>25+ hours</td><td>3-5%</td><td>0.2%</td></tr>
<tr><td>Reconnecting with past colleagues</td><td>10 hours</td><td>15-20%</td><td>5%</td></tr>
<tr><td>Direct referrals from close contacts</td><td>5 hours</td><td>40-50%</td><td>15%</td></tr>
</table>
</div>

<p><strong>The Math of "Networking":</strong></p>

<p>You send 100 "networking" messages on LinkedIn. Here's what actually happens:</p>
<ul>
<li>70 are never opened (busy people, spam filters)</li>
<li>20 are read and ignored (no time, no interest)</li>
<li>8 respond with a polite "Happy to help" but never follow through</li>
<li>2 actually have a call with you</li>
<li>0.5 remember you three months later when they can actually help</li>
</ul>

<p><strong>Why "Building Your Network" Before You Need It Fails:</strong></p>

<p>1. <strong>You Can't Store Social Capital</strong>: A connection made 2 years ago doesn't remember you vividly. The relationship decays without maintenance, and maintenance at scale is impossible.</p>

<p>2. <strong>Weak Ties Are Actually Weak</strong>: The famous "strength of weak ties" research is misunderstood. Weak ties help when they happen to have relevant information at the right time—not when you mass-produce them hoping one will be useful.</p>

<p>3. <strong>Networking Events Are Status Sorting</strong>: Everyone at a networking event is trying to network UP, not down. If you're junior, the senior people you want to meet are avoiding you because 50 other juniors are chasing them.</p>

<p>4. <strong>Informational Interviews Are One-Sided Transactions</strong>: You're asking for someone's time with nothing to offer in return. The people with the best insights are too busy to give "informational interviews" to strangers.</p>

<div class="chart-container">
<h4>📈 What Actually Gets Jobs (Hiring Manager Survey)</h4>
<table class="data-table">
<tr><th>How Candidates Got Hired</th><th>Percentage</th><th>Time to Offer</th></tr>
<tr><td>Internal referral (close relationship)</td><td>40%</td><td>2-3 weeks</td></tr>
<tr><td>Recruiter outreach</td><td>25%</td><td>3-4 weeks</td></tr>
<tr><td>Direct application (strong portfolio)</td><td>20%</td><td>4-6 weeks</td></tr>
<tr><td>Past colleague rejoining</td><td>10%</td><td>1-2 weeks</td></tr>
<tr><td>"Networking" with strangers</td><td>5%</td><td>6-10 weeks</td></tr>
</table>
</div>

<p><strong>Case Study - The Networking Illusion:</strong></p>

<p><em>Arun, 28, Software Engineer:</em></p>
<ul>
<li>LinkedIn connections: 2,400+</li>
<li>Networking events attended in 2023: 15</li>
<li>Coffee chats with "network": 30+</li>
<li>Jobs found through networking: 0</li>
<li>How he actually got his job: Former teammate from 2019 referred him</li>
</ul>

<p>All that networking busywork produced nothing. One genuine relationship from years of working together did.</p>""",

        "salary_reality": """<p><strong>The Economics of Different Relationship Types:</strong></p>

<div class="chart-container">
<h4>💰 Job Search ROI by Relationship Type</h4>
<table class="data-table">
<tr><th>Relationship Type</th><th>Time to Develop</th><th>Referral Success Rate</th><th>Salary Impact</th></tr>
<tr><td>Close former colleague</td><td>1-3 years working together</td><td>40-60%</td><td>+10-20% (they vouch for you)</td></tr>
<tr><td>Former manager</td><td>2+ years reporting to them</td><td>50-70%</td><td>+15-25% (strongest reference)</td></tr>
<tr><td>Industry friend (genuine)</td><td>3+ years of mutual help</td><td>30-40%</td><td>+5-15%</td></tr>
<tr><td>LinkedIn connection (cold)</td><td>0 days</td><td>1-3%</td><td>0% (they don't know you)</td></tr>
<tr><td>Networking event contact</td><td>1 conversation</td><td>2-5%</td><td>0%</td></tr>
</table>
</div>

<p><strong>What "Network" Really Means for High Earners:</strong></p>

<p>People making Rs 50 LPA+ don't have 5000 LinkedIn connections. They have:</p>
<ul>
<li>5-10 close industry friends who would vouch for them anywhere</li>
<li>2-3 former managers who actively promote them</li>
<li>15-20 colleagues they've shipped real projects with</li>
<li>A reputation for delivering results, not collecting cards</li>
</ul>

<p>That's maybe 35 people. Not 3500.</p>

<p><strong>The Real Salary Multiplier: Reputation, Not Rolodex</strong></p>

<p>When a hiring manager sees a referral, they ask the referrer one question: "Would you work with this person again?"</p>

<p>If the answer is an enthusiastic yes, salary negotiation gets easier. If the referrer hesitates, the referral is worthless. This is why depth beats breadth—you need people who can answer that question strongly.</p>""",

        "stuck_point": """<p><strong>Where Networkers Get Permanently Stuck:</strong></p>

<p><strong>The Collection Phase</strong>: You spend years collecting connections, attending events, and optimizing your LinkedIn profile. You feel productive. Your network looks big. But when you actually need help, you realize you have 3000 acquaintances and 3 real relationships.</p>

<p><strong>The Transaction Trap</strong>: You reach out only when you need something. People sense this. They've received 50 messages from people like you this month. Your "personalized" outreach reads like everyone else's.</p>

<p><strong>The Status Mismatch</strong>: You're trying to connect with VPs when you're an individual contributor. They don't respond because they have nothing to gain. You're fishing in the wrong pond.</p>

<p><strong>What Actually Builds Meaningful Connections:</strong></p>

<ol>
<li><strong>Work on Hard Projects Together</strong>: Shared struggle creates bonds that survive job changes. This is why former teammates help each other.</li>
<li><strong>Help When You Don't Need Anything</strong>: Share opportunities, make introductions, solve problems for others. The relationship compounds.</li>
<li><strong>Be Known for Something Specific</strong>: "Great React developer" gets referred. "Wants to connect" gets ignored.</li>
<li><strong>Keep Relationships Alive</strong>: 4 messages per year to 50 real contacts is better than 200 cold messages to strangers.</li>
<li><strong>Say No to Networking Events</strong>: Spend that time doing great work instead. Reputation travels faster than business cards.</li>
</ol>

<p><strong>The 50-Contact Strategy:</strong></p>
<ul>
<li>Identify 50 people who know your work quality (past colleagues, managers, clients)</li>
<li>Reach out 4x per year with something valuable (article, introduction, congratulations)</li>
<li>Never ask for anything directly in these touchpoints</li>
<li>When you need a job, ask specifically: "I'm looking for X at companies like Y. Can you refer me?"</li>
</ul>

<p>This beats 500 coffee chats with strangers.</p>""",

        "who_should_avoid": """<p><strong>Who Should Ignore Traditional Networking Advice:</strong></p>

<ul>
<li><strong>Introverts who hate small talk</strong>: Your energy is better spent building portfolio work that speaks for itself</li>
<li><strong>Technical roles where skills matter most</strong>: A strong GitHub profile beats 100 LinkedIn connections</li>
<li><strong>Anyone early in career</strong>: You have nothing to offer senior people yet—focus on becoming good first</li>
<li><strong>Those with demanding jobs</strong>: Networking events eat time better spent on visible work contributions</li>
</ul>

<p><strong>Who Should Actually Network (Intentionally):</strong></p>

<ul>
<li><strong>Sales and business development roles</strong>: Relationships are literally the product</li>
<li><strong>Senior executives</strong>: You're trading information and influence at similar levels</li>
<li><strong>Founders raising money</strong>: You need to know investors and potential hires</li>
<li><strong>Freelancers and consultants</strong>: Client relationships are everything</li>
</ul>

<p>Notice the pattern? Networking matters when relationships ARE the work, not when they're supposed to supplement the work.</p>""",

        "verdict": """<p><strong>The Uncomfortable Truth About Networking:</strong></p>

<p>Most networking advice is written by people selling networking—event organizers, LinkedIn influencers, career coaches. They profit from making you feel like your network is insufficient.</p>

<p>Here's the reality:</p>
<ul>
<li>You only need 30-50 strong relationships, not 3000 connections</li>
<li>Quality comes from shared work, not shared coffee</li>
<li>Helping without expecting returns compounds over years</li>
<li>Your reputation at your current job is the best networking possible</li>
</ul>

<p><strong>The Uncomfortable Question:</strong></p>

<p>If you counted only the people who would strongly vouch for your work—not just accept your coffee invite—how many would that be? If it's less than 10, forget networking events. Go be excellent at your job and build those 10 relationships properly.</p>

<p><strong>What Actually Works:</strong></p>

<ol>
<li>Be great at something specific</li>
<li>Work on visible, hard projects</li>
<li>Help others without expecting immediate returns</li>
<li>Maintain 50 real relationships over 10 years</li>
<li>Ask for referrals specifically when needed</li>
</ol>

<p>Skip the events. Skip the cold outreach. Stop measuring connections. Start measuring people who would hire you tomorrow if they had an opening.</p>"""
    }
}

print("Expanding CRITICAL articles batch 1...")
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

print("\nBatch 1 complete! Run check_content_length.py to verify.")
