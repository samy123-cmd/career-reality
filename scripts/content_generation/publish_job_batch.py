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

# Common Setup
author = Author.objects.get(name="P. Mishra")

# ==============================================================================
# ARTICLE 1: DATA SCIENCE (THE SQL JANITOR)
# ==============================================================================
slug_1 = "junior-data-scientist-reality-india-sql-janitor"
title_1 = "The Junior Data Science Reality: You Are a SQL Janitor"
cat_1, _ = Category.objects.get_or_create(name="Data Science", defaults={"slug": "data-science", "order": 3})

table_1 = """
<div style="margin-top: 3rem; margin-bottom: 2rem;">
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 30%">Role Type</th>
            <th style="width: 30%">Reality (LPA)</th>
            <th style="width: 40%">Actual Work</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Cool AI Jobs</td>
            <td>18.0 - 30.0</td>
            <td>
                Research / LLMs
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 10%"></div></div>
            </td>
        </tr>
        <tr>
            <td>Real Jobs</td>
            <td>5.0 - 12.0</td>
            <td>
                Cleaning CSVs
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 90%; background: #666;"></div></div>
            </td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*90% of openings are Mislabelled Data Analyst roles.</p>
</div>
"""

persona_1 = """
<p>This article is written for the "Kaggle Grandmaster" wannabe.</p>

<p>You have spent the last 6 months living in Jupyter Notebooks. You know the mathematical difference between L1 and L2 regularization. You have fine-tuned a BERT model on a dataset you found on Reddit. You dream in PyTorch and Scikit-learn.</p>

<p>You believe that your first job will involve "Building Models", "Training AI", or "Solving AGI".</p>

<p>You believe you are entering the industry as a Scientist — a thinker who will be paid to experiment, hypothesize, and optimize.</p>

<p>If you think your daily life will resemble an DeepMind research paper, this article is your reality check.</p>
"""

expectation_1 = """
<p>The expectation is sold to you by EdTech influencers and Coursera certificates.</p>

<p><strong>"Data is the new Oil."</strong></p>

<p>You expect to walk into a company and be handed a perfectly clean, labeled dataset. You expect the Business Stakeholders to ask you for "Predictions" and "Insights".</p>

<p>You imagine your workflow like this:</p>
<ul>
<li>Import Data</li>
<li>Train Model</li>
<li>Optimize Hyperparameters</li>
<li>Present cool 3D graphs to the CEO</li>
<li>Get promoted for increasing revenue by 20%</li>
</ul>

<p>You think 80% of your time will be spent on <strong>Modelling</strong> and 20% on deployment.</p>

<p>You think SQL is "legacy tech" for backend engineers, and Excel is for finance guys.</p>
"""

reality_1 = """
<p><strong>The Reality: You are a glorified Plumber.</strong></p>

<p>Real-world data is not a Kaggle dataset. It is a crime scene.</p>

<p>It lives in 50 disconnected Excel sheets, a legacy SQL database that crashes if you query more than 1 month of rows, and a random PDF on a sales manager's desktop.</p>

<p>Companies do not have "Modelling" problems. They have "Data Quality" problems.</p>

<p>Your job is not to build Neural Networks. Your job is to write ugly, 500-line SQL joins to figure out why the "Total Revenue" column in the Sales Database doesn't match the "Bank Deposit" column in the Finance Database.</p>

<p>You will spend 90% of your time cleaning data. Parsing dates that are formatted wrong. Fixing spelling mistakes in city names. Removing duplicates that shouldn't exist.</p>

<p>You will not touch an LLM. You will touch `pandas.dropna()` and `Regex`. And you will cry.</p>

<p>Most companies don't need AI. They need a dashboard that works.</p>
"""

salary_prose_1 = """
<p>This misalignment shows up in the salary.</p>

<p>Unless you have a PhD or are in the top 1% of graduates from IISc or Old IITs, you are not getting the "AI Researcher" salary (₹30 LPA+).</p>

<p>You are getting the "Data Analyst" salary (₹6-12 LPA), even if your title says "Junior Data Scientist".</p>

<p>Companies know that the supply of Juniors who can "import sklearn" is infinite. The supply of potential employees who can actually clean a dirty warehouse database is low.</p>
"""
salary_reality_1 = salary_prose_1 + table_1

