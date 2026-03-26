import os
import django

import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Article

slug_to_remove = "frontend-developer-reality-india-2025"
deleted_count, _ = Article.objects.filter(slug=slug_to_remove).delete()

print(f"Deleted {deleted_count} legacy article(s) with slug: {slug_to_remove}")
