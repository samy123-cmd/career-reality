"""
Fix the broken template tag in category_detail.html
"""
import re

filepath = 'templates/content/category_detail.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print("Before fix:")
print("=" * 50)
# Find the broken pattern
if '{{ article.author.display_name }}</a>' in content and 'article.updated_at|date:"F Y"' in content:
    print("Found the template tag content...")
    
    # Use regex to find the split pattern
    # Match: · {{ followed by whitespace/newline, then article.updated_at...
    pattern = r'·\s*\{\{\s*\n\s*article\.updated_at\|date:"F Y"\s*\}\}'
    
    if re.search(pattern, content):
        print("Found split pattern with regex!")
        content = re.sub(pattern, '· {{ article.updated_at|date:"F Y" }}', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("\n✅ Fixed! Template tag is now on single line.")
    else:
        print("Regex pattern not found, trying alternative...")
        # Try a more flexible pattern
        pattern2 = r'\}\}</a>\s*·\s*\{\{\s+article\.updated_at'
        match = re.search(pattern2, content)
        if match:
            print(f"Found at position: {match.start()}-{match.end()}")
            print(f"Match: {repr(match.group())}")
        else:
            print("Alternative pattern also not found")
            # Print the area around the problem
            idx = content.find('article.updated_at')
            if idx > 0:
                print(f"\nContext around 'article.updated_at':")
                print(repr(content[idx-100:idx+100]))
else:
    print("Content markers not found")

# Verify
print("\n" + "=" * 50)
print("After fix - checking lines 28-33:")
lines = content.split('\n')
for i, line in enumerate(lines[27:33], start=28):
    print(f"{i}: {line}")
