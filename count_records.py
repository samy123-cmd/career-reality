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
print('Articles published:', Article.objects.filter(status='published').count())
print('Categories:', Category.objects.count())
print('Authors:', Author.objects.count())
print('AINewsItems total:', AINewsItem.objects.count())
print('AINewsItems published:', AINewsItem.objects.filter(status='published').count())
print('Companies:', Company.objects.count())
print('SalarySubmissions:', SalarySubmission.objects.count())
