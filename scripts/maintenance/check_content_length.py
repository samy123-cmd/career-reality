import os
import django
from django.db.models import Sum, F, Value
from django.db.models.functions import Length

# Setup Django environment
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Article

def count_words(text):
    if not text:
        return 0
    return len(text.split())

def analyze_content():
    print(" Analyzing Article Content Length...\n")
    print(f"{'TITLE':<60} | {'WORDS':<10} | {'STATUS'}")
    print("-" * 90)

    articles = Article.objects.all()
    thin_count = 0
    total_count = 0

    results = []

    for article in articles:
        # Calculate total word count across all content fields
        content_fields = [
            article.common_expectation,
            article.actual_reality,
            article.salary_reality,
            article.stuck_point,
            article.verdict
        ]
        
        # Add intro fields too for completeness
        intro_fields = [
            article.target_persona,
            article.who_should_avoid
        ]

        total_words = sum(count_words(field) for field in content_fields + intro_fields)
        results.append((article.title, total_words, article.slug))

    # Sort by word count (ascending)
    results.sort(key=lambda x: x[1])

    for title, words, slug in results:
        status = "🔴 THIN" if words < 600 else "🟢 GOOD"
        if words < 600:
            thin_count += 1
        
        # Truncate title for display
        display_title = (title[:57] + '..') if len(title) > 57 else title
        print(f"{display_title:<60} | {words:<10} | {status}")

    print("-" * 90)
    print(f"\nSummary:")
    print(f"Total Articles: {len(articles)}")
    print(f"Thin Articles (< 600 words): {thin_count}")
    print(f"Healthy Articles (> 600 words): {len(articles) - thin_count}")

if __name__ == "__main__":
    analyze_content()
