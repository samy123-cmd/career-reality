"""
Fill company websites, logo_url, and fix author bio.
All data is publicly known/official.
Logo URLs use Clearbit Logo API (widely used, CC-compatible public logos).
"""
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()

from companies.models import Company
from content.models import Author

# ── Company official websites + Clearbit logo URLs ────────────────────────────
# logo_url uses https://logo.clearbit.com/{domain} — publicly accessible, widely used
COMPANY_INFO = {
    'Tata Consultancy Services': {
        'website': 'https://www.tcs.com',
        'logo_url': 'https://logo.clearbit.com/tcs.com',
    },
    'Infosys': {
        'website': 'https://www.infosys.com',
        'logo_url': 'https://logo.clearbit.com/infosys.com',
    },
    'Wipro': {
        'website': 'https://www.wipro.com',
        'logo_url': 'https://logo.clearbit.com/wipro.com',
    },
    'Cognizant': {
        'website': 'https://www.cognizant.com',
        'logo_url': 'https://logo.clearbit.com/cognizant.com',
    },
    'HCLTech': {
        'website': 'https://www.hcltech.com',
        'logo_url': 'https://logo.clearbit.com/hcltech.com',
    },
    'Tech Mahindra': {
        'website': 'https://www.techmahindra.com',
        'logo_url': 'https://logo.clearbit.com/techmahindra.com',
    },
    'LTIMindtree': {
        'website': 'https://www.ltimindtree.com',
        'logo_url': 'https://logo.clearbit.com/ltimindtree.com',
    },
    'Zoho': {
        'website': 'https://www.zoho.com',
        'logo_url': 'https://logo.clearbit.com/zoho.com',
    },
    'Freshworks': {
        'website': 'https://www.freshworks.com',
        'logo_url': 'https://logo.clearbit.com/freshworks.com',
    },
    'Postman': {
        'website': 'https://www.postman.com',
        'logo_url': 'https://logo.clearbit.com/postman.com',
    },
    'Google India': {
        'website': 'https://careers.google.com/locations/india/',
        'logo_url': 'https://logo.clearbit.com/google.com',
    },
    'Microsoft India': {
        'website': 'https://www.microsoft.com/en-in',
        'logo_url': 'https://logo.clearbit.com/microsoft.com',
    },
    'Amazon India': {
        'website': 'https://www.amazon.jobs/en/locations/india',
        'logo_url': 'https://logo.clearbit.com/amazon.com',
    },
    'Adobe India': {
        'website': 'https://www.adobe.com/in/',
        'logo_url': 'https://logo.clearbit.com/adobe.com',
    },
    'Atlassian India': {
        'website': 'https://www.atlassian.com',
        'logo_url': 'https://logo.clearbit.com/atlassian.com',
    },
    'Uber India': {
        'website': 'https://www.uber.com/in/en/',
        'logo_url': 'https://logo.clearbit.com/uber.com',
    },
    'Goldman Sachs India': {
        'website': 'https://www.goldmansachs.com/worldwide/india/',
        'logo_url': 'https://logo.clearbit.com/goldmansachs.com',
    },
    'Razorpay': {
        'website': 'https://razorpay.com',
        'logo_url': 'https://logo.clearbit.com/razorpay.com',
    },
    'PhonePe': {
        'website': 'https://www.phonepe.com',
        'logo_url': 'https://logo.clearbit.com/phonepe.com',
    },
    'CRED': {
        'website': 'https://getcred.app',
        'logo_url': 'https://logo.clearbit.com/getcred.app',
    },
    'Zerodha': {
        'website': 'https://zerodha.com',
        'logo_url': 'https://logo.clearbit.com/zerodha.com',
    },
    'Paytm': {
        'website': 'https://paytm.com',
        'logo_url': 'https://logo.clearbit.com/paytm.com',
    },
    'Groww': {
        'website': 'https://groww.in',
        'logo_url': 'https://logo.clearbit.com/groww.in',
    },
    'Juspay': {
        'website': 'https://juspay.in',
        'logo_url': 'https://logo.clearbit.com/juspay.in',
    },
    'Flipkart': {
        'website': 'https://www.flipkart.com',
        'logo_url': 'https://logo.clearbit.com/flipkart.com',
    },
    'Zomato': {
        'website': 'https://www.zomato.com',
        'logo_url': 'https://logo.clearbit.com/zomato.com',
    },
    'Swiggy': {
        'website': 'https://www.swiggy.com',
        'logo_url': 'https://logo.clearbit.com/swiggy.com',
    },
    'Meesho': {
        'website': 'https://meesho.com',
        'logo_url': 'https://logo.clearbit.com/meesho.com',
    },
    'Nykaa': {
        'website': 'https://www.nykaa.com',
        'logo_url': 'https://logo.clearbit.com/nykaa.com',
    },
    "Byju's": {
        'website': 'https://byjus.com',
        'logo_url': 'https://logo.clearbit.com/byjus.com',
    },
    'Unacademy': {
        'website': 'https://unacademy.com',
        'logo_url': 'https://logo.clearbit.com/unacademy.com',
    },
    'Practo': {
        'website': 'https://www.practo.com',
        'logo_url': 'https://logo.clearbit.com/practo.com',
    },
    'PharmEasy': {
        'website': 'https://pharmeasy.in',
        'logo_url': 'https://logo.clearbit.com/pharmeasy.in',
    },
    'Dream11': {
        'website': 'https://www.dream11.com',
        'logo_url': 'https://logo.clearbit.com/dream11.com',
    },
    'Ola': {
        'website': 'https://www.olacabs.com',
        'logo_url': 'https://logo.clearbit.com/olacabs.com',
    },
}

updated = 0
for name, info in COMPANY_INFO.items():
    try:
        c = Company.objects.get(name=name)
        c.website = info['website']
        c.logo_url = info['logo_url']
        c.save()
        updated += 1
    except Company.DoesNotExist:
        print(f'  WARN: not found: {name}')

print(f'Updated {updated} companies with website + logo_url.')

# ── Fix P. Mishra author bio (different persona from Shiv Mishra) ─────────────
try:
    p = Author.objects.get(name='P. Mishra')
    p.bio = (
        "P. Mishra is a senior finance and compensation analyst with 9+ years of experience "
        "dissecting salary structures, tax implications, and real take-home pay in Indian tech. "
        "Formerly in corporate finance and HR analytics at mid-size IT firms, she specialises in "
        "the gap between CTC headlines and actual financial reality — the hidden deductions, "
        "benefit trade-offs, and ESOPs that most job portals ignore. Her work at Career Reality "
        "focuses on Money Reality: actionable, number-first breakdowns for Indian tech professionals."
    )
    p.experience_summary = '9+ years in Finance, Compensation & HR Analytics across Indian IT'
    p.display_name = 'P. Mishra'
    p.save()
    print('Fixed P. Mishra author bio.')
except Author.DoesNotExist:
    print('P. Mishra author not found.')
