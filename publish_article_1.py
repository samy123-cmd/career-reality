import os
import django
import datetime
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Author, Category, Article

# 0. CLEANUP OLD SLUG (To avoid duplication)
old_slug = "7-year-career-plateau-india"
Article.objects.filter(slug=old_slug).delete()
print(f"Cleaned up old version: {old_slug}")

# 1. AUTHOR CONFIGURATION
author, _ = Author.objects.get_or_create(
    name="P. Mishra",
    defaults={
        "display_name": "P. Mishra",
        "bio": "Senior Editor. Independent Observer of Indian Tech Markets.",
        "linkedin_url": "https://linkedin.com/in/pmishra-reality",
        "is_active": True
    }
)

# 2. CATEGORY ASSIGNMENT (Locked: "Career Reality Checks")
cat_name = "Career Reality Checks"
category, _ = Category.objects.get_or_create(
    name=cat_name, 
    defaults={"slug": "career-reality-checks", "order": 1}
)

# 3. ARTICLE DATA (Locked Slug & Title)
slug = "the-7-year-career-plateau-nobody-warns-you-about"
title = "The 7-Year Career Plateau Nobody Warns You About"

# 4. CONTENT BLOCKS (LOCKED PROSE)
salary_table_html = """
<div style="margin-top: 3rem; margin-bottom: 2rem;">
<table class="editorial-table">
    <thead>
        <tr>
            <th style="width: 25%">Phase</th>
            <th style="width: 20%">Years</th>
            <th style="width: 30%">Realistic Pay (LPA)</th>
            <th style="width: 25%">Dominant Feeling</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>The Rise</td>
            <td>0-4 Yrs</td>
            <td>
                6.0 - 18.0
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 30%"></div></div>
            </td>
            <td>Euphoria / Growth</td>
        </tr>
        <tr>
            <td>The Senior</td>
            <td>5-7 Yrs</td>
            <td>
                18.0 - 35.0
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 60%"></div></div>
            </td>
            <td>Confidence</td>
        </tr>
        <tr>
            <td>The Plateau</td>
            <td>7-12 Yrs</td>
            <td>
                30.0 - 50.0
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 80%; background: #666;"></div></div>
            </td>
            <td>Stagnation / Anxiety</td>
        </tr>
        <tr>
            <td>The Breakout</td>
            <td>12+ Yrs</td>
            <td>
                High Variance
                <div class="salary-bar-container"><div class="salary-bar-fill" style="width: 100%"></div></div>
            </td>
            <td>Leverage OR Irrelevance</td>
        </tr>
    </tbody>
</table>
<p style="font-size: 13px; color: #999; margin-top: 1rem;">*Based on Indian Product/Tech Market Data (2024-25).</p>
</div>
"""

target_persona = """
<p>This article is written for people who are far enough into their careers to sense a problem, but not far enough to have named it clearly.</p>

<p>Typically, that means:</p>
<ul>
<li>6 to 10 years of experience</li>
<li>a stable role</li>
<li>a respectable title</li>
<li>and a salary that looks fine on paper</li>
</ul>

<p>From the outside, things appear to be moving forward.</p>
<p>From the inside, something feels stalled.</p>

<p>If your workdays are predictable but not satisfying,<br>
if promotions have started to feel symbolic rather than meaningful,<br>
if learning new skills no longer changes how you’re evaluated,<br>
and if time has become a quiet pressure in the background —</p>

<p>this article is for you.</p>

<p>It is not written for people who are struggling to enter the workforce.<br>
It is not written for those chasing quick success stories.<br>
It is written for people who have already done most of what they were told would work, and are now wondering why it feels flatter than expected.</p>
"""

