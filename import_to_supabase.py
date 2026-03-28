import os
import django

# Set Supabase DATABASE_URL
os.environ['DATABASE_URL'] = 'postgresql://postgres.iakuzoeqdjkutpgettlx:vTo8B7KGQmoa4PqK@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres'
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

django.setup()

from django.core.management import call_command

print("Importing data to Supabase PostgreSQL...")

try:
    call_command('loaddata', 'data_export.json', verbosity=2)
    print("\nData import completed successfully!")
    
    # Verify
    from content.models import Article, Category, Author
    print(f"\nVerification:")
    print(f"  Articles: {Article.objects.count()}")
    print(f"  Categories: {Category.objects.count()}")
    print(f"  Authors: {Author.objects.count()}")
    
except Exception as e:
    print(f"Error: {e}")
