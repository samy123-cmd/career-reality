"""
Management command: refresh_career_index
Computes or updates the CareerRealityIndexSnapshot for the current month
using live data from SalarySubmission, LayoffReport, and CompanyReview.

Run via cron or after significant data imports:
    python manage.py refresh_career_index
"""
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db.models import Avg, Count, Q
from django.utils import timezone

from core.career_index_data import IndexBaseline, blend_with_baseline, editorial_baseline
from core.cache_utils import invalidate_career_index_cache
from core.models import CareerRealityIndexSnapshot


class Command(BaseCommand):
    help = "Compute and store the Career Reality Index from live crowdsourced data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--months", type=int, default=4,
            help="Number of past months to (re)compute. Default: 4"
        )

    def handle(self, *args, **options):
        from analyzer.models import SalarySubmission, LayoffReport
        from companies.models import CompanyReview

        months_back = options["months"]
        today = timezone.localdate()

        for i in range(months_back):
            # Derive month window
            year = today.year
            month = today.month - i
            while month <= 0:
                month += 12
                year -= 1
            month_start = date(year, month, 1)
            # End = last day of this month
            if month == 12:
                month_end = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                month_end = date(year, month + 1, 1) - timedelta(days=1)

            month_label = month_start.strftime("%B %Y")

            # --- Salary Pressure ---
            # Look at last 90 days rolling for more stable signal
            window_start = month_end - timedelta(days=90)
            sal_qs = SalarySubmission.objects.filter(
                created_at__date__gte=window_start,
                created_at__date__lte=month_end,
            )
            sal_count = sal_qs.count()

            # Proxy for stagnation: service-based companies with < 5yr exp
            # have notoriously low CTCs. We use % of service submissions as pressure signal.
            if sal_count > 0:
                service_count = sal_qs.filter(company_type="service").count()
                # Median CTC below ₹10L is "pressure" in a product market
                low_ctc_count = sal_qs.filter(ctc__lt=1_000_000).count()
                salary_pressure = min(
                    100,
                    int(((service_count * 0.5) + (low_ctc_count * 0.5)) / sal_count * 100) + 50
                )
                # Clamp to realistic range 40-95
                salary_pressure = max(40, min(95, salary_pressure))
            else:
                salary_pressure = 65  # Fallback to baseline

            # --- Layoff Risk ---
            layoff_qs = LayoffReport.objects.filter(
                created_at__date__gte=month_start,
                created_at__date__lte=month_end,
            )
            layoff_count = layoff_qs.count()
            if layoff_count > 0:
                danger_count = layoff_qs.filter(
                    status__in=["layoff", "rumor", "freeze"]
                ).count()
                layoff_risk = min(95, int(danger_count / layoff_count * 100))
                layoff_risk = max(20, layoff_risk)
            else:
                layoff_risk = 40  # Fallback

            # --- Switch Difficulty ---
            switch_difficulty = min(95, int((salary_pressure * 0.4 + layoff_risk * 0.6)))
            switch_difficulty = max(30, switch_difficulty)

            review_count = CompanyReview.objects.filter(
                created_at__date__gte=month_start,
                created_at__date__lte=month_end,
            ).count()

            computed = IndexBaseline(
                salary_pressure=salary_pressure,
                switch_difficulty=switch_difficulty,
                layoff_risk=layoff_risk,
            )

            # Blend with editorial baseline when we have a calibrated monthly trend.
            baseline = editorial_baseline(year, month)
            if baseline:
                data_points = sal_count + layoff_count + review_count
                data_weight = min(0.7, data_points / 50)
                blended = blend_with_baseline(computed, baseline, data_weight=data_weight)
                salary_pressure = blended.salary_pressure
                switch_difficulty = blended.switch_difficulty
                layoff_risk = blended.layoff_risk

            overall = int(salary_pressure * 0.35 + switch_difficulty * 0.35 + layoff_risk * 0.30)

            snapshot, created = CareerRealityIndexSnapshot.objects.update_or_create(
                month_date=month_start,
                defaults={
                    "month": month_label,
                    "salary_pressure": salary_pressure,
                    "switch_difficulty": switch_difficulty,
                    "layoff_risk": layoff_risk,
                    "overall": overall,
                    "total_salary_submissions": sal_count,
                    "total_layoff_reports": layoff_count,
                    "total_reviews": review_count,
                },
            )
            action = "Created" if created else "Updated"
            self.stdout.write(
                self.style.SUCCESS(
                    f"{action} index for {month_label}: "
                    f"salary={salary_pressure}, switch={switch_difficulty}, "
                    f"layoff={layoff_risk}, overall={overall}"
                )
            )

        invalidate_career_index_cache()
        self.stdout.write(self.style.SUCCESS("Career Reality Index refresh complete."))
