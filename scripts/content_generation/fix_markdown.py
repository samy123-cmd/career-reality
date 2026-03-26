"""Fix markdown to HTML in all articles"""
import os
import re
os.environ['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'postgresql://postgres.iakuzoeqdjkutpgettlx:<YOUR_SUPABASE_PASSWORD>@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()
from content.models import Article

def convert_markdown_to_html(text):
    """Convert markdown formatting to HTML"""
    if not text:
        return text
    
    # Convert **bold** to <strong>
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    
    # Convert *italic* to <em> (but not inside HTML tags)
    text = re.sub(r'(?<![<>])\*([^*]+)\*(?![<>])', r'<em>\1</em>', text)
    
    # Convert `code` to <code>
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # Convert - list items to proper lists (only at start of line)
    lines = text.split('\n')
    result_lines = []
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- '):
            if not in_list:
                result_lines.append('<ul>')
                in_list = True
            content = stripped[2:]
            # Convert internal markdown in list items
            content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
            result_lines.append(f'<li>{content}</li>')
        else:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            result_lines.append(line)
    
    if in_list:
        result_lines.append('</ul>')
    
    text = '\n'.join(result_lines)
    
    # Convert numbered lists (1. 2. 3. etc)
    lines = text.split('\n')
    result_lines = []
    in_ol = False
    
    for line in lines:
        stripped = line.strip()
        if re.match(r'^\d+\.\s', stripped):
            if not in_ol:
                result_lines.append('<ol>')
                in_ol = True
            content = re.sub(r'^\d+\.\s', '', stripped)
            content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
            result_lines.append(f'<li>{content}</li>')
        else:
            if in_ol:
                result_lines.append('</ol>')
                in_ol = False
            result_lines.append(line)
    
    if in_ol:
        result_lines.append('</ol>')
    
    text = '\n'.join(result_lines)
    
    # Convert double newlines to paragraph breaks
    text = re.sub(r'\n\n+', '</p>\n\n<p>', text)
    
    return text

print("Converting markdown to HTML in all articles...")

# Get all new articles (those with markdown)
slugs = [
    'indian-education-trap-degree-career-mistake',
    'broke-at-30-money-mistakes-nobody-warned',
    'self-learning-trap-online-courses-expensive-entertainment',
    'engineering-career-ceiling-peak-at-35',
    'career-switch-illusion-changing-jobs-not-career',
    'data-science-bubble-excel-work-reality',
    'networking-myth-professional-relationships-worthless',
    '10x-developer-myth-productivity-killing-careers',
    'pm-prestige-trap-escape-from-engineering',
    'digital-marketing-illusion-instagram-ads-burning-money',
    'ux-salary-myth-design-careers-plateau',
    'home-loan-trap-dream-house-financial-prison'
]

fields_to_convert = [
    'target_persona',
    'who_should_avoid',
    'common_expectation',
    'actual_reality',
    'salary_reality',
    'stuck_point',
    'verdict'
]

count = 0
for slug in slugs:
    try:
        article = Article.objects.get(slug=slug)
        changed = False
        for field in fields_to_convert:
            content = getattr(article, field, '')
            if content and '**' in content:
                new_content = convert_markdown_to_html(content)
                setattr(article, field, new_content)
                changed = True
        
        if changed:
            article.save()
            count += 1
            print(f"  Fixed: {slug[:45]}")
    except Article.DoesNotExist:
        print(f"  Not found: {slug}")
    except Exception as e:
        print(f"  Error: {slug} - {e}")

print(f"\nConverted {count} articles from markdown to HTML!")
