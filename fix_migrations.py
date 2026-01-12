import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
os.environ['DATABASE_URL'] = 'postgresql://postgres.iakuzoeqdjkutpgettlx:vTo8B7KGQmoa4PqK@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres'

django.setup()

from django.core.management import call_command
from django.db import connection

# Check current tables
with connection.cursor() as cursor:
    cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"Current tables: {tables}")

# If django_migrations exists but other tables don't, we need to reset
if 'django_migrations' in tables and 'content_article' not in tables:
    print("\nResetting migration state...")
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS django_migrations CASCADE;")
    print("Dropped django_migrations table")

# Now run migrate
print("\nRunning migrations...")
call_command('migrate', verbosity=2)

# Verify
with connection.cursor() as cursor:
    cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"\nFinal tables: {tables}")
