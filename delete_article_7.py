import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Article

try:
    article = Article.objects.get(id=7)
    title = article.title
    slug = article.slug
    article.delete()
    print(f"SUCCESS: Deleted Article 7 ('{title}', slug='{slug}').")
except Article.DoesNotExist:
    print("Article 7 does not exist (already deleted?).")
except Exception as e:
    print(f"ERROR: {e}")
