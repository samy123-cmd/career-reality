import os
import django
import datetime
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Author, Category, Article

# Common Setup
author = Author.objects.get(name="P. Mishra")

# ==============================================================================
# ARTICLE 1: UPSKILLING TRAP
# ==============================================================================
slug_1 = "why-upskilling-stops-working-career-trap"
title_1 = "Why 'Upskilling' Stops Working After a Point"
cat_1, _ = Category.objects.get_or_create(name="Career Strategy", defaults={"slug": "career-strategy"})

table_1 = """
<div style="margin-top: 3rem; margin-bottom: 2rem;">
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 30%">Career Stage</th>
            <th style="width: 40%">Impact of Courses</th>
            <th style="width: 30%">Real Driver of Growth</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Years 0-3</td>
            <td>
                High (Critical)
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 90%"></div></div>
            </td>
            <td>Hard Skills</td>
        </tr>
        <tr>
            <td>Years 4-10</td>
            <td>
                Low (Diminishing)
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 30%"></div></div>
            </td>
            <td>Execution & Outcome</td>
        </tr>
        <tr>
            <td>Years 10+</td>
            <td>
                Zero (Irrelevant)
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 5%; background: #666;"></div></div>
            </td>
            <td>Judgment & Politics</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*The "Course Collector" curve flattens rapidly.</p>
</div>
"""

persona_1 = """
<p>This article is for the "Course Collector".</p>

<p>You have 25 certifications on your LinkedIn profile. Your weekend routine involves watching Udemy tutorials at 2x speed. You feel a compulsive, anxious need to learn the "next big thing" — currently Generative AI, Rust, or Blockchain.</p>

<p>You believe that you are one skill away from being successful.</p>

<p>Yet, your career velocity has slowed down. You know more tools than your manager, but he gets the promotion. You are technically superior to the "political" guy, but he gets the budget.</p>

<p>If you think the solution is <em>one more certificate</em>, this article is your intervention.</p>
"""

expectation_1 = """
<p>We are sold a simple lie: <strong>Knowledge = Power.</strong></p>

<p>The EdTech industry is built on this insecurity. They tell you that if you don't learn AI, you will be obsolete. They sell you "Masterclasses" that promise to make you an Architect in 6 weekends.</p>

<p>You expect that upgrading your skills will automatically upgrade your title.</p>

<p>You treat your brain like a hard drive: <em>"If I just add more data (skills), my value goes up."</em></p>

<p>You believe that the person who knows the most syntax wins.</p>
"""

reality_1 = """
<p>The reality is that <strong>Certifications are the adult equivalent of gold stars.</strong></p>

<p>They comfort you, but they don't convince the market.</p>

<p>In the first 3 years of your career, skills matter immensely. You need to know how to code, design, or write. The ROI on learning is high.</p>

<p>But after Year 4, the game changes. No CTO hires a Senior Architect because they have a Udemy certificate. They hire them because they know <em>when not to use</em> a technology.</p>

<p>That is called <strong>Judgment</strong>. And you cannot learn Judgment in a Bootcamp.</p>

<p>Upskilling often becomes a procrastination tool. It is a safe way to feel productive without doing the scary work of solving messy, ambiguous business problems.</p>

<p>You are hiding behind tutorials because you are afraid of production.</p>
"""

salary_prose_1 = """
<p>The market pays for <strong>Outcomes</strong>, not Inputs.</p>

<p>Your "knowledge" of Rust is an Input. A system that scales to 1M users at 50ms latency is an Outcome.</p>

<p>If you can deliver the Outcome without knowing the "coolest" tech, you win. If you know the tech but ship nothing, you lose.</p>

<p>Notice how the value of pure "Learning" crashes as you get senior:</p>
"""
salary_reality_1 = salary_prose_1 + table_1

