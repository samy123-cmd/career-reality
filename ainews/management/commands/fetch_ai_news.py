import logging
import re
from datetime import datetime, timezone as dt_timezone
from urllib.request import Request, urlopen

import feedparser
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from ainews.impact_filters import passes_ingest_filter
from ainews.models import AINewsFetchRun, AINewsItem, AITag

logger = logging.getLogger(__name__)
REQUEST_HEADERS = {'User-Agent': 'CareerRealityAIBot/1.0 (+https://careerreality.in)'}
REQUEST_TIMEOUT_SECONDS = 15

# IT workplace impact only — no research papers, model roundups, or benchmark feeds.
RSS_FEEDS = [
    {
        'name': 'VentureBeat AI',
        'url': 'https://venturebeat.com/category/ai/feed',
        'default_tags': ['Industry News'],
    },
]

TRUSTED_SOURCES: set[str] = set()


class Command(BaseCommand):
    help = 'Fetch IT workplace-impact AI news (draft only; editor publishes with career_angle).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--auto-publish',
            action='store_true',
            help='Deprecated — kept for compatibility; items always save as draft.',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=3,
            help='Maximum items per feed after filtering (default: 3).',
        )

    def handle(self, *args, **options):
        limit = options['limit']
        run = AINewsFetchRun.objects.create(source_count=len(RSS_FEEDS))
        run_notes = []

        total_created = 0
        total_skipped = 0
        total_filtered = 0
        total_errors = 0
        total_warnings = 0

        tag_cache = {}
        for feed_config in RSS_FEEDS:
            for tag_name in feed_config.get('default_tags', []):
                if tag_name not in tag_cache:
                    tag_obj, _ = AITag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': slugify(tag_name)}
                    )
                    tag_cache[tag_name] = tag_obj

        for feed_config in RSS_FEEDS:
            source_name = feed_config['name']
            feed_url = feed_config['url']
            default_tag_names = feed_config.get('default_tags', [])

            self.stdout.write(f"\n--- Fetching: {source_name} ({feed_url})")

            feed, warning = self._parse_feed_with_fallback(feed_url)
            if warning:
                self.stderr.write(self.style.WARNING(f"  Warning for {source_name}: {warning}"))
                total_warnings += 1
                run_notes.append(f"{source_name}: {warning}")

            if feed is None:
                self.stderr.write(self.style.ERROR(f"  Failed to fetch usable feed for {source_name}"))
                total_errors += 1
                run_notes.append(f"{source_name}: failed to fetch usable feed")
                continue

            kept = 0
            for entry in feed.entries:
                if kept >= limit:
                    break

                external_id = getattr(entry, 'id', None) or getattr(entry, 'link', None)
                if not external_id:
                    total_skipped += 1
                    continue

                if AINewsItem.objects.filter(external_id=external_id).exists():
                    total_skipped += 1
                    continue

                title = getattr(entry, 'title', 'Untitled')[:300]
                link = getattr(entry, 'link', '')

                summary = ''
                if hasattr(entry, 'summary'):
                    summary = entry.summary
                elif hasattr(entry, 'description'):
                    summary = entry.description

                summary = re.sub(r'<[^>]+>', '', summary or '').strip()
                summary = re.sub(r'[\r\n\t]+', ' ', summary).strip()
                if len(summary) > 1000:
                    summary = summary[:997] + '...'

                if not passes_ingest_filter(title, summary, source_name):
                    total_filtered += 1
                    self.stdout.write(f"  - filtered (not IT impact): {title[:70]}…")
                    continue

                published_dt = self._parse_entry_datetime(entry)

                slug = slugify(title)[:300]
                base_slug = slug
                counter = 1
                while AINewsItem.objects.filter(slug=slug).exists():
                    slug = f"{base_slug[:290]}-{counter}"
                    counter += 1

                try:
                    item = AINewsItem.objects.create(
                        title=title,
                        slug=slug,
                        summary=summary or f"Development from {source_name}.",
                        source_name=source_name,
                        source_url=link or feed_url,
                        status='draft',
                        fact_check_status='pending',
                        event_date=published_dt,
                        published_at=published_dt,
                        external_id=external_id,
                    )
                    for tag_name in default_tag_names:
                        if tag_name in tag_cache:
                            item.tags.add(tag_cache[tag_name])

                    total_created += 1
                    kept += 1
                    self.stdout.write(f"  + draft: {title[:80]}…")

                except Exception as exc:
                    self.stderr.write(self.style.ERROR(f"  Error saving '{title[:60]}': {exc}"))
                    total_errors += 1
                    run_notes.append(f"{source_name}: save error for '{title[:40]}' - {exc}")

        run.finished_at = timezone.now()
        run.total_created = total_created
        run.total_skipped = total_skipped + total_filtered
        run.total_warnings = total_warnings
        run.total_errors = total_errors
        if total_errors and total_created == 0:
            run.status = 'failed'
        elif total_errors:
            run.status = 'partial'
        else:
            run.status = 'success'
        run.notes = "\n".join(run_notes[:100])
        run.save(
            update_fields=[
                'finished_at', 'total_created', 'total_skipped', 'total_warnings',
                'total_errors', 'status', 'notes',
            ]
        )

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. Created: {total_created} | Skipped/filtered: {total_skipped + total_filtered} | "
            f"Warnings: {total_warnings} | Errors: {total_errors}"
        ))

    def _parse_feed_with_fallback(self, feed_url):
        warning = None
        try:
            feed = feedparser.parse(feed_url, request_headers=REQUEST_HEADERS)
        except Exception as exc:
            feed = None
            warning = f"initial parse failed: {exc}"

        if feed and getattr(feed, 'entries', None):
            if getattr(feed, 'bozo', False):
                warning = f"parser warning: {getattr(feed, 'bozo_exception', 'unknown bozo warning')}"
            return feed, warning

        fallback_reason = warning or "empty feed entries"
        try:
            req = Request(feed_url, headers=REQUEST_HEADERS)
            with urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
                raw_data = resp.read()
            fallback_feed = feedparser.parse(raw_data)
        except Exception as exc:
            return None, f"{fallback_reason}; fallback fetch failed: {exc}"

        if not getattr(fallback_feed, 'entries', None):
            return None, f"{fallback_reason}; fallback returned no entries"

        warning = f"{fallback_reason}; recovered via raw-fetch fallback"
        return fallback_feed, warning

    def _parse_entry_datetime(self, entry):
        for attr in ('published_parsed', 'updated_parsed'):
            parsed = getattr(entry, attr, None)
            if not parsed:
                continue
            try:
                dt = datetime(*parsed[:6], tzinfo=dt_timezone.utc)
                return timezone.localtime(dt)
            except Exception:
                continue
        return timezone.now()
