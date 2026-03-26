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
slug = "the-ux-design-reality-india-ui-factory" # Long-form, trust signal
title = "The UX Design Reality: You Are Not a Researcher, You Are a UI Factory"
cat_name = "Career Reality Checks" # Same primary category

# Fetch Author
author = Author.objects.get(name="P. Mishra")
category, _ = Category.objects.get_or_create(name=cat_name, defaults={"slug": "career-reality-checks", "order": 1})

# ==========================================
# VISUAL DATA (HTML TABLE)
# ==========================================
salary_table_html = """
<div style="margin-top: 3rem; margin-bottom: 2rem;">
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 25%">Role Focus</th>
            <th style="width: 25%">Typical Title</th>
            <th style="width: 30%">Reality (LPA)</th>
            <th style="width: 20%">Market Demand</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Visual / UI</td>
            <td>Product Designer</td>
            <td>
                8.0 - 20.0
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 60%"></div></div>
            </td>
            <td>High</td>
        </tr>
        <tr>
            <td>UX / Research</td>
            <td>UX Researcher</td>
            <td>
                12.0 - 25.0
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 75%"></div></div>
            </td>
            <td>Very Low (Rare)</td>
        </tr>
        <tr>
            <td>The Unicorn</td>
            <td>Lead Designer</td>
            <td>
                30.0 - 50.0
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 90%; background: #666;"></div></div>
            </td>
            <td>Medium</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*Data reflects Indian Startup & Product Ecosystem (2024-25).</p>
</div>
"""

# ==========================================
# EDITORIAL PROSE (DRAFTED FOR "LOCK")
# ==========================================

target_persona = """
<p>This article is written for the creative professionals who entered the tech industry expecting a studio, but found a factory.</p>

<p>Typically, you are:</p>
<ul>
<li>Transitioning from Graphic Design, Architecture, or NIFT/NID</li>
<li>A bootcamp graduate who fell in love with "Human-Computer Interaction"</li>
<li>Or a "Product Designer" with 3 years of experience who mainly moves rectangles in Figma</li>
</ul>

<p>You care about empathy, user journeys, and solving deep systemic problems.</p>
<p>But your day-to-day work feels largely like high-speed decoration.</p>

<p>If you find yourself arguing about button border-radius more often than you discuss user needs,<br>
if your "research" budget is zero,<br>
and if you feel like a pair of hands for a Product Manager who already decided the solution —</p>

<p>this article is for you.</p>
"""

common_expectation = """
<p>The promise of UX Design is seductive.</p>

<p><strong>"You will be the voice of the user."</strong></p>

<p>Courses and influencers sell a vision where Designers are strategic partners. You expect to spend weeks in discovery, interviewing users, mapping affinities, and testing prototypes. You believe that "Good Design" is about the process, not just the output.</p>

<p>You expect to be valued for your <em>thinking</em>, not just your tool proficiency.</p>

<p>The expectation is that valid research will always trump an opinion. That if you can prove a user struggles with a flow, the business will pause and fix it.</p>

<p>You assume that the industry differentiates between a "UI Designer" (who makes it pretty) and a "UX Designer" (who makes it work).</p>
"""

actual_reality = """
<p>The reality in 90% of Indian companies is that there is no "UX". There is only fast UI.</p>

<p>Most startups and even mid-sized product companies do not want a Researcher. They want a <strong>Full-Stack Visualizer</strong>.</p>

<p>They want someone who can:</p>
<ul>
<li>Take a rough wireframe from a PM</li>
<li>Make it look like Cred, Airbnb, or Uber</li>
<li>And hand it off to developers by Friday</li>
</ul>

<p>The "Discovery Phase" you learned about? It usually happens in the CEO’s shower. By the time the ticket reaches you, the solution is already decided. Your job is not to question <em>why</em> we are building it, but to determine <em>how</em> it looks.</p>

<p>This is the <strong>UI Factory</strong>.</p>

<p>You are measured on speed and aesthetics. If you try to slow down the process to conduct interviews, you are seen as a bottleneck.</p>
<p>The feedback you get is rarely about usability ("Is this clear?").<br>
It is almost always subjective ("Can you make it pop?", "I don't like this shade of blue", "Copy what Swiggy did").</p>

<p>You realize that "Empathy" is a marketing term, while "Conversion Rate" is the religion.</p>
"""

salary_prose = """
<p>Financially, Design is lucrative, but the hierarchy is brutal.</p>

<p>Entry-level salaries are often depressed because the supply of bootcamp graduates is endless. Everyone has the same case study (a food delivery app or a pet adoption app).</p>

<p>To break out of the ₹6–8 LPA bucket, you must deliver <strong>Business Impact</strong>, not just Polish.</p>

<p>The market pays a premium for "Product Designers" who understand logic, edge cases, and developer constraints. It pays very little for "Pure Researchers" because most Indian companies don't believe they have a research problem—they believe they have an execution problem.</p>

<p>The ceiling is high (₹50 LPA+), but it is reserved for those who stop acting like artists and start acting like Architects.</p>
"""
salary_reality = salary_prose + salary_table_html

stuck_point = """
<p>Most designers get stuck in the <strong>Dribbble Trap</strong>.</p>

<p>Because they feel undervalued at work, they overcompensate by making beautiful, impractical concepts on social media. They redesign Netflix or Spotify with splashy gradients and impossible interactions.</p>

<p>This builds a following, but it hurts their career.</p>

<p>Senior Hiring Managers look at these portfolios and see "risk". They see a designer who doesn't understand constraints, data density, or technical feasibility.</p>

<p>You get stuck because you keep refining your <strong>Craft</strong> (UI skills) while the business wants you to refine your <strong>Context</strong> (Domain understanding).</p>

<p>You become the "Figma Wizard" — the person who is fast, but never invited to the strategy meeting.</p>
"""

who_should_avoid = """
<p><strong>This career works for:</strong></p>
<p>Visual thinkers who enjoy high-paced problem solving. If you like the "craft" of UI—systems, typography, and seeing things built—you will thrive. The instant gratification of shipping a screen is real.</p>

<p><strong>This career destroys:</strong></p>
<p>Purist Researchers and Artists. If you need 4 weeks to validate a hypothesis before opening Figma, you will be miserable. If you view your design as "Art" that shouldn't be compromised by business metrics, you will burn out within 2 years.</p>
"""

verdict = """
<p>The "UX" label is mostly a lie. Accept that you are a <strong>Digital Product Designer</strong>.</p>

<p>This is not a bad thing. It is a powerful role. But it requires a shift in mindset:</p>
<ul>
<li>Your canvas is not the screen;, it is the Business Logic.</li>
<li>Your medium is not pixels; it is Developer Constraints.</li>
<li>Your goal is not delight; it is Clarity.</li>
</ul>

<p>Stop waiting for permission to do research. Do "Guerrilla Research".</p>
<p>Stop complaining about the process. Fix the outcome.</p>
<p>The moment you stop fighting the reality of the business is the moment you start leading it.</p>
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
        "meta_title": "The UX Design Reality: You Are Not a Researcher",
        "meta_description": "The truth about UX Design jobs in India. Why most roles are actually UI production, and why research budgets don't exist.",
        "published_at": timezone.now(),
        "last_reality_check": datetime.date.today(),
    }
)

print(f"Published Draft: {title}")
