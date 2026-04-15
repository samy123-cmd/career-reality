import os
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
import django
django.setup()
from urllib.parse import quote
from companies.models import Company

SECTOR_COLORS = {
    "service":     "2563EB",
    "product":     "7C3AED",
    "mnc_captive": "0F766E",
    "bfsi":        "B45309",
    "ecommerce":   "DC2626",
    "edtech":      "16A34A",
    "healthtech":  "0284C7",
    "other":       "475569",
}

updated = 0
for c in Company.objects.all():
    color = SECTOR_COLORS.get(c.sector, "374151")
    name_encoded = quote(c.name)
    c.logo_url = f"https://ui-avatars.com/api/?name={name_encoded}&size=64&background={color}&color=ffffff&bold=true&length=2&format=svg"
    c.save()
    updated += 1

print(f"Updated {updated} companies with ui-avatars URLs.")