stuck_1 = """
<p>You get stuck in the <strong>Tutorial Loop</strong>.</p>

<p>You finish a course, feel a dopamine hit ("I learned something!"), and then... do nothing with it. Two months later, you forget it. So you buy another course.</p>

<p>You are building a library of theoretical knowledge that is rotting on the shelf.</p>

<p>Meanwhile, the "Average" developer who picked one boring stack and spent 5 years solving real business problems is now your Team Lead. He didn't learn the new framework. He just shipped the product.</p>
"""

avoid_1 = """
<p><strong>This mindset works for:</strong> Actual R&D Researchers. If your job is literally to push the boundary of computer science, keep studying. For everyone else, it is a trap.</p>

<p><strong>This mindset destroys:</strong> Effectual Engineers. If you need a tutorial to start a project, you are not an Engineer; you are a typist.</p>
"""

verdict_1 = """
<p><strong>Stop taking courses. Start shipping.</strong></p>

<p>Delete your Udemy bookmarks. Cancel the weekend workshop.</p>

<p>Pick a problem at work that scares you. A legacy codebase nobody touches. A slow database query. A broken process.</p>

<p>Fix it. Struggle with it. Google it when you get stuck.</p>

<p>Real learning happens in the fire of Production, not in the safety of a Sandbox. You don't need more skills. You need more scars.</p>
"""

Article.objects.update_or_create(
    slug=slug_1,
    defaults={
        "title": title_1, "author": author, "category": cat_1, "status": "published",
        "target_persona": persona_1, "who_should_avoid": avoid_1, "common_expectation": expectation_1,
        "actual_reality": reality_1, "salary_reality": salary_reality_1, "stuck_point": stuck_1, "verdict": verdict_1,
        "meta_title": "Why 'Upskilling' Stops Working: The Tutorial Trap",
        "meta_description": "Why certifications lose value after 3 years. The shift from skills to judgment in seasoned careers.",
        "published_at": timezone.now(), "last_reality_check": datetime.date.today()
    }
)
print(f"Published Savage: {title_1}")


# ==============================================================================
# ARTICLE 2: IT SERVICES COST
# ==============================================================================
slug_2 = "hidden-cost-of-staying-in-it-services-too-long"
title_2 = "The Hidden Cost of Staying in IT Services Too Long"
cat_2 = cat_1 # Career Strategy

table_2 = """
<div style="margin-top: 3rem; margin-bottom: 2rem;">
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 25%">Tenure</th>
            <th style="width: 30%">Service Co Hike</th>
            <th style="width: 45%">Product Market Value</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Year 0-2</td>
            <td>3-5%</td>
            <td>
                High (Transferable)
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 80%"></div></div>
            </td>
        </tr>
        <tr>
            <td>Year 5</td>
            <td>5-8%</td>
            <td>
                Declining (Legacy Trap)
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 50%"></div></div>
            </td>
        </tr>
        <tr>
            <td>Year 10</td>
            <td>Stagnant</td>
            <td>
                Unhirable
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 10%; background: #d93025;"></div></div>
            </td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*The "Lifer" penalty kicks in hard after Year 6.</p>
</div>
"""

persona_2 = """
<p>This article is for the "Safe Player".</p>

<p>You work at TCS, Infosys, Wipro, Accenture, or Cognizant. You have been there for 6+ years. Your parents love your job because it is "stable".</p>

<p>You are comfortable. The campus is nice. The bench time is relaxing. You haven't given an interview in 4 years because the thought of LeetCode terrifies you.</p>

<p>But you look at your Product company peers earning 3x your salary and wonder: <em>"What did I do wrong?"</em></p>
"""

expectation_2 = """
<p>You believe in <strong>Loyalty</strong>.</p>

<p>You think: <em>"If I stick around, I will eventually become a Manager/Delivery Head. The On-Site opportunity is just around the corner."</em></p>

<p>You believe that "Experience" is measured in years. You think that 10 years at Infosys = 10 Years of Experience.</p>

<p>You think the "brand name" of a massive MNC protects you from irrelevance.</p>
"""

