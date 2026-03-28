
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Article

# Expansion Data Batch 2
EXPANSIONS = {
    18: { # Switching After 30
        "case_study": """
<h3>Case Study: The "Senior" Junior</h3>
<p>Rajesh, 32, was a Sales Manager earning ₹18 LPA. He hated it. He did a 6-month Data Science bootcamp. He thought his "management experience" would count.</p>
<p>Reality: Recruiters saw him as a fresher in Data Science. The offers he got were for ₹6-8 LPA. He couldn't afford the 60% pay cut because of his home loan. He is now back in Sales, but ₹2L poorer from the bootcamp fees. The window to switch effortlessly closes faster than you think.</p>
""",
        "data_table": """
<h3>The Cost of Switching Late</h3>
<div class="table-container">
    <table class="reality-table">
        <thead>
            <tr>
                <th>Factor</th>
                <th>Switching at 24</th>
                <th>Switching at 32</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <th>Salary Risk</th>
                <td>Low (Can take a cut)</td>
                <td>High (EMIs, Kids, Lifestyle)</td>
            </tr>
            <tr>
                <th>Ego Friction</th>
                <td>None (Happy to learn)</td>
                <td>High (Reporting to a 25yo)</td>
            </tr>
            <tr>
                <th>Ramp Up Time</th>
                <td>Fast (Single focus)</td>
                <td>Slow (Divided attention)</td>
            </tr>
        </tbody>
    </table>
</div>
""",
        "deep_dive": """
<h3>The "Unlearning" Curve</h3>
<p>The hardest part isn't learning Python; it's unlearning the "Manager" mindset. When you switch careers, you go from being an expert to being incompetent. Most 30-somethings can't handle the psychological blow of being the "dumbest person in the room" again.</p>
"""
    },
    21: { # Product Manager Reality
        "case_study": """
<h3>Case Study: The "Feature Factory" PM</h3>
<p>Neha thought PM meant "CEO of the Product". She imagined setting vision and strategy.</p>
<p>Reality: She spends 6 hours a day on Zoom calls. Sales wants feature X to close a deal. Support wants bug fix Y. Engineering says both are impossible. She is not a CEO; she is a sophisticated negotiator begging people to do work. She hasn't written a PRD in weeks; she just updates Jira tickets.</p>
""",
        "data_table": """
<h3>PM Types: Expectations vs Reality</h3>
<div class="table-container">
    <table class="reality-table">
        <thead>
            <tr>
                <th>PM Archetype</th>
                <th>What You Think You Do</th>
                <th>What You Actually Do</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Growth PM</td>
                <td>"Hacking Viral Loops"</td>
                <td>Changing button colors (A/B Tests)</td>
            </tr>
            <tr>
                <td>Tech PM</td>
                <td>"System Architecture"</td>
                <td>Explaining JSON to Sales</td>
            </tr>
            <tr>
                <td>Generalist PM</td>
                <td>"Strategy"</td>
                <td>Calendar Tetris & Jira Janitor</td>
            </tr>
        </tbody>
    </table>
</div>
""",
        "deep_dive": """
<h3>The Influence Without Authority Trap</h3>
<p>This is the most toxic phrase in tech. It implies you are responsible for the outcome but have zero power to fire/hire/direct the people doing the work. If the product fails, it's the PM's fault. If it succeeds, the Engineers are heroes. It requires a specific type of masochism to enjoy this.</p>
"""
    },
    22: { # Digital Marketing: Agency vs Brand (Focus on House)
        "case_study": """
<h3>Case Study: The "Brand Side" Bore</h3>
<p>Sameer escaped the agency grind to join a large FMCG brand. He wanted "strategy".</p>
<p>He got it. But "strategy" meant 4 months of meetings to approve ONE Instagram campaign. Legal has to review the font. Brand team hates the color. The product manager delays the launch. He misses the speed of the agency. He works 9-5, but he creates nothing.</p>
""",
        "data_table": """
<h3>Agency vs. Brand Side Metrics</h3>
<div class="table-container">
    <table class="reality-table">
        <thead>
            <tr>
                <th>Metric</th>
                <th>The Agency Life</th>
                <th>The Brand Life</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Speed</td>
                <td>Breakneck (Ship daily)</td>
                <td>Glacial (Ship quarterly)</td>
            </tr>
            <tr>
                <td>Politics</td>
                <td>Low (Just appease client)</td>
                <td>Game of Thrones level</td>
            </tr>
            <tr>
                <td>Skill Depth</td>
                <td>Wide (Many industries)</td>
                <td>Deep (One product line)</td>
            </tr>
        </tbody>
    </table>
</div>
""",
        "deep_dive": """
<h3>There is No Goldilocks Zone</h3>
<p>You either sell your soul for speed (Agency) or your sanity for stability (Brand). The "perfect" marketing role where you do cool creative work, get paid well, and leave at 5 PM does not exist in 2026.</p>
"""
    },
    23: { # American Dream
        "case_study": """
<h3>Case Study: The H1B Hostage</h3>
<p>Rahul makes $140,000 in Seattle. Sounds amazing (₹1.1 Crore!).</p>
<p>But he hasn't visited his parents in India for 4 years because his visa stamping is pending. If he gets laid off (like 12,000 others this month), he has 60 days to pack his entire life and leave. Ideally, he is rich. Legally, he is a second-class citizen with a countdown timer on his head.</p>
""",
        "data_table": """
<h3>The Purchasing Power Parity (PPP) Lie</h3>
<div class="table-container">
    <table class="reality-table">
        <thead>
            <tr>
                <th>Item</th>
                <th>India (₹30 LPA)</th>
                <th>USA ($120k)</th>
                <th>Winner?</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Rent (City Center)</td>
                <td>₹40k (15% of income)</td>
                <td>$3k (45% of income)</td>
                <td>India</td>
            </tr>
            <tr>
                <td>Domestic Help</td>
                <td>₹10k (Available)</td>
                <td>$0 (Unaffordable)</td>
                <td>India</td>
            </tr>
            <tr>
                <td>Healthcare</td>
                <td>Cheap/Insurance</td>
                <td>One ER visit = Bankruptcy</td>
                <td>India</td>
            </tr>
            <tr>
                <td>Tech/Cars</td>
                <td>Expensive</td>
                <td>Cheap</td>
                <td>USA</td>
            </tr>
        </tbody>
    </table>
</div>
""",
        "deep_dive": """
<h3>The "Golden Cage"</h3>
<p>The US works if you intend to optimize for savings rate and exit. If you intend to optimize for lifestyle *quality*, the equation has flipped in the last decade. A Senior Dev in Bangalore lives a more luxurious life than a Senior Dev in the Bay Area, purely due to service availability (cooks, drivers, help).</p>
"""
    },
    25: { # Remote Work
        "case_study": """
<h3>Case Study: The Invisible Employee</h3>
<p>Sneha works remotely for a US startup from Jaipur. She earns in dollars. Great?</p>
<p>She works 6 PM to 3 AM IST. Her social life is dead. Her parents don't understand why she sleeps till noon. At work, she was passed over for promotion because the other guy visits the SF office twice a week and has "face time" with the boss. She is a highly paid freelancer with no career ladder.</p>
""",
        "data_table": """
<h3>Remote vs. Office Trade-offs</h3>
<div class="table-container">
    <table class="reality-table">
        <thead>
            <tr>
                <th>Category</th>
                <th>Remote (Global)</th>
                <th>Hybrid (Local)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Salary</td>
                <td>High (Arbitrage)</td>
                <td>Market Standard</td>
            </tr>
            <tr>
                <td>Career Growth</td>
                <td>Capped (Out of sight)</td>
                <td>Normal</td>
            </tr>
            <tr>
                <td>Mental Health</td>
                <td>Isolation Risk</td>
                <td>Commute Stress</td>
            </tr>
        </tbody>
    </table>
</div>
""",
        "deep_dive": """
<h3>The "Overemployed" Secret</h3>
<p>The only real winners in the remote game are those running two jobs (r/overemployed). If you are doing one reliable remote job, you are likely underpaid relative to the value you create, or you are trading career growth for location freedom. It's a fair trade, but admit it's a trade.</p>
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
