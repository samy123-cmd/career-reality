import os
import django

# Set Supabase DATABASE_URL
os.environ['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'postgresql://postgres.iakuzoeqdjkutpgettlx:<YOUR_SUPABASE_PASSWORD>@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

django.setup()

from django.db import connection

# Drop all constraints and indexes that might be causing issues
# Then reload with a more lenient approach

print("Modifying varchar lengths...")

alter_statements = [
    # Increase varchar limits for common fields
    "ALTER TABLE auth_user ALTER COLUMN username TYPE varchar(150);",
    "ALTER TABLE auth_user ALTER COLUMN first_name TYPE varchar(150);",
    "ALTER TABLE auth_user ALTER COLUMN last_name TYPE varchar(150);",
    "ALTER TABLE auth_user ALTER COLUMN email TYPE varchar(254);",
    "ALTER TABLE django_site ALTER COLUMN domain TYPE varchar(255);",
    "ALTER TABLE django_site ALTER COLUMN name TYPE varchar(255);",
]

with connection.cursor() as cursor:
    for sql in alter_statements:
        try:
            cursor.execute(sql)
            print(f"OK: {sql[:60]}...")
        except Exception as e:
            print(f"Skip: {sql[:40]}... - {e}")

print("\nNow trying import again...")

from django.core.management import call_command

try:
    call_command('loaddata', 'data_export.json', verbosity=1)
    print("\nData import completed!")
    
    from content.models import Article, Category, Author
    print(f"\nVerification:")
    print(f"  Articles: {Article.objects.count()}")
    print(f"  Categories: {Category.objects.count()}")
    print(f"  Authors: {Author.objects.count()}")
except Exception as e:
    print(f"\nError: {e}")
