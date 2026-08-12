"""Signals for companies app."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from companies.models import CompanyReview


@receiver(post_save, sender=CompanyReview)
def sync_company_on_review(sender, instance, **kwargs):
    from companies.stats import sync_company_stats
    sync_company_stats(instance.company)
