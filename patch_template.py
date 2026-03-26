import os
article_path = r"c:\Users\pmish\Downloads\career_reality\templates\content\article_detail.html"

with open(article_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add get_current_language to top level
if "{% get_current_language as LANGUAGE_CODE %}" not in content:
    content = content.replace("{% block content %}", "{% block content %}\n{% get_current_language as LANGUAGE_CODE %}")

# Macro template replacement helper
def replace_tag(field_name):
    target = "{{ article." + field_name + " }}"
    safe_target = "{{ article." + field_name + "|safe }}"
    
    # Replacement block prefers Hindi if language is Hindi and value exists
    replacement = "{% if LANGUAGE_CODE == 'hi' and article." + field_name + "_hi %}{{ article." + field_name + "_hi }}{% else %}{{ article." + field_name + " }}{% endif %}"
    safe_replacement = "{% if LANGUAGE_CODE == 'hi' and article." + field_name + "_hi %}{{ article." + field_name + "_hi|safe }}{% else %}{{ article." + field_name + "|safe }}{% endif %}"
    
    global content
    content = content.replace(safe_target, safe_replacement)
    content = content.replace(target, replacement)

# Replace fields dynamically
fields = [
    "title", "target_persona", "who_should_avoid", "common_expectation", 
    "actual_reality", "salary_reality", "stuck_point", "verdict", "meta_title", "meta_description"
]

for field in fields:
    replace_tag(field)

# Also update category name dynamically
cat_target = "{{ article.category.name }}"
cat_replacement = "{% if LANGUAGE_CODE == 'hi' and article.category.name_hi %}{{ article.category.name_hi }}{% else %}{{ article.category.name }}{% endif %}"
content = content.replace(cat_target, cat_replacement)

with open(article_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Article template successfully patched for Hindi!")
