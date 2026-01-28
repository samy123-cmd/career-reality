import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Article

count = Article.objects.filter(status='published').count()
print(f"Total published articles: {count}")
