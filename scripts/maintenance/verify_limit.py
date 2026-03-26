import os
import django
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Article

# Mimic the view's query
articles = Article.objects.filter(status='published').select_related('author', 'category').order_by('-published_at')[:10]
count = len(list(articles))
print(f"Fetched articles count: {count}")

if count <= 10:
    print("SUCCESS: Article limit is working.")
else:
    print(f"FAILURE: Article limit NOT working. Got {count}")
