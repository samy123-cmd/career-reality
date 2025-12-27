
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from content.models import Author

def run():
    target_url = "https://www.linkedin.com/in/shivmishra1408"
    
    # 1. Update ALL authors to use the target URL
    count = Author.objects.all().update(linkedin_url=target_url)
    print(f"Updated {count} authors to link: {target_url}")

    # 2. Ensure reasonable Display Names
    # If any display_name is missing or generic, fix it.
    for author in Author.objects.all():
        if not author.display_name or "admin" in author.display_name.lower():
            author.display_name = "Shiv Mishra"
            author.save()
            print(f"Fixed display name for author ID {author.id} to 'Shiv Mishra'")
        else:
             print(f"Author {author.display_name} is good.")

if __name__ == "__main__":
    run()
