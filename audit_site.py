import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()

from content.models import Article, Author, Category
from ainews.models import AINewsItem
from companies.models import Company

print('=== Article Health ===')
arts = list(Article.objects.all())
print('Total articles:', len(arts))
print('No meta_title:', sum(1 for a in arts if not a.meta_title))
print('No meta_description:', sum(1 for a in arts if not a.meta_description))
no_body = [a.slug for a in arts if not getattr(a, 'actual_reality', None)]
print('No actual_reality body:', len(no_body))
no_verdict = [a.slug for a in arts if not getattr(a, 'verdict', None)]
print('No verdict:', len(no_verdict))
print()

print('=== Author Health ===')
for au in Author.objects.all():
    bio_len = len(au.bio or '')
    linkedin = bool(getattr(au, 'linkedin_url', ''))
    twitter = bool(getattr(au, 'twitter_url', ''))
    credentials = getattr(au, 'credentials', '')
    print(f'  {au.display_name}: bio={bio_len}chars linkedin={linkedin} twitter={twitter} credentials={bool(credentials)}')
print()

print('=== Category Health ===')
for cat in Category.objects.all():
    count = Article.objects.filter(category=cat, status='published').count()
    desc = bool(getattr(cat, 'description', ''))
    print(f'  {cat.name}: {count} articles, has_desc={desc}')
print()

print('=== AI News Health ===')
items = list(AINewsItem.objects.filter(status='published'))
print('Published count:', len(items))
no_meta = [i.slug for i in items if not i.meta_title]
print('No meta_title:', len(no_meta))
no_desc = [i.slug for i in items if not i.meta_description]
print('No meta_description:', len(no_desc))
print()

print('=== Company Health ===')
companies = Company.objects.all()
print('Total:', companies.count())
print('No website:', companies.filter(website='').count())
print('No logo_url:', companies.filter(logo_url='').count())
print('No glassdoor_rating:', companies.filter(glassdoor_rating=None).count())
print('No ambitionbox_rating:', companies.filter(ambitionbox_rating=None).count())
