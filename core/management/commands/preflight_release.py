from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Validate production-critical settings before release."

    def add_arguments(self, parser):
        parser.add_argument(
            "--strict",
            action="store_true",
            help="Fail with non-zero exit code if any blocking issue is found.",
        )

    def handle(self, *args, **options):
        strict = options["strict"]
        issues = []
        warnings = []

        if settings.DEBUG:
            issues.append("DEBUG=True (must be False in production).")

        if not settings.ALLOWED_HOSTS:
            issues.append("ALLOWED_HOSTS is empty.")

        if not getattr(settings, "SECURE_SSL_REDIRECT", False):
            issues.append("SECURE_SSL_REDIRECT is not enabled.")

        if not getattr(settings, "SESSION_COOKIE_SECURE", False):
            issues.append("SESSION_COOKIE_SECURE is not enabled.")

        if not getattr(settings, "CSRF_COOKIE_SECURE", False):
            issues.append("CSRF_COOKIE_SECURE is not enabled.")

        hsts_seconds = int(getattr(settings, "SECURE_HSTS_SECONDS", 0) or 0)
        if hsts_seconds <= 0:
            warnings.append("SECURE_HSTS_SECONDS is not set (>0 recommended for HTTPS-only deployments).")

        if issues:
            self.stdout.write(self.style.ERROR("Release preflight: BLOCKING ISSUES"))
            for issue in issues:
                self.stdout.write(self.style.ERROR(f" - {issue}"))
        else:
            self.stdout.write(self.style.SUCCESS("Release preflight: no blocking issues found."))

        if warnings:
            self.stdout.write(self.style.WARNING("Release preflight: WARNINGS"))
            for warning in warnings:
                self.stdout.write(self.style.WARNING(f" - {warning}"))

        if strict and issues:
            raise CommandError("Preflight failed with blocking issues.")