stuck_1 = """
<p>You get stuck because you refuse to accept your role.</p>

<p>You turn your nose up at <strong>Data Engineering</strong>. You think writing pipelines, configuring Airflow, and managing ETL jobs is "below you". You want to do the Math.</p>

<p>So you sit in your corner, building complex models on your local machine that never get deployed because the data infrastructure doesn't support them.</p>

<p>Meanwhile, the "Average" engineer who learned SQL, DBT, and Cloud Infrastructure is getting promoted because they are actually delivering value (clean data) to the business.</p>

<p>The market pays for Pipelines, not Notebooks. If you can't put your model in production, you are useless.</p>
"""

avoid_1 = """
<p><strong>Avoid if:</strong> You hate cleaning up other people's messes. If you have a low tolerance for ambiguity and broken systems, you will burn out in 3 months.</p>

<p><strong>This career works for:</strong> Detectives. People who enjoy the hunt. People who find satisfaction in taking a chaotic, broken mess and making it orderly.</p>
"""

verdict_1 = """
<p><strong>Learn SQL and MLOps.</strong></p>

<p>Stop trying to be an "AI Architect" as a fresher. Be the person who can actually get clean data from Point A to Point B.</p>

<p>The "Sexy" part of Data Science is a luxury. The "Janitor" part is a necessity.</p>

<p>If you want to survive, become a Data Engineer who knows Statistics, not a Statistician who refuses to Engineering.</p>
"""

Article.objects.update_or_create(
    slug=slug_1,
    defaults={
        "title": title_1, "author": author, "category": cat_1, "status": "published",
        "target_persona": persona_1, "who_should_avoid": avoid_1, "common_expectation": expectation_1,
        "actual_reality": reality_1, "salary_reality": salary_reality_1, "stuck_point": stuck_1, "verdict": verdict_1,
        "meta_title": "The Junior Data Science Reality: You Are a SQL Janitor",
        "meta_description": "Why 90% of Data Science jobs are actually Data Engineering. The truth about AI hype vs reality in India.",
        "published_at": timezone.now(), "last_reality_check": datetime.date.today()
    }
)
print(f"Published Savage: {title_1}")


# ==============================================================================
# ARTICLE 2: FRONTEND (REACT TRAP)
# ==============================================================================
slug_2 = "frontend-developer-reality-react-is-not-a-career"
title_2 = "The Frontend Reality: React is Not a Career"
cat_2, _ = Category.objects.get_or_create(name="Engineering", defaults={"slug": "engineering", "order": 4})

table_2 = """
<div style="margin-top: 3rem; margin-bottom: 2rem;">
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
            <td>UI Library User</td>
            <td>4.0 - 8.0</td>
            <td>
                Low (Saturated)
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 30%"></div></div>
            </td>
        </tr>
        <tr>
            <td>Engineeer (JS/TS)</td>
            <td>12.0 - 25.0</td>
            <td>
                High
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 80%"></div></div>
            </td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*Knowing `useEffect` is no longer a differentiator.</p>
</div>
"""

persona_2 = """
<p>This article is for the "Bootcamp React Dev".</p>

<p>You learned HTML, CSS, and React in 3 months. You built a Todo App, a Weather App, and a Netflix Clone following a YouTube tutorial.</p>

<p>You have memorized the syntax for `useState` and `useEffect`. You know how to center a div using Flexbox.</p>

<p>You believe this qualifies you for a ₹15 LPA "Software Engineer" role.</p>

<p>You think Frontend Development is about making things look pretty, adding animations, and converting Figma designs into code.</p>
"""

expectation_2 = """
<p>You expect to be hired for your "Creativity".</p>

<p>You think your job will be to install `npm install framer-motion`, build smooth sliders, and argue about pixel perfection.</p>

<p>You believe that as long as you know the latest framework (Next.js, Remix, whatever is trending on Twitter), you are safe.</p>

<p>You think the "Backend" is scary and complicated, so you will just stay happily in the browser, manipulating the DOM.</p>
"""

