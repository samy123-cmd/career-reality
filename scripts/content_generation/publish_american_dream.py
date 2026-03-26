
import os
import django
from django.utils.text import slugify

# Setup Django environment
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Article, Author, Category

def run():
    # 1. Author
    author, _ = Author.objects.update_or_create(
        name="Shiv Mishra",
        defaults={
            "bio": "Tech industry observer. Writes about the uncomfortable truths of engineering careers.",
            "linkedin_url": "https://www.linkedin.com/in/shivmishra1408" 
        }
    )

    # 2. Category
    category, _ = Category.objects.get_or_create(name="Software Engineering")

    # 3. Article Content
    title = "The American Dream Indian Engineers Are Still Chasing — and Why It’s Getting Harder"
    slug = slugify("american-dream-indian-engineers")
    
    # Content Blocks
    target_persona = "Mid-level Devs (3-8 YOE), MS Aspirants, H1B Chasers."
    
    common_expectation = """
    <p>The playbook has been unchanged since 2010:</p>
    <ul>
        <li>Take a 40 Lakh loan.</li>
        <li>Do an MS in CS from a Tier-2 US University.</li>
        <li>Land a FAANG job paying $150k+.</li>
        <li>Buy a Tesla, post photos on Instagram.</li>
        <li>Get a Green Card, buy a house, retire rich.</li>
    </ul>
    <p>It’s viewed as the only escape velocity from Indian mediocrity.</p>
    """

    actual_reality = """
    <p>The math has fundamentally broken. The "Golden Era" (2010-2019) is over.</p>
    
    <h3>1. The H1B Lottery is a Casino</h3>
    <p>Your chances are no longer 50/50. With 700k+ registrations for 85k spots, the probability is closer to <strong>10-15%</strong>. Even with a Master's cap. You are betting a 40L loan on a dice roll where the house always wins.</p>

    <h3>2. $150k is the new $100k</h3>
    <p>Inflation in tech hubs (Bay Area, NYC, Seattle) has eroded the "savings potential" that made the US attractive. Rent for a 1BHK in San Jose is $3,200. After taxes (35%+), 401k, and basic living, your "huge savings" are remarkably average unless you live like a student for decade.</p>

    <h3>3. The "Visa Ghetto"</h3>
    <p>You cannot switch jobs easily. You cannot start a startup. You cannot take a break. If you leverage yourself with a mortgage, you are one layoff email away from being deported in 60 days. This psychological toll is rarely priced in by consultancies selling you the dream.</p>
    """

    salary_reality = """
    <div class="editorial-table-wrapper">
        <table class="editorial-table">
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>San Francisco ($160k)</th>
                    <th>Bangalore (₹50 LPA)</th>
                    <th>Verdict</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Take Home (Monthly)</strong></td>
                    <td>~$9,200</td>
                    <td>~₹3.1 Lakhs</td>
                    <td>US wins (Absolute)</td>
                </tr>
                <tr>
                    <td><strong>Rent (1BHK/Good Area)</strong></td>
                    <td>$3,200 (35%)</td>
                    <td>₹45,000 (14%)</td>
                    <td>India wins (Ratio)</td>
                </tr>
                <tr>
                    <td><strong>Savings (PPP Adjusted)</strong></td>
                    <td>High, but vulnerable</td>
                    <td>High, and secure</td>
                    <td>Tie</td>
                </tr>
                <tr>
                    <td><strong>Job Security</strong></td>
                    <td>Zero (At-will + Visa)</td>
                    <td>Moderate</td>
                    <td>India Wins</td>
                </tr>
            </tbody>
        </table>
        <p class="caption">Note: $160k in SF feels like ₹30 LPA in Bangalore lifestyle-wise, but savings in USD still accumulate faster—if you survive.</p>
    </div>
    """

    stuck_point = """
    <p><strong>The " sunk cost" trap.</strong></p>
    <p>You pay off the loan in 3 years. But by then, you’ve waited 3 years for green card priority dates that moved 2 months. You have kids who are US citizens. Moving back feels like "failure", but staying feels like anxiety. You are stuck in a golden cage, waiting for a piece of paper that might arrive in 2045.</p>
    """

    who_should_avoid = """
    <ul>
        <li><strong>Risk Averse People:</strong> If you panic at uncertainty, the H1B life will destroy your mental health.</li>
        <li><strong>Mediocre Engineers:</strong> The bar for entry is higher. Average devs are the first to be cut and the hardest to re-hire in 60 days.</li>
        <li><strong>Those seeking "Work-Life Balance":</strong> Being on a visa means you often have to work twice as hard to prove you are "essential".</li>
    </ul>
    """

    verdict = """
    <p><strong>Go for the adventure, not the safety.</strong></p>
    <p>If you want to work on cutting-edge tech, build a global network, and experience a different culture—go. The US tech ecosystem is still unmatched.</p>
    <p>But if you are going mainly to "escape" or "get rich safe", the math doesn't hold up like it used to. The Great Indian Dream needs a firmware update.</p>
    """

    today = django.utils.timezone.now()
    
    # 4. Save
    article, created = Article.objects.update_or_create(
        slug=slug,
        defaults={
            "title": title,
            "author": author,
            "category": category,
            "target_persona": target_persona,
            "common_expectation": common_expectation,
            "actual_reality": actual_reality,
            "salary_reality": salary_reality,
            "stuck_point": stuck_point,
            "who_should_avoid": who_should_avoid,
            "verdict": verdict,
            "meta_title": "The American Dream for Indian Engineers: A Reality Check",
            "meta_description": "Is the MS in US pathway still worth it? A brutally honest look at H1B odds, $150k salaries vs cost of living, and the visa trap.",
            "status": "published",
            "published_at": today,
            "last_reality_check": today.date()
        }
    )

    print(f"Successfully published: {article.title}")

if __name__ == "__main__":
    run()
