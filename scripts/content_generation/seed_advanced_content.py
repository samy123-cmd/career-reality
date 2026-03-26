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

# Ensure Author exists
author, _ = Author.objects.get_or_create(
    name="P. Mishra",
    defaults={
        "display_name": "P. Mishra",
        "bio": "10+ Years in Tech & Strategy. Based in Bangalore.",
        "linkedin_url": "https://linkedin.com/in/example",
        "is_active": True
    }
)

# Helpers
def create_article(cat_name, slug, title, persona, avoid, expect, reality, salary, stuck_point, verdict, seo_desc):
    category, _ = Category.objects.get_or_create(name=cat_name, defaults={"slug":  cat_name.lower().replace(" ", "-"), "order": 2})
    
    article, created = Article.objects.get_or_create(
        slug=slug,
        defaults={
            "title": title,
            "author": author,
            "category": category,
            "status": "published",
            "target_persona": persona,
            "who_should_avoid": avoid,
            "common_expectation": expect,
            "actual_reality": reality,
            "salary_reality": salary,
            "stuck_point": stuck_point,
            "verdict": verdict,
            "meta_title": title[:60],
            "meta_description": seo_desc[:160],
            "published_at": timezone.now(),
            "last_reality_check": datetime.date.today(),
        }
    )
    print(f"Processed: {title}")

# 1. Frontend Developer
create_article(
    cat_name="Software Engineering",
    slug="frontend-developer-reality-india-2025",
    title="The Reality of Frontend Development in India (It's Not Just React)",
    persona="Bootcamp grads and Self-taught developers expecting easy remote jobs.",
    avoid="People who hate debugging logic and think CSS is 'easy'. If you rely entirely on AI to write loops, you will fail the machine coding round.",
    expect="I will learn React, build a few clones (Netflix/Spotify), and get hired for 12 LPA. I'll spend my day centering divs and making animations.",
    reality="The 'React Wrapper' era is over. Companies now demand Full Stack capabilities even for frontend roles.\n\nAI tools like v0 and Cursor generate UI faster than you can. Your value is now in **State Management, Performance Optimization, and System Design**.\n\nIf you can't explain how the Virtual DOM works or optimize a re-render cycle, you are unhirable.",
    salary="| Role | Experience | Realistic Content (LPA) |\n|---|---|---|\n| Junior React Dev | 0-2 Years | 3.5 - 6.0 |\n| Senior Frontend | 4-6 Years | 18.0 - 28.0 |\n| Principal UI Eng | 8+ Years | 45.0+ |\n\nEntry level is crushed by supply. Senior level pays hugely but requires deep architecture skills.",
    stuck_point="The 'Tutorial Hell' Trap.\n\nMost juniors can build a To-Do app following a video but cannot debug a race condition in a `useEffect` hook without help. This is where 70% of candidates get rejected.",
    verdict="Frontend is no longer the 'easy entry' into tech. You must be a Software Engineer first, a React developer second. Learn TypeScript and Server Components or perish.",
    seo_desc="Honest truth about Frontend jobs in India. Why React alone is not enough and specific salary data for 2025."
)

# 2. Product Manager
create_article(
    cat_name="Product Management",
    slug="product-manager-reality-india",
    title="Product Management is Not 'CEO of the Product' (The Indian Reality)",
    persona="Engineers and MBAs seeking power, strategy, and high status.",
    avoid="People who hate conflict, need clear instructions, or want a 9-to-5 job. If you can't handle being blamed for things you didn't do, stay away.",
    expect="I will set the vision, command the engineering team, and make high-level strategy decisions while sipping coffee.",
    reality="You are the 'Janitor of Jira'.\n\nYou have 100% of the responsibility for the product failing, but 0% authority to order anyone to do anything.\n\nDais life is 6 hours of 'alignment calls', chasing developers for updates, and pleading with stakeholders. Strategy is 5% of the job; execution is 95%.",
    salary="| Role | Experience | Realistic Content (LPA) |\n|---|---|---|\n| APM (Fresher) | 0-2 Years | 12.0 - 18.0 |\n| Product Manager | 3-5 Years | 22.0 - 35.0 |\n| Group PM | 8+ Years | 60.0+ |\n\nHigh ceiling, but high burnout. Salaries vary wildly between 'Service' and 'Product' companies.",
    stuck_point="The 'Execution Trap'.\n\nMany PMs get stuck as 'Backlog Groomers'—just writing tickets and never driving outcomes. Moving from 'Delivery' to 'Strategy' is the hardest leap.",
    verdict="A high-status, high-pay role that costs you your peace of mind. Only pursue if you thrive on chaos and solving ambiguous human problems.",
    seo_desc="The brutal truth about Product Management in India. It's not being CEO; it's being a high-paid coordinator. Salary and stress reality check."
)

