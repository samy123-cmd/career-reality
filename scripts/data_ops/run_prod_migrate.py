import os
import django
from django.core.management import execute_from_command_line

# SET PROD CREDENTIALS
db_url = os.environ.get('DATABASE_URL')
if not db_url:
    raise ValueError("❌ DATABASE_URL environment variable is not set. Please set it before running production migrations.")
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

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
