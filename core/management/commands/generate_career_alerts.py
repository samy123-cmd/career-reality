"""
Generate personalized career risk alerts for Pro users.
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q

from accounts.models import CareerProfile, CareerAlert, CompanyWatchlist
from analyzer.models import LayoffReport
from analyzer.services.ai_career_impact import analyze_ai_career_impact
from analyzer.services.salary_engine import get_salary_reality
from companies.scoring import compute_company_reality_score


class Command(BaseCommand):
    help = "Generate career risk alerts for Pro users"

    def handle(self, *args, **options):
        since = timezone.now() - timedelta(hours=24)
        created = 0

        for profile in CareerProfile.objects.select_related("user", "company").filter(
            user__profile__tier__in=["pro", "team"]
        ):
            user = profile.user
            try:
                if not user.profile.is_pro:
                    continue
            except Exception:
                continue

            # Layoff/freeze alerts for user's company
            if profile.company:
                reports = LayoffReport.objects.filter(
                    Q(company=profile.company) | Q(company_name__iexact=profile.company.name),
                    created_at__gte=since,
                    status__in=["freeze", "rumor", "layoff"],
                )
                for report in reports:
                    if not CareerAlert.objects.filter(
                        user=user,
                        alert_type="layoff" if report.status == "layoff" else "freeze",
                        message__icontains=profile.company.name,
                        created_at__gte=since,
                    ).exists():
                        CareerAlert.objects.create(
                            user=user,
                            alert_type="layoff" if report.status == "layoff" else "freeze",
                            severity="critical" if report.status == "layoff" else "warning",
                            message=f"{profile.company.name}: {report.get_status_display()} reported.",
                            source_url=f"/companies/{profile.company.slug}/",
                        )
                        created += 1

            # Salary stagnation — no raise signal (simplified: underpaid for 12+ months)
            if profile.current_ctc and profile.role:
                salary = get_salary_reality(
                    profile.role,
                    float(profile.experience_years or 5),
                    profile.city or "Bengaluru",
                    profile.company_type or "",
                    current_ctc=profile.current_ctc,
                )
                if salary.pay_label == "underpaid" and salary.pay_delta_pct and salary.pay_delta_pct < -15:
                    if not CareerAlert.objects.filter(
                        user=user,
                        alert_type="salary_stagnation",
                        created_at__gte=timezone.now() - timedelta(days=30),
                    ).exists():
                        CareerAlert.objects.create(
                            user=user,
                            alert_type="salary_stagnation",
                            severity="warning",
                            message=(
                                f"You may be underpaid by ~{abs(salary.pay_delta_pct)}% vs market. "
                                f"Median for your band: ₹{salary.p50}L."
                            ),
                            source_url="/tools/salary-reality-engine/",
                        )
                        created += 1

            # AI disruption alert
            title = profile.title or profile.role
            if title:
                ai = analyze_ai_career_impact(title)
                if ai.ai_risk_score >= 70:
                    if not CareerAlert.objects.filter(
                        user=user,
                        alert_type="ai_disruption",
                        created_at__gte=timezone.now() - timedelta(days=30),
                    ).exists():
                        CareerAlert.objects.create(
                            user=user,
                            alert_type="ai_disruption",
                            severity="warning",
                            message=f"High AI exposure ({ai.ai_risk_score}/100) for {title}. Consider upskilling.",
                            source_url="/tools/ai-career-impact/",
                        )
                        created += 1

        # Watchlist layoff alerts (reuse watchlist)
        for watch in CompanyWatchlist.objects.select_related("user", "company"):
            user = watch.user
            try:
                if not user.profile.is_pro:
                    continue
            except Exception:
                continue
            reports = LayoffReport.objects.filter(
                Q(company=watch.company) | Q(company_name__iexact=watch.company.name),
                created_at__gte=since,
                status__in=["freeze", "rumor", "layoff"],
            )
            for report in reports:
                if not CareerAlert.objects.filter(
                    user=user,
                    message__icontains=watch.company.name,
                    created_at__gte=since,
                ).exists():
                    CareerAlert.objects.create(
                        user=user,
                        alert_type="layoff" if report.status == "layoff" else "freeze",
                        severity="critical" if report.status == "layoff" else "warning",
                        message=f"Watchlist alert: {watch.company.name} — {report.get_status_display()}.",
                        source_url=f"/companies/{watch.company.slug}/",
                    )
                    created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} career alerts."))
