import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Article

print(f"Total Articles: {Article.objects.count()}")
print("-" * 50)
premium_count = 0
basic_count = 0

for a in Article.objects.all():
    is_premium = '<table class="editorial-table">' in a.salary_reality
    if is_premium:
        premium_count += 1
    else:
        basic_count += 1
        print(f"[BASIC]  {a.slug}  |  {a.title}")

print("-" * 50)
print(f"Premium: {premium_count}")
print(f"Basic:   {basic_count}")
