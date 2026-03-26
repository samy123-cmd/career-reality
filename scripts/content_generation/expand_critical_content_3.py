
import os
import django

import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Article

# Expansion Data Batch 3
EXPANSIONS = {
    26: { # Side Hustles
        "case_study": """
<h3>Case Study: The "Passive Income" Myth</h3>
<p>Karan read about "Passive Income" and started a drop-shipping store while working his Senior Dev job. He spent ₹2L on ads.</p>
<p>Reality: He spent his nights fulfilling orders and handling refund complaints. His performance at his main job slipped, costing him a ₹4L promotion. He made ₹50k profit from the store but lost ₹4L in potential salary growth. Side hustles are not passive; they are second jobs.</p>
""",
        "data_table": """
<h3>The True Cost of a Side Hustle</h3>
<div class="table-container">
    <table class="reality-table">
        <thead>
            <tr>
                <th>Resource</th>
                <th>Day Job</th>
                <th>Side Hustle</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Time Input</td>
                <td>40 Hours (Structured)</td>
                <td>20 Hours (Nights/Weekends)</td>
            </tr>
            <tr>
                <td>Reliability</td>
                <td>High (Monthly Salary)</td>
                <td>Zero (Sales dependent)</td>
            </tr>
            <tr>
                <td>Opportunity Cost</td>
                <td>None</td>
                <td>Health, Sleep, Main Career Focus</td>
            </tr>
        </tbody>
    </table>
</div>
""",
        "deep_dive": """
<h3>Focus is the New Oil</h3>
<p>In a specialized economy, the person who is top 1% at ONE thing extracts 80% of the value. The person who is "average" at two things gets replaced. Unless your side hustle is building a product that scales without code (SaaS/Content), trading hours for dollars in a second gig is a poor strategy compared to getting promoted.</p>
"""
    },
    27: { # Equity Trap
        "case_study": """
<h3>Case Study: The "Paper" Millionaire</h3>
<p>Arjun joined a Unicorn in 2021. He got ₹60L worth of ESOPs. He felt rich. He calculated his net worth including this.</p>
<p>2023: The funding winter hit. The company's valuation was slashed by 60%. His options are now "underwater" (Strike price > Share price). He cannot exercise them because the tax bill (Perquisite Tax) would be ₹20L cash upfront, which he doesn't have. He owns "paper wealth" that costs him money to keep.</p>
""",
        "data_table": """
<h3>ESOP Taxation Reality (India)</h3>
<div class="table-container">
    <table class="reality-table">
        <thead>
            <tr>
                <th>Stage</th>
                <th>Action</th>
                <th>Tax Impact</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Vesting</td>
                <td>You earn right to buy</td>
                <td>Zero</td>
            </tr>
            <tr>
                <td>Exercise</td>
                <td>You buy the shares</td>
                <td><strong>30%+ (Perquisite Tax)</strong> on paper gain!</td>
            </tr>
            <tr>
                <td>Sale (Exit)</td>
                <td>You sell shares</td>
                <td>10-20% (Capital Gains)</td>
            </tr>
        </tbody>
    </table>
</div>
""",
        "deep_dive": """
<h3>The Liquidation Preference Trap</h3>
<p>Investors get paid first. If the company sells for $100M, and VCs put in $80M with a "2x Liquidation Preference", they take $160M (or everything). Employees get zero. Common stock (ESOPs) is at the bottom of the food chain. Never accept a lower salary for "more equity" unless you see the Cap Table.</p>
"""
    },
    28: { # Manager vs IC
        "case_study": """
<h3>Case Study: The "Code-Sick" Architect</h3>
<p>Vikram was the best coder on the team. Naturally, they made him Engineering Manager.</p>
<p>Now he sits in Excel sheets, Jira, and 1:1 meetings all day. He hasn't committed code in 3 months. He feels useless. When he tries to intervene in architecture, the juniors resent him. He earns 20% more but enjoys his life 50% less. He wants to go back to IC, but his ego won't let him take a "demotion".</p>
""",
        "data_table": """
<h3>The Maker vs. Manager Schedule</h3>
<div class="table-container">
    <table class="reality-table">
        <thead>
            <tr>
                <th>Factor</th>
                <th>Individual Contributor (IC)</th>
                <th>Manager</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Unit of Work</td>
                <td>Code / Design / Output</td>
                <td>Decisions / Meetings / People</td>
            </tr>
            <tr>
                <td>Context Switching</td>
                <td>Low (Deep Work)</td>
                <td>Extreme (Every 30 mins)</td>
            </tr>
            <tr>
                <td>Dopamine Source</td>
                <td>"It Works!"</td>
                <td>"Team didn't quit"</td>
            </tr>
        </tbody>
    </table>
</div>
""",
        "deep_dive": """
<h3>The Pendulum Career</h3>
<p>The best modern career path isn't a ladder; it's a pendulum. Spend 3 years as an IC, then 2 years managing to learn empathy/business, then back to IC. Staying in management too long robs you of hard skills. Staying in IC too long limits your leverage. Swing between them.</p>
"""
    }
}

def apply_updates():
    print(f"Applying updates to {len(EXPANSIONS)} articles...")
    for art_id, content in EXPANSIONS.items():
        try:
            article = Article.objects.get(id=art_id)
            print(f"Updating Article {article.id}: {article.title}")
            
            if "case_study" in content and content["case_study"] not in article.actual_reality:
                article.actual_reality += "\n\n" + content["case_study"]
                
            if "deep_dive" in content and content["deep_dive"] not in article.actual_reality:
                article.actual_reality += "\n\n" + content["deep_dive"]
                
            if "data_table" in content and content["data_table"] not in article.salary_reality:
                article.salary_reality += "\n\n" + content["data_table"]
            
            article.save()
            print("  -> Success")
            
        except Article.DoesNotExist:
            print(f"  -> Article {art_id} not found!")

if __name__ == "__main__":
    apply_updates()
