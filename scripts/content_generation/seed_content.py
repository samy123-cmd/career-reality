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

# 1. Create Author
author, created = Author.objects.get_or_create(
    name="P. Mishra",
    defaults={
        "display_name": "P. Mishra",
        "bio": "10+ Years in Tech & Strategy. Based in Bangalore.",
        "linkedin_url": "https://linkedin.com/in/example",
        "experience_summary": "Ex-PM at Unicorn",
        "is_active": True
    }
)
print(f"Author: {author}")

# 2. Create Category
category, created = Category.objects.get_or_create(
    name="Data Science",
    defaults={
        "slug": "data-science",
        "description": "The reality of data roles in India.",
        "order": 1
    }
)
print(f"Category: {category}")

# 3. Create Article
article, created = Article.objects.get_or_create(
    slug="junior-data-scientist-reality-india",
    defaults={
        "title": "The Brutal Reality of 'Junior Data Scientist' Jobs in India (2025)",
        "author": author,
        "category": category,
        "status": "published",
        "target_persona": "Fresh graduates and career switchers expecting 15 LPA+ starting packages.",
        "who_should_avoid": "People who hate statistics but love the 'AI hype'. If you find cleaning Excel sheets boring, do not enter this field.",
        "common_expectation": "I will spend 100% of my time building LLMs, training deep learning models, and solving AGI. Companies will pay me 20 LPA just because I know Python.",
        "actual_reality": "90% of 'Data Scientist' roles in India are actually Data Analyst or Data Engineering roles in disguise.\n\nYou will spend 80% of your time cleaning dirty CSVs, fixing SQL query errors, and making PowerBI dashboards for management.\n\nYou will likely not touch a neural network for the first 3 years of your career.",
        "salary_reality": "| Level | Realistic Salary (India) |\n|---|---|\n| Fresher (Service Base) | 3.5 - 5 LPA |\n| Fresher (Product Base) | 8 - 12 LPA |\n| Senior (5+ Years) | 25 - 40 LPA |\n\nThe gap between entry-level and senior is massive. Entry level is saturated.",
        "stuck_point": "The 'SQL Filter'.\n\nMost innovative work happens in Python, but most *business* work happens in SQL. Juniors who refuse to master advanced SQL get stuck as 'notebook maintainers' and never move up.",
        "verdict": "Data Science is a powerful, long-term career, but it is NOT a lottery ticket. The 'bootcamp to 20 LPA' path is dead. Enter only if you genuinely enjoy math and data cleaning.",
        "meta_title": "Data Scientist Reality India: Salary, Work, and Burnout (2025)",
        "meta_description": "Honest reality check on Data Science careers in India. What they don't tell you about the 80% data cleaning grind.",
        "published_at": timezone.now(),
        "last_reality_check": datetime.date.today(),
    }
)
print(f"Article: {article.title}")
