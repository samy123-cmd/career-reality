import os
import django
from django.utils import timezone
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from content.models import Article
from ainews.models import AINewsItem
from django.db import transaction

def main():
    now = timezone.now()
    today = now.date()

    print(
        "Running conservative content refresh at "
        f"{now.isoformat()}.\n"
        "This script does not mark content as fact-checked or append verification claims."
    )

    # 1. Refresh article timestamps only
    articles = Article.objects.all()
    print(f"Refreshing {articles.count()} Articles...")
    updated_articles = []

    with transaction.atomic():
        for article in articles:
            article.updated_at = now
            if article.status == "published":
                article.last_reality_check = today
            updated_articles.append(article)

        Article.objects.bulk_update(
            updated_articles,
            ['updated_at', 'last_reality_check'],
            batch_size=500
        )
    print(f"Refreshed {len(updated_articles)} Articles.")

    # 2. Refresh AI news timestamps only for already-verified items
    news_items = AINewsItem.objects.all()
    print(f"Refreshing {news_items.count()} AI News Items...")
    updated_news = []

    with transaction.atomic():
        for news in news_items:
            if news.fact_check_status == 'verified':
                news.last_verified_at = now
                updated_fields = True
            else:
                updated_fields = False
            if news.status == 'published' and not news.reviewed_at:
                news.reviewed_at = now
                updated_fields = True
            if not updated_fields:
                continue
            updated_news.append(news)

        AINewsItem.objects.bulk_update(
            updated_news,
            ['reviewed_at', 'last_verified_at'],
            batch_size=500
        )
    print(f"Refreshed {len(updated_news)} AI News Items.")

if __name__ == '__main__':
    main()
