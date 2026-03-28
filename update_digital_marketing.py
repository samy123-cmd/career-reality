
import os
import django
from django.utils.text import slugify

# Setup Django environment
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

    # 2. Get Article
    slug = "digital-marketing-reality-india"
    
    # Content Blocks
    title = "Digital Marketing in India: The 'Creative' Trap That Pays in Peanuts"
    target_persona = "BBA/MBA Grads, 'Creative' Engineers, Agency Aspirants"
    
    common_expectation = """
    <p>The Instagram Reel dream:</p>
    <ul>
        <li>"I'll work in a cool cafe."</li>
        <li>"I'll make viral memes and get famous."</li>
        <li>"No coding, just vibes and creativity."</li>
        <li>"Start my own agency and make crores."</li>
    </ul>
    <p>It’s sold as the easy alternative to the IT grind.</p>
    """

    actual_reality = """
    <p><strong>It is a sweatshop with a MacBook.</strong></p>
    
    <h3>1. The "Agency" Meat Grinder</h3>
    <p>Most entrants join an agency. You will handle 5-8 clients simultaneously. You will spend 12 hours a day making "festival creatives" (Happy Diwali posts) that get 3 likes. Your boss will scream about "Reach" while paying you ₹18,000 per month.</p>

    <h3>2. Data > Creativity</h3>
    <p>Real money is in <strong>Performance Marketing</strong> (Facebook Ads, Google Ads, SEO). This is not creative; this is <strong>Math</strong>. It's spreadsheets, attribution models, pixel tracking, and bid optimization. If you hate numbers, you will stay poor.</p>

    <h3>3. The AI Threat is Real</h3>
    <p>Copywriting and Graphic Design (Canva wrappers) are being decimated by ChatGPT and Midjourney. The "creative" junior roles are vanishing. Only the strategists survive, and you can't be a strategist with 0 years of experience.</p>
    """

    salary_reality = """
    <div class="editorial-table-wrapper">
        <table class="editorial-table">
            <thead>
                <tr>
                    <th>Role / Level</th>
                    <th>Salary (Annual)</th>
                    <th>Reality</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Social Media Intern</strong></td>
                    <td>₹1.2L - ₹2L</td>
                    <td>Less than a Swiggy driver.</td>
                </tr>
                <tr>
                    <td><strong>Performance Marketer (3 YOE)</strong></td>
                    <td>₹6L - ₹10L</td>
                    <td>Decent, if you can prove ROAS.</td>
                </tr>
                <tr>
                    <td><strong>CMO / Head of Growth</strong></td>
                    <td>₹30L - ₹80L+</td>
                    <td>High stress. Measured on Revenue, not Likes.</td>
                </tr>
                <tr>
                    <td><strong>Agency Owner (Small)</strong></td>
                    <td>₹0 - ₹20L</td>
                    <td>Most fail in 18 months.</td>
                </tr>
            </tbody>
        </table>
        <p class="caption">Verdict: The ceiling is high, but the floor is in the basement.</p>
    </div>
    """

    stuck_point = """
    <p><strong>The "Generalist" Trap.</strong></p>
    <p>You know a little bit of SEO, a little bit of Instagram, and a little bit of Email. You are a "Jack of all trades" who is replaced by two cheap interns. To survive, you must niche down ruthlessly (e.g., "B2B SaaS PPC Expert") or become a Revenue Leader.</p>
    """

    who_should_avoid = """
    <ul>
        <li><strong>People who hate Numbers:</strong> Marketing is 70% Analytics today.</li>
        <li><strong>People who want 9-to-5:</strong> Social media never sleeps. Clients will text you on Sunday night because a link is broken.</li>
        <li><strong>Introverts:</strong> You have to sell your ideas constantly.</li>
    </ul>
    """

    verdict = """
    <p><strong>Learn to Sell, not just Post.</strong></p>
    <p>If you can spend ₹1 to make ₹5 for a business, you will be wealthy. If you just "manage communities" and "post content", you are a commodity.</p>
    <p>Don't be a "Digital Marketer". Be a <strong>Growth Engineer</strong> or a <strong>Revenue Specialist</strong>.</p>
    """

    # 4. Save
    article, created = Article.objects.update_or_create(
        slug=slug,
        defaults={
            "title": title,
            "author": author,
            # "category": category, # Keep existing category
            "target_persona": target_persona,
            "common_expectation": common_expectation,
            "actual_reality": actual_reality,
            "salary_reality": salary_reality,
            "stuck_point": stuck_point,
            "who_should_avoid": who_should_avoid,
            "verdict": verdict,
            "meta_title": "Digital Marketing Reality in India: Salaries, Agency Life, and burnout",
            "meta_description": "Thinking of a career in Digital Marketing? Read this before you join an agency. The truth about salaries, burnout, and why 'creative' is a trap.",
            # "status": "published", # Keep existing status
        }
    )

    print(f"Successfully updated: {article.title}")

if __name__ == "__main__":
    run()