reality_2 = """
<p><strong>The Reality: "Pixel Moving" is dead.</strong></p>

<p>The market has shifted. AI tools (v0, Cursor, Copilot) can write basic UI components faster and cleaner than you can.</p>

<p>If your value proposition is "I can write a nice Button component", you are obsolete.</p>

<p>The market doesn't need "React Developers" anymore. It needs <strong>Product Engineers</strong>.</p>

<p>Companies today expect Frontend Engineers to handle logic, not just aesthetics. They expect you to understand:</p>
<ul>
<li>Server Side Rendering (SSR) vs Client Side Rendering (CSR)</li>
<li>Caching Strategies (SWR, React Query)</li>
<li>API Design and Data Fetching Waterfalls</li>
<li>Performance Optimization (Core Web Vitals)</li>
</ul>

<p>"Frontend" is no longer just the View layer. It is becoming the entire Application layer. If you can't handle the logic, you are just a decorator.</p>
"""

salary_prose_2 = """
<p>The entry-level market is flooded. There are 10,000 juniors for every React job.</p>

<p>Because the barrier to entry was so low (3 months), supply has exploded. This crushes wages.</p>

<p>If you want to earn money, you have to verify yourself. You have to move down the stack (Backend/Full Stack) or deeper into the browser (WebGL, Canvas, Complex State).</p>

<p>The days of getting paid ₹10 LPA to center divs are over.</p>
"""
salary_reality_2 = salary_prose_2 + table_2

stuck_2 = """
<p>You get stuck in <strong>Div Soup</strong>.</p>

<p>You are great at building specific components, but you panic when you have to glue them together into a real app.</p>

<p>You don't know how the internet works. You don't understand HTTP, DNS, or CORS. If the API returns a 500 error, you freeze. You blame the Backend guy.</p>

<p>You keep learning new "Tools" to mask your lack of "First Principles". You jump from Redux to Zustand to Jotai, hoping the next library will fix your confusion. It won't.</p>
"""

avoid_2 = """
<p><strong>Avoid if:</strong> You only care about the Visuals. If you hate logic and just want things to look nice, go be a UI Designer. Code is logic, not art.</p>
"""

verdict_2 = """
<p><strong>Learn the Server.</strong></p>

<p>Frontend is just a consumption layer. The real logic is on the server (Next.js/Node/Go). </p>

<p>Stop labelling yourself as a "React Developer". Be a "Software Engineer" who happens to know React.</p>

<p>If you can't write a DB query, you are half an engineer. And you will be paid half the salary.</p>
"""

Article.objects.update_or_create(
    slug=slug_2,
    defaults={
        "title": title_2, "author": author, "category": cat_2, "status": "published",
        "target_persona": persona_2, "who_should_avoid": avoid_2, "common_expectation": expectation_2,
        "actual_reality": reality_2, "salary_reality": salary_reality_2, "stuck_point": stuck_2, "verdict": verdict_2,
        "meta_title": "The Frontend Developer Reality: React is Not a Career",
        "meta_description": "Why knowing React is no longer enough in 2025. The shift to Full Stack and the impact of AI on UI coding.",
        "published_at": timezone.now(), "last_reality_check": datetime.date.today()
    }
)
print(f"Published Savage: {title_2}")


# ==============================================================================
# ARTICLE 3: PRODUCT MANAGER (JIRA JANITOR)
# ==============================================================================
slug_3 = "product-manager-reality-india-jira-janitor"
title_3 = "The Product Manager Reality: You Are a Jira Janitor"
cat_3, _ = Category.objects.get_or_create(name="Product Management", defaults={"slug": "product-management", "order": 5})

table_3 = """
<div style="margin-top: 3rem; margin-bottom: 2rem;">
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 30%">Role</th>
            <th style="width: 25%">Pay (LPA)</th>
            <th style="width: 45%">Stress Source</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>APM / PM 1</td>
            <td>12.0 - 18.0</td>
            <td>
                Execution
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 40%"></div></div>
            </td>
        </tr>
        <tr>
            <td>PM 2 / Senior</td>
            <td>22.0 - 35.0</td>
            <td>
                Politics + Alignment
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 90%; background: #d93025;"></div></div>
            </td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*Responsibility > Authority.</p>
</div>
"""

persona_3 = """
<p>This is for the "Mini-CEO".</p>

<p>You either did an MBA or transitioned from Engineering because you wanted to "Define Strategy". You read Marty Cagan's *Inspired* and Lenny's Newsletter religiously.</p>

<p>You think you are the Steve Jobs of your feature. You believe you will command the roadmap, have grand visions, and lead the team to victory.</p>

<p>You think being a PM is about "Ideas".</p>
"""

