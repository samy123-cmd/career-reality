"""
Fix article publication dates to be realistic past dates
Also adds more category descriptions
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from content.models import Article, Category
from datetime import datetime, timedelta
from django.utils import timezone
import random

# ============================================================
# FIX ARTICLE DATES
# ============================================================

print("Updating article publication dates...")

articles = Article.objects.all()
base_date = timezone.now() - timedelta(days=180)  # Start 6 months ago

for i, article in enumerate(articles):
    # Stagger dates so they're spread across the last 6 months
    days_offset = random.randint(0, 180)
    article.published_at = base_date + timedelta(days=days_offset)
    # Also set updated_at by using the model's auto-update
    article.save()
    print(f"  ✓ {article.title[:40]}... → {article.published_at.strftime('%B %Y')}")

print(f"\n✓ Updated {articles.count()} article dates")

# ============================================================
# ADD CATEGORY DESCRIPTIONS
# ============================================================

print("\nUpdating category descriptions...")

category_descriptions = {
    'career-reality-checks': 'Hard truths about career progression, salary expectations, and the gap between professional aspirations and workplace reality in India.',
    'career-strategy': 'Strategic career decisions, long-term planning, and navigating the complexities of professional growth in the Indian job market.',
    'data-science': 'Reality checks for data science careers—the actual work, salary expectations, and skills that matter in Indian tech companies.',
    'education': 'The truth about educational investments, degrees, certifications, and their actual impact on career outcomes in India.',
    'engineering': 'Career realities for software engineers, developers, and technical professionals navigating the Indian tech industry.',
    'learning': 'What actually works for professional skill development, and what the upskilling industry conveniently omits.',
    'money-reality': 'Real talk about salaries, compensation structures, financial planning, and what money actually buys in professional life.',
    'design': 'Career realities for UX designers, product designers, and creative professionals in Indian tech.',
    'financial-reality': 'The financial truths behind career decisions—ROI of education, salary negotiations, and wealth building.',
    'marketing': 'Digital marketing career realities—agency life, in-house roles, and what actually drives career growth.',
    'product-management': 'The truth about PM roles—what the job actually involves versus the "mini-CEO" narrative.',
    'software-engineering': 'Hard truths about software engineering careers—skill ceiling, salary progression, and common career traps.',
}

for slug, description in category_descriptions.items():
    try:
        category = Category.objects.get(slug=slug)
        category.description = description
        category.save()
        print(f"  ✓ {category.name}")
    except Category.DoesNotExist:
        print(f"  ⚠ Category '{slug}' not found")

print("\n✅ All dates and categories updated!")
