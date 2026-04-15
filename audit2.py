import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()

from content.models import Category, Article
from companies.models import Company

print('=== Categories ===')
for c in Category.objects.all().order_by('name'):
    count = Article.objects.filter(category=c, status='published').count()
    desc_len = len(c.description or '')
    print(f'{c.name}: {count} articles | {desc_len} desc chars | slug={c.slug}')

print()
print('=== Companies - full data ===')
for c in Company.objects.all().order_by('name'):
    print(f'{c.name}: website={bool(c.website)} logo={bool(c.logo_url)} glassdoor={c.glassdoor_rating} ambitionbox={c.ambitionbox_rating} size={c.size} work_mode={c.work_mode}')