expectation_3 = """
<p>You expect to spend your days whiteboarding, looking at analytics charts, and giving inspiring speeches to developers.</p>

<p>You expect Engineers to report to you (or at least listen to you).</p>
<p>You expect Designers to execute your vision perfectly.</p>
<p>You expect the CEO to ask for your opinion on the "Next Big Thing".</p>

<p>You think your job is to tell people what to do.</p>
"""

reality_3 = """
<p><strong>The Reality: You are a Secretary for Engineers.</strong></p>

<p>You find out the hard way that you have all the <strong>Responsibility</strong> but <strong>Zero Authority</strong>.</p>

<p>The Engineers report to the Engineering Manager. The Designers report to the Design Lead. You are nobody's boss. You cannot order anyone to do anything.</p>

<p>To get a single button changed, you have to beg, plead, and "influence".</p>

<p>Your day is not Strategy. Your day is:</p>
<ul>
<li>Updating JIRA tickets so the team looks busy</li>
<li>Writing requirement documents that nobody reads</li>
<li>Sitting in "Alignment Calls" for 6 hours where people argue about semantics</li>
<li>Apologizing to Sales for why the feature is delayed again</li>
</ul>

<p>You are not the CEO. You are the Janitor who cleans up the mess so the Engineers can work. You are the "Shit Umbrella" that protects the team from management chaos.</p>
"""

salary_prose_3 = """
<p>The money is good. PMs are often the highest-paid individual contributors.</p>

<p>But the "Hourly Rate" is terrible. Because you are the central point of failure, you never really clock off. If the server crashes on Sunday, the Engineer fixes it, but <em>you</em> have to explain it to the stakeholders.</p>

<p>You are paying for that salary with your peace of mind.</p>
"""
salary_reality_3 = salary_prose_3 + table_3

stuck_3 = """
<p>You get stuck in the <strong>Feature Factory</strong>.</p>

<p>You know what the "Right Product" is. But the CEO wants Feature X because he promised it to an investor. The Sales Head wants Feature Y to close a deal.</p>

<p>You stop fighting. You become a ticket-pusher. You ship trash features just to meet a deadline, knowing they won't work.</p>

<p>You are measured on "shipping", not "impact". So you ship. And the product becomes a bloated mess.</p>
"""

avoid_3 = """
<p><strong>Avoid if:</strong> You have thin skin. Everyone hates the PM when things go wrong. When things go right, the Engineers get the credit.</p>

<p><strong>Avoid if:</strong> You crave closure. A PM's job is never "Done". There is always a bug, a complaint, or a new requirement.</p>
"""

verdict_3 = """
<p><strong>Learn to Influence without Authority.</strong></p>

<p>Stop acting like a Boss. Start acting like an Enabler. Your job is to make the Engineer's life easier, not harder.</p>

<p>If you can gain the trust of your Engineering team, you can move mountains. If they think of you as "Management", you are dead.</p>

<p>Humility is your most expensive skill.</p>
"""

Article.objects.update_or_create(
    slug=slug_3,
    defaults={
        "title": title_3, "author": author, "category": cat_3, "status": "published",
        "target_persona": persona_3, "who_should_avoid": avoid_3, "common_expectation": expectation_3,
        "actual_reality": reality_3, "salary_reality": salary_reality_3, "stuck_point": stuck_3, "verdict": verdict_3,
        "meta_title": "The Product Manager Reality: You Are a Jira Janitor",
        "meta_description": "Product Management is not about being CEO. It's about responsibility without authority. The truth about PM stress in India.",
        "published_at": timezone.now(), "last_reality_check": datetime.date.today()
    }
)
print(f"Published Savage: {title_3}")


# ==============================================================================
# ARTICLE 4: DIGITAL MARKETING (AGENCY SLAVERY)
# ==============================================================================
slug_4 = "digital-marketing-reality-agency-burnout"
title_4 = "The Digital Marketing Reality: Agency Slavery vs B2B Strategy"
cat_4, _ = Category.objects.get_or_create(name="Marketing", defaults={"slug": "marketing", "order": 6})

