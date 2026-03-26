import os
import django

import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Author

try:
    # Assuming ID 2 based on user screenshot /author/2/
    author = Author.objects.get(id=2)
    print(f"Found Author: {author.display_name}")
    print(f"Old Bio: {author.bio}")
    
    new_bio = "Not a 'thought leader'. Not a LinkedIn influencer. Just someone who's been in tech long enough to have opinions and low enough patience to share them. No content calendar here—I write when I'm bored, frustrated, or when someone's bullshit finally crosses my threshold. If that sounds useful, stick around."
    
    author.bio = new_bio
    author.save()
    
    print("-" * 30)
    print(f"New Bio: {author.bio}")
    print("SUCCESS: Author bio updated.")

except Author.DoesNotExist:
    print("Author ID 2 not found! listing all authors:")
    for a in Author.objects.all():
        print(f"ID: {a.id} | Name: {a.display_name}")

except Exception as e:
    print(f"ERROR: {e}")
