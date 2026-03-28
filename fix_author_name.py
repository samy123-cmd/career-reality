import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Author

# Target the corrupted author
authors = Author.objects.filter(display_name__contains="{{")

for author in authors:
    print(f"Fixing Author: {author.name} (Was: {author.display_name})")
    author.display_name = author.name
    author.save()
    print(f" -> Fixed: {author.display_name}")

if not authors:
    print("No corrupted authors found. Checking specifically for P. Mishra...")
    try:
        a = Author.objects.get(name="P. Mishra")
        print(f"P. Mishra display_name: {a.display_name}")
        if "{{" in a.display_name:
            a.display_name = "P. Mishra"
            a.save()
            print(" -> Fixed manually.")
    except Author.DoesNotExist:
        print("Author P. Mishra not found within standard query.")
