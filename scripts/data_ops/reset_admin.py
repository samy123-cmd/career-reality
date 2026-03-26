import os
import django

# Setup Django environment
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

try:
    User = get_user_model()
    username = 'admin'
    password = 'password123'
    email = 'admin@careerreality.in'

    # Try to get 'admin' or create it
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"SUCCESS: Reset password for existing user '{username}' to '{password}'")
    else:
        User.objects.create_superuser(username, email, password)
        print(f"SUCCESS: Created new superuser '{username}' with password '{password}'")

except Exception as e:
    print(f"ERROR: {str(e)}")