# 3. Digital Marketing
create_article(
    cat_name="Marketing",
    slug="digital-marketing-reality-india",
    title="Digital Marketing Reality: It's Excel Sheets, Not Viral Reels",
    persona="Creative thinkers who believe marketing is about making cool Instagram content.",
    avoid="If you hate numbers, analytics, and spreadsheets, do not enter Digital Marketing. Go into Content Creation instead.",
    expect="I'll be a 'Social Media Manager', making memes and viral videos all day. It's a fun, creative creative job.",
    reality="Performance Marketing (Ads) is the only area with real money, and it is 90% data analysis.\n\nYou will stare at Facebook Ads Manager and Google Analytics dashboards all day, tweaking bid caps and CPA targets.\n\nAgency life is a burnout factory with 12-hour workdays and demanding clients.",
    salary="| Role | Experience | Realistic Content (LPA) |\n|---|---|---|\n| Junior Executive | 0-1 Years | 3.0 - 4.5 |\n| Performance Marketer | 3-4 Years | 8.0 - 15.0 |\n| CMO / Head | 10+ Years | 30.0 - 50.0 |\n\nLow entry barrier = Low entry salaries. You must specialize in Performance or SEO to earn well.",
    stuck_point="The 'Agency Loop'.\n\nStaying in an agency too long caps your salary. The real money is in moving 'In-House' to a B2B SaaS or D2C brand after 3-4 years.",
    verdict="Ignore the 'make money online' gurus. True Digital Marketing is a technical, data-driven profession. Learn SQL and Analytics, not just Canva.",
    seo_desc="Digital Marketing career reality in India. Why it is data-driven work and why agency life leads to burnout. Salary data included."
)

# 4. UX Design
create_article(
    cat_name="Design",
    slug="ux-design-reality-india",
    title="UX Design in India: They Want UI Painters, Not Researchers",
    persona="Graphic designers and architects switching to tech for 'empathy' and 'research'.",
    avoid="If you refuse to learn Figma shortcuts or basic HTML/CSS logic, you will struggle. Pure 'Research' roles are rare.",
    expect="I will spend weeks doing user empathy mapping, conducting interviews, and building accessible, human-centric products.",
    reality="Most Indian startups just want a 'UI Painter' to copy the screens of Cred, Airbnb, or Uber.\n\nResearch budgets are almost non-existent. You will be asked to 'just make it pop' and 'finish the screens by tomorrow'.\n\nReal UX process is a luxury afforded only by the top 1% of companies.",
    salary="| Role | Experience | Realistic Content (LPA) |\n|---|---|---|\n| Junior Designer | 0-2 Years | 4.0 - 7.0 |\n| Senior Product Designer | 4-6 Years | 15.0 - 28.0 |\n| Design Manager | 8+ Years | 40.0+ |\n\nPortfolio is everything. Degrees don't matter.",
    stuck_point="The 'Dribbble Effect'.\n\nDesigners who make pretty but unusable screens get hired junior but fired senior. You must understand business constraints and developer feasibility.",
    verdict="A great career, but be ready to fight for the user. Learn to design for speed and business impact, not just for your portfolio.",
    seo_desc="UX Design career path reality in India. The gap between design school expectations and the 'make it pretty' startup reality."
)
