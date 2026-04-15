import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()

from django.core import serializers
from analyzer.models import SalarySubmission

data = serializers.serialize('json', SalarySubmission.objects.all(), indent=2, ensure_ascii=True)
with open('salary_export.json', 'w', encoding='utf-8') as f:
    f.write(data)
print(f'Done: {SalarySubmission.objects.count()} salary submissions exported')