table_4 = """
<div style="margin-top: 3rem; margin-bottom: 2rem;">
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
            <td>Agency (Client Service)</td>
            <td>3.6 - 6.0</td>
            <td>
                Extreme
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 100%; background: #d93025;"></div></div>
            </td>
        </tr>
        <tr>
            <td>B2B / SaaS In-House</td>
            <td>10.0 - 18.0</td>
            <td>
                Low
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 40%"></div></div>
            </td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*Agencies run on fresh blood and low wages.</p>
</div>
"""

persona_4 = """
<p>This is for the "Creative Soul".</p>

<p>You watched "Emily in Paris" or "Mad Men" and thought Marketing was your calling. You see yourself as a storyteller, a brand builder, a viral sensation.</p>

<p>You love making Reels, writing clever captions, and thinking about "Brand Identity".</p>

<p>You joined a Digital Marketing Agency expecting high energy, creativity, and cool clients.</p>
"""

expectation_4 = """
<p>You expect to be valued for your Ideas.</p>

<p>You imagine brainstorming sessions in bean bags, sipping coffee, and coming up with the next Nike slogan.</p>

<p>You expect to work on strategy. You expect clients to listen to your expertise.</p>

<p>You think Marketing is an Art.</p>
"""

reality_4 = """
<p><strong>The Reality: It is a Spreadsheet Job.</strong></p>

<p>Modern marketing is not Art; it is Math. It is CAC (Customer Acquisition Cost), LTV (Lifetime Value), ROAS (Return on Ad Spend), and Attribution Models.</p>

<p>If you work in an Agency, you are not a Strategist. You are a factory worker.</p>

<p>You handle 10 clients at once. Each one calls you at 9 PM screaming about why they didn't get 100 leads today.</p>

<p>You spend your day:</p>
<ul>
<li>Making 50 slightly different versions of a banner on Canva</li>
<li>Setting up Facebook Ad sets</li>
<li>Formatting Excel reports</li>
<li>Begging the client to approve a caption</li>
</ul>

<p>The "Creative" part is maybe 5% of the job. The rest is operations and crisis management.</p>
"""

salary_prose_4 = """
<p>Agencies pay peanuts because there is an endless supply of 22-year-olds willing to work for "exposure".</p>

<p>The business model of an agency is: Hire cheap juniors, sell them as experts, work them until they burn out in 18 months, replace them.</p>

<p>The money is in B2B / SaaS In-House roles. Where marketing drives Revenue, not just Likes. But getting there requires real skills (CRM, Automation, Analytics), not just "Content Creation".</p>
"""
salary_reality_4 = salary_prose_4 + table_4

stuck_4 = """
<p>You get stuck in the <strong>Vanity Trap</strong>.</p>

<p>You chase Likes, Views, and Followers because they give you a dopamine hit. But you cannot prove to the CEO that your work made money.</p>

<p>When a recession hits, the "Brand Marketing" team is fired first. The "Performance Marketing" team survives because they can show an Excel sheet that says "I spent $1 and made $3".</p>
"""

avoid_4 = """
<p><strong>Avoid if:</strong> You hate numbers. If the thought of a Pivot Table scares you, you are in the wrong industry. Excel is your boss now.</p>
"""

verdict_4 = """
<p><strong>Go B2B.</strong></p>

<p>Stop trying to be an Influencer. Start becoming a Revenue Driver.</p>

<p>Learn Performance Marketing, CRM (HubSpot/Salesforce), and Marketing Automation. Leave the "Creative" stuff to the freelancers.</p>

<p>Be the person who brings the Leads, and you will never be fired.</p>
"""

Article.objects.update_or_create(
    slug=slug_4,
    defaults={
        "title": title_4, "author": author, "category": cat_4, "status": "published",
        "target_persona": persona_4, "who_should_avoid": avoid_4, "common_expectation": expectation_4,
        "actual_reality": reality_4, "salary_reality": salary_reality_4, "stuck_point": stuck_4, "verdict": verdict_4,
        "meta_title": "The Digital Marketing Reality: Agency Slavery vs B2B",
        "meta_description": "Why Agency life is a burnout factory. The truth about Digital Marketing salaries and the shift to B2B.",
        "published_at": timezone.now(), "last_reality_check": datetime.date.today()
    }
)
print(f"Published Savage: {title_4}")


# Clean up old drafts
Article.objects.filter(slug__in=[
    "junior-data-scientist-reality-india", "frontend-developer-reality-2025", 
    "product-manager-reality-india", "digital-marketing-reality"
]).delete()
print("Cleaned up old drafts.")
