import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Article

slug_to_remove = "frontend-developer-reality-india-2025"
deleted_count, _ = Article.objects.filter(slug=slug_to_remove).delete()

print(f"Deleted {deleted_count} legacy article(s) with slug: {slug_to_remove}")
