import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Author

try:
    # Assuming ID 2 based on user screenshot /author/2/
    author = Author.objects.get(id=2)
    print(f"Found Author: {author.display_name}")
    print(f"Old Bio: {author.bio}")
    
    new_bio = "Not a 'Thought Leader'. Just an observer with a low tolerance for corporate lies. I don't have a content calendar; I write here when I feel like it. Follow me on LinkedIn."
    
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
