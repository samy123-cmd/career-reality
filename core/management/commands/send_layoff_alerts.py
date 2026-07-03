"""
management command: send_layoff_alerts

Sends Pro watchlist layoff alert emails for recent danger-status reports.
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import CompanyWatchlist, LayoffAlertLog
from analyzer.models import LayoffReport
from core.email import send_layoff_watchlist_alert


class Command(BaseCommand):
    help = "Send layoff watchlist alerts to Pro subscribers"

    def handle(self, *args, **options):
        since = timezone.now() - timedelta(hours=24)
        alert_statuses = ["freeze", "rumor", "layoff"]

        recent_reports = LayoffReport.objects.filter(
            created_at__gte=since,
            status__in=alert_statuses,
        ).select_related("company")

        if not recent_reports.exists():
            self.stdout.write("No recent layoff reports to alert on.")
            return

        sent_count = 0
        for watch in CompanyWatchlist.objects.select_related("user", "company"):
            user = watch.user
            try:
                if not user.profile.is_pro:
                    continue
            except Exception:
                continue

            company = watch.company
            matching = [
                r for r in recent_reports
                if (r.company_id == company.id)
                or (r.company_name and r.company_name.lower() == company.name.lower())
            ]
            if not matching:
                continue

            to_send = []
            for report in matching:
                if LayoffAlertLog.objects.filter(user=user, layoff_report=report).exists():
                    continue
                to_send.append(report)

            if not to_send:
                continue

            if send_layoff_watchlist_alert(user.email, company, to_send):
                for report in to_send:
                    LayoffAlertLog.objects.get_or_create(user=user, layoff_report=report)
                sent_count += 1
                self.stdout.write(f"Alert sent to {user.email} for {company.name}")

        self.stdout.write(self.style.SUCCESS(f"Done. {sent_count} alert emails sent."))
