from __future__ import annotations

from datetime import datetime
from typing import Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand
from django.utils import timezone

from ainews.models import AINewsItem


def _probe_url(url: str, timeout: int) -> Tuple[bool, str]:
    if not url:
        return False, "missing_url"

    try:
        request = Request(url, method="HEAD", headers={"User-Agent": "CareerRealityBot/1.0"})
        with urlopen(request, timeout=timeout) as response:
            status_code = getattr(response, "status", 200)
            return 200 <= status_code < 400, f"status_{status_code}"
    except HTTPError as exc:
        if exc.code in (403, 405):
            try:
                request = Request(url, method="GET", headers={"User-Agent": "CareerRealityBot/1.0"})
                with urlopen(request, timeout=timeout) as response:
                    status_code = getattr(response, "status", 200)
                    return 200 <= status_code < 400, f"status_{status_code}"
            except Exception as fallback_exc:
                return False, f"{type(fallback_exc).__name__}:{fallback_exc}"
        return False, f"HTTPError:{exc.code}"
    except URLError as exc:
        return False, f"URLError:{exc.reason}"
    except Exception as exc:
        return False, f"{type(exc).__name__}:{exc}"


class Command(BaseCommand):
    help = "Verify AI news source URL reachability and update review metadata."

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            action="store_true",
            help="Persist verification updates to DB. Without this, runs in dry-run mode.",
        )
        parser.add_argument(
            "--set-verified",
            action="store_true",
            help="When URL probe succeeds, set fact_check_status='verified'.",
        )
        parser.add_argument(
            "--include-drafts",
            action="store_true",
            help="Include draft items as well. Default verifies only published items.",
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=10,
            help="Timeout in seconds for URL probe requests.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Optional max number of items to process (0 = all).",
        )

    def handle(self, *args, **options):
        commit = options["commit"]
        set_verified = options["set_verified"]
        include_drafts = options["include_drafts"]
        timeout = options["timeout"]
        limit = options["limit"]

        queryset = AINewsItem.objects.all().order_by("-published_at", "-fetched_at")
        if not include_drafts:
            queryset = queryset.filter(status="published")
        if limit and limit > 0:
            queryset = queryset[:limit]

        checked = 0
        reachable = 0
        unreachable = 0
        updated = 0

        now = timezone.now()
        stamp = now.strftime("%Y-%m-%d %H:%M:%S %Z")

        self.stdout.write(self.style.NOTICE("Starting AI source verification pass"))
        self.stdout.write(f"Mode: {'commit' if commit else 'dry-run'}")
        self.stdout.write(f"Target set: {'all statuses' if include_drafts else 'published only'}")

        for item in queryset:
            checked += 1
            ok, reason = _probe_url(item.source_url, timeout=timeout)
            if ok:
                reachable += 1
                self.stdout.write(self.style.SUCCESS(f"[OK] {item.slug} ({reason})"))
                if commit:
                    update_fields = ["reviewed_at", "last_verified_at", "review_notes"]
                    item.reviewed_at = now
                    item.last_verified_at = now
                    item.review_notes = (
                        (item.review_notes or "").strip() + "\n"
                        + f"[{stamp}] Automated source reachability check passed ({reason})."
                    ).strip()
                    if set_verified and item.fact_check_status != "verified":
                        item.fact_check_status = "verified"
                        update_fields.append("fact_check_status")
                    item.save(update_fields=update_fields)
                    updated += 1
            else:
                unreachable += 1
                self.stdout.write(self.style.WARNING(f"[FAIL] {item.slug} ({reason})"))
                if commit:
                    item.review_notes = (
                        (item.review_notes or "").strip() + "\n"
                        + f"[{stamp}] Automated source reachability check failed ({reason})."
                    ).strip()
                    item.save(update_fields=["review_notes"])

        self.stdout.write("")
        self.stdout.write(self.style.NOTICE("Verification summary"))
        self.stdout.write(f"- Items checked: {checked}")
        self.stdout.write(f"- Reachable sources: {reachable}")
        self.stdout.write(f"- Unreachable sources: {unreachable}")
        self.stdout.write(f"- Items updated: {updated}")
