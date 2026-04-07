"""
scripts/seed_products.py

Seeds the Razorpay Product catalog into the database.
Run once before going live:

    python scripts/seed_products.py
"""

import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("SECRET_KEY", "seed-script-key")
os.environ.setdefault("DEBUG", "True")

django.setup()

from payments.models import Product  # noqa: E402

PRODUCTS = [
    {
        "name": "Personalized Exit Checklist",
        "slug": "exit-checklist",
        "short_description": "7-day personalized exit plan for your exact situation. Includes F&F sheet, PIP templates, and communication scripts.",
        "price_paise": 9900,  # ₹99
        "product_type": "one_time",
    },
    {
        "name": "Career Reality Pro",
        "slug": "pro-monthly",
        "short_description": "Full salary database, layoff alerts, AI-personalized reports, and all premium tools. Billed monthly.",
        "price_paise": 29900,  # ₹299
        "product_type": "subscription_monthly",
    },
    {
        "name": "Career Reality Team",
        "slug": "team-monthly",
        "short_description": "5 seats, HR/recruiter salary dashboard, company-level layoff signal aggregation.",
        "price_paise": 99900,  # ₹999
        "product_type": "subscription_monthly",
    },
]


def seed():
    for p in PRODUCTS:
        obj, created = Product.objects.update_or_create(
            slug=p["slug"],
            defaults={
                "name": p["name"],
                "short_description": p["short_description"],
                "price_paise": p["price_paise"],
                "product_type": p["product_type"],
                "is_active": True,
            },
        )
        status = "created" if created else "updated"
        print(f"  {status}: {obj.name} — ₹{obj.price_rupees}")

    print(f"\n✓ {Product.objects.count()} products in catalog.")


if __name__ == "__main__":
    seed()
