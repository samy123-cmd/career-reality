"""
management command: send_weekly_digest

Send the weekly newsletter digest to all active subscribers.
Called from cron (vercel.json or external scheduler).

Usage:
    python manage.py send_weekly_digest
"""

import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Send the weekly career reality digest to newsletter subscribers."

    def handle(self, *args, **options):
        from core.models import NewsletterSubscriber
        from core.email import send_weekly_digest
        from analyzer.models import SalarySubmission, LayoffReport

        # Count new data points from last 7 days
        week_ago = timezone.now() - timedelta(days=7)
        salary_count = SalarySubmission.objects.filter(created_at__gte=week_ago).count()
        layoff_count = LayoffReport.objects.filter(created_at__gte=week_ago).count()

        subscribers = list(
            NewsletterSubscriber.objects.filter(is_active=True).values_list("email", flat=True)
        )

        if not subscribers:
            self.stdout.write("No active subscribers. Nothing sent.")
            return

        self.stdout.write(
            f"Sending digest to {len(subscribers)} subscribers "
            f"({salary_count} new salaries, {layoff_count} layoff reports)..."
        )

        sent = send_weekly_digest(subscribers, salary_count, layoff_count)

        self.stdout.write(self.style.SUCCESS(f"✓ Sent {sent}/{len(subscribers)} digest emails."))
