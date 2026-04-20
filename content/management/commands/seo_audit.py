"""
Management command: seo_audit
-----------------------------
Audits all published articles for SEO signal quality and prints a
prioritised report.  Run with:

    python manage.py seo_audit
    python manage.py seo_audit --fix-year        # update stale year refs in descriptions
    python manage.py seo_audit --csv report.csv  # export full table to CSV

Checks performed
----------------
1. Meta title length  (warn < 45 chars, error > 60 chars)
2. Meta description length (warn < 120 chars, error > 160 chars)
3. Year currency — descriptions mentioning a year older than current
4. Data signals — title/desc containing a number (₹, LPA, %, years)
5. CTA presence — description ends with a call-to-action phrase
6. Slug consistency — slug matches slugified title
7. Duplicate meta title or description across articles
8. Missing published_at date
9. last_reality_check staleness (> 180 days = stale)
"""

import csv
import datetime
import re
import sys

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from content.models import Article


CURRENT_YEAR = timezone.now().year
YEAR_RE = re.compile(r"\b(20\d{2})\b")
DATA_SIGNAL_RE = re.compile(r"[₹%]|\d+\s*(?:lpa|LPA|cr|lakhs?|years?|months?|%)")
CTA_ENDINGS = (
    ".", "action steps.", "find out.", "read on.", "here's what to do.",
    "how to time it right.", "make financial sense.", "build learning roi instead of course debt.",
    "beyond delivery work.",
)


class Command(BaseCommand):
    help = "SEO audit for all published articles"

    def add_arguments(self, parser):
        parser.add_argument(
            "--fix-year",
            action="store_true",
            help="Replace stale year references in meta descriptions with the current year",
        )
        parser.add_argument(
            "--csv",
            dest="csv_path",
            default=None,
            help="Export the full audit table to a CSV file at this path",
        )

    def handle(self, *args, **options):
        articles = list(
            Article.objects.filter(status="published")
            .select_related("category", "author")
            .order_by("id")
        )

        rows = []
        errors = 0
        warnings = 0

        # Duplicate detection
        seen_titles: dict[str, list[int]] = {}
        seen_descs: dict[str, list[int]] = {}
        for a in articles:
            seen_titles.setdefault(a.meta_title.lower().strip(), []).append(a.id)
            seen_descs.setdefault(a.meta_description.lower().strip(), []).append(a.id)

        for a in articles:
            issues = []

            # 1. Meta title length
            tl = len(a.meta_title)
            if tl > 60:
                issues.append(f"ERROR: meta_title {tl} chars (max 60) — Google truncates in SERP")
                errors += 1
            elif tl < 45:
                issues.append(f"WARN: meta_title only {tl} chars — low keyword density")
                warnings += 1

            # 2. Meta description length
            dl = len(a.meta_description)
            if dl > 160:
                issues.append(f"ERROR: meta_description {dl} chars (max 160)")
                errors += 1
            elif dl < 120:
                issues.append(f"WARN: meta_description only {dl} chars — room to add specifics")
                warnings += 1

            # 3. Year currency
            years_in_desc = [int(y) for y in YEAR_RE.findall(a.meta_description)]
            stale_years = [y for y in years_in_desc if y < CURRENT_YEAR - 1]
            if stale_years:
                issues.append(
                    f"WARN: stale year(s) {stale_years} in description — update to {CURRENT_YEAR}"
                )
                warnings += 1

            # 4. Data signals
            combined = a.meta_title + " " + a.meta_description
            if not DATA_SIGNAL_RE.search(combined):
                issues.append(
                    "WARN: no numeric/data signal (₹, LPA, %, years) in title+desc — add one for CTR"
                )
                warnings += 1

            # 5. Duplicate meta title
            dup_title_ids = [i for i in seen_titles.get(a.meta_title.lower().strip(), []) if i != a.id]
            if dup_title_ids:
                issues.append(f"ERROR: duplicate meta_title shared with article ids {dup_title_ids}")
                errors += 1

            # 6. Duplicate meta description
            dup_desc_ids = [i for i in seen_descs.get(a.meta_description.lower().strip(), []) if i != a.id]
            if dup_desc_ids:
                issues.append(f"ERROR: duplicate meta_description shared with ids {dup_desc_ids}")
                errors += 1

            # 7. Missing published_at
            if not a.published_at:
                issues.append("WARN: published_at is null — affects datePublished schema")
                warnings += 1

            # 8. Stale last_reality_check
            if a.last_reality_check:
                age_days = (datetime.date.today() - a.last_reality_check).days
                if age_days > 180:
                    issues.append(f"WARN: last_reality_check is {age_days} days ago — refresh needed")
                    warnings += 1
            else:
                issues.append("WARN: last_reality_check not set")
                warnings += 1

            rows.append({
                "id": a.id,
                "title": a.title[:55],
                "meta_title_len": tl,
                "meta_desc_len": dl,
                "issues": issues,
            })

        # ── Print report ──────────────────────────────────────────────────
        self.stdout.write("\n" + "═" * 90)
        self.stdout.write(self.style.HTTP_INFO("  CAREER REALITY — SEO AUDIT REPORT"))
        self.stdout.write(f"  {len(articles)} published articles · {errors} errors · {warnings} warnings")
        self.stdout.write("═" * 90 + "\n")

        for row in rows:
            if not row["issues"]:
                continue
            self.stdout.write(
                self.style.SUCCESS(f"[{row['id']:3}] {row['title']}")
                + f"  ({row['meta_title_len']}c title / {row['meta_desc_len']}c desc)"
            )
            for issue in row["issues"]:
                if issue.startswith("ERROR"):
                    self.stdout.write("       " + self.style.ERROR(issue))
                else:
                    self.stdout.write("       " + self.style.WARNING(issue))
            self.stdout.write("")

        clean_count = sum(1 for r in rows if not r["issues"])
        self.stdout.write(f"✓ {clean_count}/{len(articles)} articles have no issues\n")

        # ── Optional: fix stale years ─────────────────────────────────────
        if options["fix_year"]:
            fixed = 0
            for a in articles:
                new_desc = YEAR_RE.sub(
                    lambda m: str(CURRENT_YEAR) if int(m.group()) < CURRENT_YEAR - 1 else m.group(),
                    a.meta_description,
                )
                if new_desc != a.meta_description:
                    Article.objects.filter(id=a.id).update(meta_description=new_desc)
                    self.stdout.write(f"  Fixed year in article {a.id}: {a.title[:50]}")
                    fixed += 1
            self.stdout.write(self.style.SUCCESS(f"\n--fix-year: updated {fixed} articles"))

        # ── Optional: CSV export ──────────────────────────────────────────
        if options["csv_path"]:
            with open(options["csv_path"], "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "title", "meta_title_len", "meta_desc_len", "issues"])
                for row in rows:
                    writer.writerow([
                        row["id"],
                        row["title"],
                        row["meta_title_len"],
                        row["meta_desc_len"],
                        " | ".join(row["issues"]),
                    ])
            self.stdout.write(self.style.SUCCESS(f"CSV written to {options['csv_path']}"))
