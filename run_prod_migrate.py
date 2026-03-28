import os
import django
from django.core.management import execute_from_command_line

# SET PROD CREDENTIALS (Found in your scripts)
os.environ['DATABASE_URL'] = 'postgresql://postgres.iakuzoeqdjkutpgettlx:vTo8B7KGQmoa4PqK@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

if __name__ == "__main__":
    print("🚀 Connecting to Supabase Production DB...")
    try:
        django.setup()
        print("✅ Connection Successful.")
        print("📦 Applying Migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("🎉 Migrations Applied Successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
