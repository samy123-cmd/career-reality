import os
import django
import json

# Force local SQLite (no DATABASE_URL)
if 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from django.core.management import call_command
from io import StringIO

print("Exporting data from LOCAL SQLite database...")

# Export data
output = StringIO()
call_command(
    'dumpdata',
    '--natural-foreign',
    '--natural-primary',
    '-e', 'contenttypes',
    '-e', 'auth.Permission',
    '--indent', '2',
    stdout=output
)

# Save to file
with open('data_export.json', 'w', encoding='utf-8') as f:
    f.write(output.getvalue())

print(f"Exported to data_export.json ({len(output.getvalue())} bytes)")

# Count records
data = json.loads(output.getvalue())
print(f"Total records: {len(data)}")

# Count by model
models = {}
for item in data:
    model = item.get('model', 'unknown')
    models[model] = models.get(model, 0) + 1

print("\nRecords by model:")
for model, count in sorted(models.items()):
    print(f"  {model}: {count}")
