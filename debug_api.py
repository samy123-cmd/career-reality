import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from analyzer import models

def test_api_logic():
    print("Testing Salary Feed API Logic...")
    try:
        submissions = models.SalarySubmission.objects.all().order_by('-created_at')[:20]
        print(f"Found {submissions.count()} submissions.")
        
        data = []
        for s in submissions:
            print(f"Processing: {s}")
            item = {
                'role': s.role,
                'company': s.get_company_type_display(), # or short code
                'exp': f"{s.experience_years}y",
                'ctc': f"{s.ctc/100000:.1f} LPA",
                'city': s.city
            }
            data.append(item)
            
        print("Success! Data:")
        print(data)
    except Exception as e:
        print(f"FAILED with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_logic()