common_expectation = """
<p>Most professionals enter their careers with a simple, reasonable belief:</p>

<p><strong>If they work hard early, things will get easier later.</strong></p>

<p>The expectation is rarely articulated in detail, but it’s absorbed everywhere — from campus placements, first managers, performance reviews, and the stories people share when things are going well.</p>

<p>By the 6–8 year mark, many expect:</p>
<ul>
<li>confidence to replace uncertainty</li>
<li>promotions to compound naturally</li>
<li>compensation to feel materially different</li>
<li>work to become more strategic and less exhausting</li>
<li>and career momentum to start working with them instead of against them</li>
</ul>

<p>There is also an unspoken assumption that effort and progress remain tightly linked.<br>
That learning something new will continue to move the needle.<br>
That experience will automatically translate into leverage.</p>

<p>Early career reinforces this belief.<br>
The first few years often reward visible effort quickly. Skills improve, titles change, pay increases, and feedback stays encouraging. The system appears linear.</p>

<p>So when professionals approach the middle of their careers, they don’t expect a slowdown.<br>
They expect consolidation — stability with upward movement.</p>

<p>Very few expect a plateau.</p>
"""

actual_reality = """
<p>The career plateau rarely announces itself clearly.</p>

<p>There is no single event that marks its arrival. No obvious failure. No dramatic reversal. Instead, it shows up quietly, through a collection of small signals that are easy to dismiss in isolation.</p>

<p>Work starts to feel repetitive, even when it is technically complex.<br>
The problems are different, but the patterns aren’t.<br>
New projects resemble old ones more than expected.</p>

<p>Learning slows — not because opportunities disappear, but because the returns change.<br>
New skills improve efficiency, not trajectory.<br>
They make work smoother, but not meaningfully different.</p>

<p>Promotions, when they come, often feel procedural.<br>
Titles change, responsibilities expand slightly, and expectations increase — but the role’s fundamental shape remains intact. The workday looks similar before and after the change.</p>

<p>At this stage, effort no longer translates cleanly into progress.<br>
Performance remains solid, sometimes excellent, but the feedback becomes less specific. The praise shifts from growth to reliability.</p>

<p>This is where many professionals become confused.</p>

<p>Nothing is “wrong” in the obvious sense.<br>
The job is stable.<br>
The income is respectable.<br>
The résumé continues to grow.</p>

<p>And yet, momentum feels weaker than it should.</p>

<p>The plateau is not caused by a lack of ambition or ability.<br>
It is structural.</p>

<p>Most organizations are designed to reward rapid early growth and then slow down. As experience increases, the number of meaningful upward moves decreases. Competition intensifies. Decision-making consolidates. Visibility matters more than output.</p>

<p>The system stops being linear long before people expect it to.</p>
"""

salary_prose = """
<p>Compensation is often the clearest place where the plateau becomes visible — even if it takes time to acknowledge it.</p>

<p>In the early years of a career, salary changes feel transformative. Each increase meaningfully alters lifestyle, independence, and security. Switching roles can double compensation. Promotions feel tangible.</p>

<p>That pattern does not continue indefinitely.</p>

<p>By the mid-career phase, raises tend to compress. Increments become incremental in the literal sense. They outpace inflation on paper, but not always in lived experience.</p>

<p>Responsibilities, meanwhile, expand faster than compensation does.</p>

<p>Many professionals reach a point where:</p>
<ul>
<li>headline numbers look impressive</li>
<li>monthly obligations have grown alongside income</li>
<li>and the psychological impact of each increase has diminished</li>
</ul>

<p>At this stage, switching roles rarely produces dramatic jumps. The market prices experience more narrowly than it prices early potential. Lateral moves become common. Risk increases, reward stabilizes.</p>

<p>This creates a subtle tension.</p>

<p>People are told they are doing well — and in many ways, they are. But the financial progress they expected to feel decisive instead feels maintenance-oriented. The job sustains a life rather than reshaping it.</p>

<p>The plateau is not about low pay.<br>
It is about slowing financial leverage.</p>

<p>Understanding this distinction matters. Without it, professionals often misdiagnose the problem — assuming they need to work harder, learn more, or wait longer — when the underlying dynamics have already shifted.</p>
"""
salary_reality = salary_prose + salary_table_html

