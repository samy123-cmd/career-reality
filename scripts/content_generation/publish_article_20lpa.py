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

# ==========================================
# CONFIGURATION
# ==========================================
slug = "what-20-lpa-actually-feels-like-india-purchasing-power" # Long-form, trust signal
title = "What ₹20 LPA Actually Feels Like in India"
cat_name = "Financial Reality" # Distinct but authoritative

# Fetch Author
author = Author.objects.get(name="P. Mishra")
category, _ = Category.objects.get_or_create(name=cat_name, defaults={"slug": "financial-reality", "order": 2})

# ==========================================
# VISUAL DATA (HTML TABLE)
# ==========================================
salary_table_html = """
<div style="margin-top: 3rem; margin-bottom: 2rem;">
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 25%">CTC</th>
            <th style="width: 25%">Monthly In-Hand</th>
            <th style="width: 50%">Real Lifestyle Tier</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>₹10 LPA</td>
            <td>₹70,000</td>
            <td>
                Survival (Metro)
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 30%"></div></div>
            </td>
        </tr>
        <tr>
            <td>₹20 LPA</td>
            <td>₹1,18,000</td>
            <td>
                Comfortable Middle
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 60%"></div></div>
            </td>
        </tr>
        <tr>
            <td>₹50 LPA</td>
            <td>₹2,80,000</td>
            <td>
                Wealth Starts Here
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 100%; background: #666;"></div></div>
            </td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*Estimates based on New Regime Tax + Metro City Cost of Living (2025).</p>
</div>
"""

# ==========================================
# EDITORIAL PROSE (LOCKED)
# ==========================================

target_persona = """
<p>This article is written for the young professional who has just crossed, or is about to cross, the magical "₹20 Lakhs Per Annum" milestone.</p>

<p>Typically, you are:</p>
<ul>
<li>24–28 years old</li>
<li>Living in Bengaluru, Mumbai, or Gurugram</li>
<li>The first in your family to earn this kind of money at this age</li>
</ul>

<p>You grew up believing that ₹1.5 Lakhs a month was "Rich People Money". You thought it meant business class flights, a luxury car, and zero financial stress.</p>

<p>But now that the money is hitting your account, you feel confused.</p>

<p>Your bank balance isn't growing as fast as you expected.<br>
You still check the menu prices before ordering.<br>
And buying a house feels just as impossible as it did when you were earning ₹5 LPA.</p>

<p>If you are wondering where the money is going, this article is for you.</p>
"""

common_expectation = """
<p>The "20 LPA" number carries a heavy cultural weight in India.</p>

<p>For decades, it was the benchmark of the upper-middle class. It signaled arrival. The expectation is that crossing this threshold grants you <strong>Financial Escape Velocity</strong>.</p>

<p>You expect to:</p>
<ul>
<li>Save 50% of your income effortlessly</li>
<li>Buy a premium car (Creta/Compass/german sedan) without stress</li>
<li>Travel internationally once a year</li>
<li>And still have enough left over to invest heavily</li>
</ul>

<p>The mental model is simple: <em>"My expenses are ₹40k. If I earn ₹1.5L, I will save ₹1.1L every month."</em></p>

<p>You believe this surplus is guaranteed.</p>
"""

actual_reality = """
<p>The reality is that ₹20 LPA is the new ₹10 LPA.</p>

<p>This is not an exaggeration. It is a function of <strong>Lifestyle Inflation</strong> and <strong>Fiscal Drag</strong>.</p>

<p>First, the math. On ₹20 LPA, your monthly in-hand (under the new tax regime) is roughly <strong>₹1.18 Lakhs</strong>.</p>

<p>It is not ₹1.6L. The government takes its share first.</p>

<p>Then, the "Metro Tax" kicks in:</p>
<ul>
<li><strong>Rent in a Decent Society:</strong> ₹35,000 (1BHK/Sharing in HSR/Bandra/Cyber City)</li>
<li><strong>Maid/Cook/Laundry:</strong> ₹8,000</li>
<li><strong>Food & Ordering:</strong> ₹15,000 (You stop cooking because you "work hard")</li>
<li><strong>Commute (Uber/Cab):</strong> ₹10,000</li>
<li><strong>Socializing/Weekends:</strong> ₹15,000</li>
</ul>

<p><strong>Total Fixed Burn: ₹83,000.</strong></p>

<p>You are left with ₹35,000. </p>

<p>That is decent. But it is not "Rich".</p>
<p>One iPhone EMI (which you bought to celebrate the job), one trip to Vietnam, or one medical emergency in the family wipes out 6 months of savings.</p>

<p>You are technically earning in the top 5% of India, but you are living a paycheck-to-paycheck existence wrapped in better brands.</p>
"""