reality_2 = """
<p>The brutal truth: <strong>You are not an Engineer; you are a Row in an Excel Sheet.</strong></p>

<p>Service companies optimize for 'Billability', not 'Capability'. Their business model is to sell you to a client at $40/hour while paying you $5/hour.</p>

<p>To maximize margin, they <em>must</em> keep you on established, legacy tech (Java 8, older .NET, Mainframes, Support). Innovation hurts their margins because it requires training.</p>

<p><strong>10 Years at Infosys is often just 1 Year of Experience, repeated 10 times.</strong></p>

<p>The "On-Site" carrot is a manipulation tactic. Managers dangle the US/Europe visa to keep you cheap. You wait 4 years for a visa that never comes, while your market skills rot. By the time you realize it, you are too old to learn React.</p>
"""

salary_prose_2 = """
<p>The longer you stay, the more <strong>Unhirable</strong> you become.</p>

<p>Product companies (Uber, Amazon, Swiggy, Zerodha) do not care about your 'Domain Knowledge' of a specific insurance client's legacy system.</p>

<p>They care about Problem Solving, System Design, and Modern Stacks. Every year you spend maintaining a legacy Struts application is a year you are falling behind the industry standard.</p>

<p>See the "Lifer Curve" below:</p>
"""
salary_reality_2 = salary_prose_2 + table_2

stuck_2 = """
<p>You get stuck because of <strong>The Golden Handcuffs of Mediocrity</strong>.</p>

<p>You are paid slightly above market <em>for your actual skill level</em> (which has atrophied), but effectively below market for your <em>years of experience</em>.</p>

<p>To switch, you would have to accept that you are technically a Junior compared to a 4-year experience Product Engineer.</p>

<p>Your ego won't let you compete with a 24-year-old. So you stay. And the trap tightens.</p>
"""

avoid_2 = """
<p><strong>This path works for:</strong> People who have zero interest in technology and view a job purely as a paycheck to fund a low-stress life. There is no shame in that, as long as you accept the low growth.</p>

<p><strong>This path destroys:</strong> Ambitious Technologists. If you care about your craft, get out before Year 3. Run.</p>
"""

verdict_2 = """
<p><strong>Leave before Year 6.</strong></p>

<p>If you are past Year 6, you are in the Danger Zone. You need to aggressively upskill (night and weekends) and take a "downgrade" in title to enter a Product firm.</p>

<p>If you stay for 10 years, accept that you are a "Lifer". Stop complaining about the salary. You paid for Safety with Stagnation.</p>
"""

Article.objects.update_or_create(
    slug=slug_2,
    defaults={
        "title": title_2, "author": author, "category": cat_2, "status": "published",
        "target_persona": persona_2, "who_should_avoid": avoid_2, "common_expectation": expectation_2,
        "actual_reality": reality_2, "salary_reality": salary_reality_2, "stuck_point": stuck_2, "verdict": verdict_2,
        "meta_title": "The Hidden Cost of Staying in IT Services Too Long",
        "meta_description": "Why staying in WITCH companies (TCS, Infosys, etc.) for more than 5 years destroys your market value.",
        "published_at": timezone.now(), "last_reality_check": datetime.date.today()
    }
)
print(f"Published Savage: {title_2}")


# ==============================================================================
# ARTICLE 3: CAREER SWITCHING
# ==============================================================================
slug_3 = "career-switching-after-30-the-brutal-truth"
title_3 = "Career Switching After 30: The Trade-Offs Nobody Posts About"
cat_3 = cat_1 # Career Strategy

table_3 = """
<div style="margin-top: 3rem; margin-bottom: 2rem;">
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 30%">Path</th>
            <th style="width: 40%">Financial Impact</th>
            <th style="width: 30%">Ego Impact</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Stay (Safe)</td>
            <td>
                Slow Growth
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 50%; background: #ccc;"></div></div>
            </td>
            <td>Low (Comfort)</td>
        </tr>
        <tr>
            <td>Switch (Pivot)</td>
            <td>
                -30% to -50% Drop
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 20%; background: #d93025;"></div></div>
            </td>
            <td>Extreme (Humility)</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*Transferable skills do not pay rent in Year 1.</p>
</div>
"""