stuck_point = """
<p>The most common response to a career plateau is to assume it is temporary.</p>

<p>People tell themselves they are “between phases,” that one more project, one more role change, or one more skill will restart momentum. On the surface, this sounds reasonable. It often aligns with what worked earlier in their careers.</p>

<p>But this is where many professionals remain stuck for years.</p>

<p>One pattern is the endless upskilling loop. New technologies are learned, certifications are collected, and weekends are spent preparing for the next version of relevance. The effort is real. The progress is not always proportional. Skills improve, but positioning does not.</p>

<p>Another pattern is waiting for recognition to arrive naturally. People assume that consistent performance will eventually be noticed in a way that changes their trajectory. They stay longer than planned, hoping the system will reward patience the way it once did.</p>

<p>There is also the weight of accumulated comfort. By this stage, life has filled in around the job — financial commitments, family responsibilities, routines that are difficult to disrupt. The idea of starting over feels irresponsible, even if staying feels stagnant.</p>

<p>Over time, this creates a quiet trade-off.</p>

<p>People stop actively choosing their path and start maintaining it.<br>
They remain busy, but not deliberate.<br>
Stable, but not progressing in the way they once expected.</p>

<p>The plateau becomes durable not because it is desirable, but because it is familiar.</p>
"""

who_should_avoid = """
<p>The mid-career plateau is not universally negative.<br>
But it is not universally neutral either.</p>

<p><strong>For some, this phase works.</strong></p>

<p>It suits people who value predictability, who prefer stability over acceleration, and who are comfortable letting work occupy a defined, bounded role in their lives. For them, a flatter growth curve can coincide with fuller lives elsewhere.</p>

<p><strong>For others, it does not.</strong></p>

<p>It tends to strain people whose sense of progress is closely tied to identity. Those who measure fulfillment through momentum, challenge, or visible advancement often find this phase draining rather than calming.</p>

<p>The difference is not talent or ambition.<br>
It is alignment.</p>

<p>Problems arise when people try to force themselves to accept a structure that no longer matches what they need — or when they deny that their expectations have changed.</p>

<p>The plateau itself is not the issue.<br>
Living in it unintentionally is.</p>
"""

verdict = """
<p>The mid-career plateau is not a personal failure, and it is not a rare anomaly.</p>

<p>It is a predictable phase that emerges when early-career momentum meets structural limits — limits that are rarely discussed openly because they complicate the success narratives people prefer to share.</p>

<p>What makes this phase difficult is not stagnation alone, but ambiguity.</p>

<p>People are often unsure whether what they are experiencing is:</p>
<ul>
<li>a temporary slowdown</li>
<li>a signal to wait longer</li>
<li>or a sign that the assumptions they built their careers on no longer apply</li>
</ul>

<p>In the absence of clarity, many default to endurance. They stay busy, stay employed, and stay hopeful that momentum will return on its own.</p>

<p>Sometimes it does. Often, it doesn’t.</p>

<p>The cost of the plateau is not always financial.<br>
More frequently, it is temporal.</p>

<p>Years pass while careers remain intact but unexamined. By the time dissatisfaction becomes explicit, options feel narrower than they once were — not because they disappeared, but because they were postponed.</p>

<p>The uncomfortable truth is this:<br>
the plateau does not demand panic, but it does demand awareness.</p>

<p>Ignoring it has consequences.<br>
Overreacting to it has consequences too.</p>

<p>What matters is recognizing that this phase is not an interruption of a career — it is part of how careers actually unfold.</p>
"""

# 5. PUBLISH WITH FINAL METADATA
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
        "meta_title": "The 7-Year Career Plateau Nobody Warns You About",
        "meta_description": "A calm, honest look at the mid-career plateau many professionals face after 6–10 years—and why it happens more often than people admit.",
        "published_at": timezone.now(),
        "last_reality_check": datetime.date.today(),
    }
)

print(f"Final Configuration Complete: {title}")
print(f"Slug: {slug}")
print(f"Category: {cat_name}")
