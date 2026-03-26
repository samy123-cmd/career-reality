import re

# Read the file
with open('templates/content/article_detail.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix lines 39-40: {{ article.target_persona|safe }}
content = re.sub(
    r'\{\{\s*\n?\s*article\.target_persona\|safe\s*\}\}',
    '{{ article.target_persona|safe }}',
    content
)

# Fix lines 43-44: {{ article.updated_at|date:"F Y" }}
content = re.sub(
    r'\{\{\s*\n?\s*article\.updated_at\|date:"F Y"\s*\}\}',
    '{{ article.updated_at|date:"F Y" }}',
    content
)

# Fix {{ article.author.display_name }}
content = re.sub(
    r'\{\{\s*article\.author\.display_name\s*\}\}',
    '{{ article.author.display_name }}',
    content
)

# Fix {{ article.category.name }}
content = re.sub(
    r'\{\{\s*article\.category\.name\s*\}\}',
    '{{ article.category.name }}',
    content
)

# Fix related articles - {{ related.category.name }}
content = re.sub(
    r'\{\{\s*\n?\s*related\.category\.name\s*\}\}',
    '{{ related.category.name }}',
    content
)

# Fix {{ cat.name }}
content = re.sub(
    r'\{\{\s*\n?\s*cat\.name\s*\}\}',
    '{{ cat.name }}',
    content
)

# Fix {{ related.common_expectation...
content = re.sub(
    r'\{\{\s*\n?\s*related\.common_expectation\|striptags\|truncatewords:12\s*\}\}',
    '{{ related.common_expectation|striptags|truncatewords:12 }}',
    content
)

# Write back
with open('templates/content/article_detail.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Template tags fixed!')