persona_3 = """
<p>This article is for the "Pivot Dreamer".</p>

<p>You are 30+ years old. You spent 8 years in Sales, Operations, or Support. You hate it.</p>

<p>You see your Tech friends working remotely and earning double your salary. You see the Instagram ads for "Coding Bootcamps" that promise a new life.</p>

<p>You think: <em>"I will do a 6-month Bootcamp, switch to Product/Coding, and my life will change."</em></p>

<p>You are looking for a reset button on your career. But you have a mortgage, a spouse, and a lifestyle that costs ₹1L a month.</p>
"""

expectation_3 = """
<p>You expect your <strong>"Transferable Skills"</strong> to save you.</p>

<p>You tell yourself: <em>"I have maturity. I have communication skills. I know how business works. Surely that counts for something?"</em></p>

<p>You expect to enter the new field at a "Mid-Senior" level because, well, you are 32 years old.</p>

<p>You expect a lateral salary move, or maybe a small dip (10-20%).</p>
"""

reality_3 = """
<p>The market does not care about your past life.</p>

<p>Your 8 years of 'Sales Experience' is worth <strong>Zero</strong> to the Engineering Manager. It might even be negative (bad habits).</p>

<p>If you switch at 30, you are a <strong>Junior</strong> again.</p>

<p>You will report to a 24-year-old Team Lead. She will be faster than you. She will know more than you. She will correct your code and your documents.</p>

<p>And you will be paid like a Junior (₹6-10 LPA).</p>

<p>Can your ego handle that? Can your Family handle that? Can your EMI handle that?</p>
"""

salary_prose_3 = """
<p>Career switching is not an arithmetic addition; it is a <strong>Geometric Reset</strong>.</p>

<p>You are trading short-term cash flow for long-term trajectory. But the "Valley of Death" in between is deep.</p>

<p>Most people cannot survive the dip. They run out of savings or patience within 12 months and retreat to their old industry.</p>
"""
salary_reality_3 = salary_prose_3 + table_3

stuck_3 = """
<p>You get stuck because of <strong>Ego Dissonance</strong>.</p>

<p>It is humiliating to be the oldest person in the room with the least authority. You will feel "Slow". You will feel "Stupid".</p>

<p>Your peers are becoming VPs while you are learning "What is an API?".</p>

<p>Most people quit the switch not because they can't learn the skill, but because they can't handle the status drop.</p>
"""

avoid_3 = """
<p><strong>Avoid if:</strong> Your identity is tied to your paycheck or title. If being "The Junior" makes you resentful, stay where you are.</p>

<p><strong>Do it if:</strong> You are playing a 20-year game. If you can eat 3 years of dirt to build a 20-year career you actually like, the math works.</p>
"""

verdict_3 = """
<p><strong>Kill your Ego.</strong></p>

<p>That is the only way this works. Walk into the new room assuming you know nothing. Respect the 23-year-olds who are teaching you.</p>

<p>And save 12 months of expenses before you jump. The market will not subsidize your learning curve.</p>
"""

Article.objects.update_or_create(
    slug=slug_3,
    defaults={
        "title": title_3, "author": author, "category": cat_2, "status": "published",
        "target_persona": persona_3, "who_should_avoid": avoid_3, "common_expectation": expectation_3,
        "actual_reality": reality_3, "salary_reality": salary_reality_3, "stuck_point": stuck_3, "verdict": verdict_3,
        "meta_title": "Career Switching After 30: The Trade-Offs Nobody Posts About",
        "meta_description": "The brutal reality of changing careers in India after 30. Salary cuts, ego management, and the long road.",
        "published_at": timezone.now(), "last_reality_check": datetime.date.today()
    }
)
print(f"Published Savage: {title_3}")

# Clean up old slugs to ensure uniqueness
Article.objects.filter(slug__in=[
    "why-upskilling-stops-working", "hidden-cost-it-services-india", "career-switching-after-30-india"
]).delete()
print("Cleaned up old drafts.")
