
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Article

# Expansion Data
EXPANSIONS = {
    7: { # 20 LPA Reality
        "case_study": """
<h3>Case Study: The "Rich" Broke Engineer</h3>
<p>Meet Aryan, 27. He just cracked a ₹22 LPA offer in Bangalore. He feels like a king. Fast forward 6 months:</p>
<ul>
    <li><strong>In-Hand:</strong> ₹1.35L (after taxes and PF)</li>
    <li><strong>Rent (Indiranagar):</strong> ₹35,000</li>
    <li><strong>Lifestyle (The "I'm Rich" Trap):</strong> ₹40,000 (Weekend parties, gadgets, ordering in)</li>
    <li><strong>Car EMI:</strong> ₹20,000 (Because "I need a status symbol")</li>
    <li><strong>Savings:</strong> ₹10,000 (If lucky)</li>
</ul>
<p><strong>The Verdict:</strong> Aryan isn't building wealth; he's funding a lifestyle that keeps him trapped in the job he hates. ₹20 LPA in 2026 is the new ₹10 LPA of 2016.</p>
""",
        "data_table": """
<h3>The Purchasing Power Reality Check</h3>
<div class="table-container">
    <table class="reality-table">
        <thead>
            <tr>
                <th>Expense Category</th>
                <th>₹10 LPA Lifestyle</th>
                <th>₹20 LPA Lifestyle (Expectation)</th>
                <th>The Reality</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Housing</td>
                <td>Shared Flat (₹15k)</td>
                <td>Fancy 1BHK (₹25k)</td>
                <td>Overpriced Gated Society (₹40k+)</td>
            </tr>
            <tr>
                <td>Transport</td>
                <td>Bike/Metro</td>
                <td>Sedan</td>
                <td>Uber Surge + EMI Trap</td>
            </tr>
            <tr>
                <td>Savings Output</td>
                <td>₹20k/month</td>
                <td>₹80k/month</td>
                <td>₹25k/month (Lifestyle Inflation)</td>
            </tr>
        </tbody>
    </table>
</div>
""",
        "deep_dive": """
<h3>Why 20 LPA Isn't Freedom</h3>
<p>The number 20 is psychological. It implies you've "made it". But in metro cities, it merely buys you entry into the "Upper Middle Class Trap". You lose the hunger of the struggler but lack the capital of the wealthy. You are in the uncomfortable middle where you are one layoff away from insolvency, yet you are expected to pick up the bill at dinner. This is the "Golden Handcuffs" phase.</p>
"""
    },
    4: { # Digital Marketing
        "case_study": """
<h3>Case Study: The Agency Burnout</h3>
<p>Riya, 24, joined a "Top Tier" digital agency. Expectation: Creating viral campaigns for Nike. Reality: Resizing banners for a tire company at 11 PM on a Friday.</p>
<p>She manages 5 clients, 3 of whom call on weekends. Her "creative" work is limited to choosing between Arial and Helvetica because the client has "no budget". After 2 years, her portfolio is full of mediocre work she can't show, and her salary has moved from ₹4LPA to ₹5.5LPA.</p>
""",
        "data_table": """
<h3>Agency vs. Product vs. Freelance</h3>
<div class="table-container">
    <table class="reality-table">
        <thead>
            <tr>
                <th>Metric</th>
                <th>Agency (The Grinder)</th>
                <th>In-House (The Bore)</th>
                <th>Freelance (The Hustle)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Work-Life Balance</td>
                <td>Non-existent (12h days)</td>
                <td>Good (9-5)</td>
                <td>Volatile (Feast/Famine)</td>
            </tr>
            <tr>
                <td>Salary Growth</td>
                <td>Slow (10-15%)</td>
                <td>Stable (20-30% switch)</td>
                <td>Exponential or Zero</td>
            </tr>
            <tr>
                <td>Creative Freedom</td>
                <td>Low (Client dictates)</td>
                <td>Medium (Brand guidelines)</td>
                <td>High (If you're good)</td>
            </tr>
        </tbody>
    </table>
</div>
""",
        "deep_dive": """
<h3>The "Creative Strat" is Dead</h3>
<p>AI is eating the bottom 80% of digital marketing. Copywriting, basic graphics, and ad scheduling are automated. If your skill is "I can run Facebook Ads", you are obsolete. The future belongs to "Growth Engineers" and "Data-Driven Marketers" who can connect API endpoints, not just write catchy slogans. The "Creative" era is over; the "Performance" era is brutal.</p>
"""
    },
    17: { # IT Services
        "case_study": """
<h3>Case Study: The "Bench" Warmer</h3>
<p>Vikram, 29, spent 4 years at a witch company. For 2 of those years, he was on the "bench" or doing "internal projects" (which meant filling Excel sheets). He listed "Java Expert" on his resume.</p>
<p>When he tried to switch to a Product startup, he failed the basic coding round. He realized his 4 years of experience were actually 6 months of experience repeated 8 times. He had to take a salary CUT to join a startup just to learn actual coding.</p>
""",
        "data_table": """
<h3>Service vs. Product Mindset</h3>
<div class="table-container">
    <table class="reality-table">
        <thead>
            <tr>
                <th>Feature</th>
                <th>IT Services (WITCH)</th>
                <th>Product Startup</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Code Quality</td>
                <td>"Make it work"</td>
                <td>"Make it scale"</td>
            </tr>
            <tr>
                <td>Learning Curve</td>
                <td>Flat after year 1</td>
                <td>Vertical (Sink or Swim)</td>
            </tr>
            <tr>
                <td>Exit Options</td>
                <td>Other IT Services</td>
                <td>FAANG, Unicorns, Founder</td>
            </tr>
        </tbody>
    </table>
</div>
""",
        "deep_dive": """
<h3>The Skill Rot is Real</h3>
<p>Staying in a legacy IT service role for >5 years is career suicide for a developer. Your salary might grow via "internal hikes" to match inflation, but your market value plummets. Real engineering happens where the product *is* the revenue, not where the *billable hours* are the revenue.</p>
"""
    },
    24: { # MBA Reality
        "case_study": """
<h3>Case Study: The Loan Burden</h3>
<p>Sarthak took a ₹20L loan for a Tier-2 MBA. He was promised "Marketing Management".</p>
<p>Campus placement got him a job at an EdTech. The role? "Business Development Associate". Reality? Cold calling parents to sell courses. He is essentially a telemarketer with an MBA degree, paying off a loan that eats 40% of his in-hand salary. He is trapped.</p>
""",
        "data_table": """
<h3>The Tier-1 vs. Tier-2/3 Gap</h3>
<div class="table-container">
    <table class="reality-table">
        <thead>
            <tr>
                <th>College Tier</th>
                <th>Avg. Fees</th>
                <th>Avg. Package (Real)</th>
                <th>Role Quality</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Tier 1 (IIM A/B/C)</td>
                <td>₹25L+</td>
                <td>₹25-30 LPA</td>
                <td>Strategy, Consulting, ProdMan</td>
            </tr>
            <tr>
                <td>Tier 2 (New IIMs/Pvt)</td>
                <td>₹15-20L</td>
                <td>₹10-12 LPA</td>
                <td>Sales, Ops, Analyst</td>
            </tr>
            <tr>
                <td>Tier 3 (Local)</td>
                <td>₹5-10L</td>
                <td>₹4-6 LPA</td>
                <td>Glorified Sales</td>
            </tr>
        </tbody>
    </table>
</div>
""",
        "deep_dive": """
<h3>The "Network" Myth</h3>
<p>People say "Do an MBA for the network." In a Tier-2 college, your network is 200 other confused people who couldn't crack CAT. That's not a network; that's a support group. Unless you are in the top 10 B-Schools, the ROI calculation is extremely dangerous in 2026.</p>
"""
    },
    20: { # Frontend Reality
        "case_study": """
<h3>Case Study: The Framework Hopper</h3>
<p>Amit spent 2023 mastering React. Then Next.js 13 came out with App Router. He learned that. Then Remix. Then Svelte. He spends 80% of his time learning tools and 20% building.</p>
<p>In an interview, he was asked to implement a `debounce` function in vanilla JS. He failed. He can configure Webpack but can't write an algorithm. He is valid only as long as the framework is trendy.</p>
""",
        "data_table": """
<h3>The "Churn" Tax</h3>
<div class="table-container">
    <table class="reality-table">
        <thead>
            <tr>
                <th>Era</th>
                <th>The "Must Know" Stack</th>
                <th>Lifespan</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>2015</td>
                <td>jQuery, Bootstrap</td>
                <td>5 Years</td>
            </tr>
            <tr>
                <td>2018</td>
                <td>React Class Components, Redux</td>
                <td>3 Years</td>
            </tr>
            <tr>
                <td>2022</td>
                <td>React Hooks, Tailwind</td>
                <td>2 Years</td>
            </tr>
            <tr>
                <td>2026</td>
                <td>Server Components, AI Gen UI</td>
                <td>???</td>
            </tr>
        </tbody>
    </table>
</div>
""",
        "deep_dive": """
<h3>AI is Coming for the "Pixel Pusher"</h3>
<p>Frontend development involves two parts: Logic and Layout. AI is already excellent at Layout (Tailwind, CSS). If your value is "I can center a div", you are in trouble. The future Frontend Engineer is actually a "Full Stack Lite" engineer who understands State, Caching, and Server Components. Pure UI devs are becoming an endangered species.</p>
"""
    }
}

def apply_updates():
    print(f"Applying updates to {len(EXPANSIONS)} articles...")
    for art_id, content in EXPANSIONS.items():
        try:
            article = Article.objects.get(id=art_id)
            print(f"Updating Article {article.id}: {article.title}")
            
            # Append content to 'actual_reality' and 'salary_reality' to boost length and value
            # We treat 'actual_reality' as the main body for the Deep Dive & Case Study
            
            if "case_study" in content and content["case_study"] not in article.actual_reality:
                article.actual_reality += "\n\n" + content["case_study"]
                
            if "deep_dive" in content and content["deep_dive"] not in article.actual_reality:
                article.actual_reality += "\n\n" + content["deep_dive"]
                
            # Append Table to 'salary_reality' or 'actual_reality' depending on context
            # We'll put charts in salary_reality usually, or actual_reality
            if "data_table" in content and content["data_table"] not in article.salary_reality:
                article.salary_reality += "\n\n" + content["data_table"]
            
            article.save()
            print("  -> Success")
            
        except Article.DoesNotExist:
            print(f"  -> Article {art_id} not found!")

if __name__ == "__main__":
    apply_updates()
