"""Django signals for analyzer app."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from analyzer.models import SalarySubmission, LayoffReport


@receiver(post_save, sender=SalarySubmission)
def sync_company_on_salary_submit(sender, instance, **kwargs):
    company = instance.company
    if not company and instance.company_name:
        from companies.models import Company
        company = Company.objects.filter(name__iexact=instance.company_name).first()
    if company:
        from companies.stats import sync_company_stats
        sync_company_stats(company)


@receiver(post_save, sender=LayoffReport)
def sync_company_on_layoff_report(sender, instance, **kwargs):
    company = instance.company
    if not company and instance.company_name:
        from companies.models import Company
        company = Company.objects.filter(name__iexact=instance.company_name).first()
    if company:
        from companies.stats import sync_company_stats
        sync_company_stats(company)
