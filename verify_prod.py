import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()

from content.models import Article, Category, Author
from ainews.models import AINewsItem
from companies.models import Company
from analyzer.models import SalarySubmission

print('=== DB RECORD COUNTS ===')
print('Articles total:', Article.objects.count())
print('Categories:', Category.objects.count())
print('Companies:', Company.objects.count())
print('  - with avg_ctc:', Company.objects.exclude(avg_ctc=None).count())
print('  - with overall_score:', Company.objects.exclude(overall_score=None).count())
print('SalarySubmissions total:', SalarySubmission.objects.count())
print('  - verified:', SalarySubmission.objects.filter(is_verified=True).count())

# Sample company data
print()
print('Sample companies:')
for c in Company.objects.order_by('name')[:5]:
    print(f'  {c.name}: avg={c.avg_ctc} score={c.overall_score} salaries={c.salary_count}')