salary_prose = """
<p>The biggest trap at this level is the illusion of Purchasing Power.</p>

<p>Because the cash flow is high, banks line up to offer you credit cards and loans. You feel wealthy because you have <strong>Access to Debt</strong>, not because you have <strong>Assets</strong>.</p>

<p>You qualify for a car loan of ₹15 Lakhs. You qualify for a home loan of ₹80 Lakhs.</p>

<p>But servicing those loans on a ₹1.18L salary is suicide.</p>

<p>The chart below breaks down the purchasing power tiers. Notice how the "Comfortable Middle" has a ceiling that is much lower than you think.</p>
"""
salary_reality = salary_prose + salary_table_html

stuck_point = """
<p>Most people get stuck here because of <strong>Lifestyle Creep</strong>.</p>

<p>The moment the salary hike letter arrives, the standard of living upgrades instantly—often <em>before</em> the first paycheck hits.</p>

<p>You move to a gated society with a pool you never use.<br>
You switch from shopping at Myntra to Zara.<br>
You switch from Old Monk to Single Malt.</p>

<p>Your "Needs" don't change, but your "Standards" do.</p>

<p>You tell yourself, <em>"I work hard, I deserve this."</em></p>

<p>This is the <strong>Golden Hamster Wheel</strong>. You run faster (earn more), but the wheel spins faster (spend more). You never actually move forward.</p>
"""

who_should_avoid = """
<p><strong>This cycle works for:</strong></p>
<p>People who prioritize experiences over security. If your goal is to enjoy your 20s, travel, and live well, spending your entire paycheck is a valid choice. Just don't call it "wealth building".</p>

<p><strong>This cycle destroys:</strong></p>
<p>People who want Freedom. If you want to retire early, start a business, or take a career break, you need <strong>Liquid Cash</strong>, not a high credit score. If you lock yourself into high EMIs at 20 LPA, you are signing a contract to stay employed in a job you might hate for the next 15 years.</p>
"""

verdict = """
<p>Stop looking at your CTC. It is a vanity metric.</p>

<p>The only number that matters is your <strong>Savings Rate</strong>.</p>

<p>Real wealth in India (defined as freedom from anxiety) starts when you can save <strong>50% of your in-hand income</strong> without feeling deprived.</p>

<p>If you earn ₹20 LPA and save ₹10k a month, you are poorer than the guy earning ₹8 LPA and saving ₹20k.</p>

<p>Don't upgrade your life. Upgrade your savings.<br>
Stay "Poor" for 3 more years. That is the only way to become actually Rich.</p>
"""

# ==========================================
# 5. PUBLISH
# ==========================================
Article.objects.update_or_create(
    slug=slug,
    defaults={
        "title": title,
        "author": author,
        "category": category,
        "status": "published",
        "target_persona": target_persona,
        "who_should_avoid": who_should_avoid,
        "common_expectation": common_expectation, 
        "actual_reality": actual_reality,
        "salary_reality": salary_reality,
        "stuck_point": stuck_point,
        "verdict": verdict,
        "meta_title": "What ₹20 LPA Actually Feels Like: The Middle Class Trap",
        "meta_description": "Why earning ₹20 Lakhs in India doesn't make you rich anymore. A breakdown of taxes, metro city rent, and lifestyle inflation.",
        "published_at": timezone.now(),
        "last_reality_check": datetime.date.today(),
    }
)

print(f"Published Draft: {title}")
