import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()

from django.core import serializers
from companies.models import Company

try:
    from companies.models import CompanyReview
    all_objs = list(Company.objects.all()) + list(CompanyReview.objects.all())
    print(f'Exporting {Company.objects.count()} companies + {CompanyReview.objects.count()} reviews')
except Exception:
    all_objs = list(Company.objects.all())
    print(f'Exporting {Company.objects.count()} companies (no reviews model)')

data = serializers.serialize('json', all_objs, indent=2, ensure_ascii=True)
with open('companies_export.json', 'w', encoding='utf-8') as f:
    f.write(data)
print('Done: companies_export.json')
