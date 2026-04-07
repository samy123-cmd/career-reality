import logging
import re
from datetime import datetime, timezone as dt_timezone
from urllib.request import Request, urlopen

import feedparser
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from ainews.models import AINewsFetchRun, AINewsItem, AITag

logger = logging.getLogger(__name__)
REQUEST_HEADERS = {'User-Agent': 'CareerRealityAIBot/1.0 (+https://careerreality.in)'}
REQUEST_TIMEOUT_SECONDS = 15

# RSS feeds to aggregate, grouped by source name
RSS_FEEDS = [
    {
        'name': 'OpenAI',
        'url': 'https://openai.com/news/rss.xml',
        'default_tags': ['Model Release', 'Industry News'],
    },
    {
        'name': 'Google DeepMind',
        'url': 'https://deepmind.google/blog/rss.xml',
        'default_tags': ['Research Paper', 'Model Release'],
    },
    {
        'name': 'VentureBeat AI',
        'url': 'https://venturebeat.com/category/ai/feed',
        'default_tags': ['Industry News'],
    },
    {
        'name': 'HuggingFace Trending',
        'url': 'https://zernel.github.io/huggingface-trending-feed/feed.xml',
        'default_tags': ['Open Source', 'Model Release'],
        'bundle': True,
    },
    {
        'name': 'HuggingFace Papers',
        'url': 'https://papers.takara.ai/api/feed',
        'default_tags': ['Research Paper'],
        'bundle': True,
    },
    {
        'name': 'MIT AI News',
        'url': 'https://news.mit.edu/rss/topic/artificial-intelligence2',
        'default_tags': ['Research Paper', 'Industry News'],
    },
    {
        'name': 'MarkTechPost',
        'url': 'https://www.marktechpost.com/feed/',
        'default_tags': ['Industry News'],
    },
]

# Trusted sources that can be auto-published when --auto-publish is used
TRUSTED_SOURCES = {'OpenAI', 'Google DeepMind', 'HuggingFace Trending'}


class Command(BaseCommand):
    help = 'Fetch AI news from RSS feeds and store as AINewsItem entries.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--auto-publish',
            action='store_true',
            help='Auto-publish items from trusted sources instead of saving as draft.',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='Maximum number of items to process per feed (default: 10).',
        )

    def handle(self, *args, **options):
        auto_publish = options['auto_publish']
        limit = options['limit']
        run = AINewsFetchRun.objects.create(source_count=len(RSS_FEEDS))
        run_notes = []

        total_created = 0
        total_skipped = 0
        total_errors = 0
        total_warnings = 0

        # Ensure default tags exist
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

            entries = feed.entries[:limit]
            self.stdout.write(f"  Found {len(feed.entries)} entries, processing {len(entries)}")

            bundle = feed_config.get('bundle', False)
            if bundle:
                bundled_items = []
                today_str = timezone.now().strftime('%Y-%m-%d')
                bundle_external_id = f"{source_name}-bundle-{today_str}"
                
                if AINewsItem.objects.filter(external_id=bundle_external_id).exists():
                    self.stdout.write(f"  Bundle for {source_name} already exists today. Skipping {len(entries)} items.")
                    total_skipped += len(entries)
                    continue
                
                for entry in entries:
                    title = getattr(entry, 'title', 'Untitled')[:300]
                    link = getattr(entry, 'link', '')
                    if link:
                        bundled_items.append(f"<li><a href='{link}' target='_blank' rel='noopener noreferrer'>{title}</a></li>")
                    else:
                        bundled_items.append(f"<li>{title}</li>")
                
                if bundled_items:
                    summary = "<p>Here are the latest model releases and trending repositories:</p><ul>" + "".join(bundled_items) + "</ul>"
                    title = f"{source_name} Daily Model Roundup"
                    
                    is_trusted = source_name in TRUSTED_SOURCES
                    status = 'published' if (auto_publish and is_trusted) else 'draft'
                    slug = slugify(f"{title} {today_str}")[:300]
                    counter = 1
                    base_slug = slug
                    while AINewsItem.objects.filter(slug=slug).exists():
                        slug = f"{base_slug[:290]}-{counter}"
                        counter += 1
                    
                    try:
                        item = AINewsItem.objects.create(
                            title=title,
                            slug=slug,
                            summary=summary,
                            source_name=source_name,
                            source_url=feed_url,
                            status=status,
                            fact_check_status='pending',
                            event_date=timezone.now(),
                            reviewed_at=timezone.now() if status == 'published' else None,
                            published_at=timezone.now(),
                            external_id=bundle_external_id,
                        )
                        for tag_name in default_tag_names:
                            if tag_name in tag_cache:
                                item.tags.add(tag_cache[tag_name])
                        total_created += 1
                        self.stdout.write(f"  + Bundled {len(bundled_items)} items into one roundup [{status}]")
                    except Exception as exc:
                        self.stderr.write(self.style.ERROR(f"  Error saving bundle: {exc}"))
                        total_errors += 1
                continue

            for entry in entries:
                external_id = getattr(entry, 'id', None) or getattr(entry, 'link', None)
                if not external_id:
                    total_skipped += 1
                    continue

                # Deduplication check
                if AINewsItem.objects.filter(external_id=external_id).exists():
                    total_skipped += 1
                    continue

                title = getattr(entry, 'title', 'Untitled')[:300]
                link = getattr(entry, 'link', '')

                # Extract summary from various feed formats
                summary = ''
                if hasattr(entry, 'summary'):
                    summary = entry.summary
                elif hasattr(entry, 'description'):
                    summary = entry.description

                # Strip HTML tags for a clean summary
                summary = re.sub(r'<[^>]+>', '', summary or '').strip()
                summary = re.sub(r'[\r\n\t]+', ' ', summary).strip()
                if len(summary) > 1000:
                    summary = summary[:997] + '...'

                # Parse published date
                published_dt = self._parse_entry_datetime(entry)

                # Determine status
                is_trusted = source_name in TRUSTED_SOURCES
                status = 'published' if (auto_publish and is_trusted) else 'draft'

                slug = slugify(title)[:300]
                # Handle slug collisions
                base_slug = slug
                counter = 1
                while AINewsItem.objects.filter(slug=slug).exists():
                    slug = f"{base_slug[:290]}-{counter}"
                    counter += 1

                try:
                    item = AINewsItem.objects.create(
                        title=title,
                        slug=slug,
                        summary=summary or f"New development from {source_name}.",
                        source_name=source_name,
                        source_url=link or feed_url,
                        status=status,
                        fact_check_status='pending',
                        event_date=published_dt,
                        reviewed_at=timezone.now() if status == 'published' else None,
                        published_at=published_dt,
                        external_id=external_id,
                    )

                    # Attach default tags
                    for tag_name in default_tag_names:
                        if tag_name in tag_cache:
                            item.tags.add(tag_cache[tag_name])

                    total_created += 1
                    self.stdout.write(f"  + {title[:80]}... [{status}]")

                except Exception as exc:
                    self.stderr.write(self.style.ERROR(f"  Error saving '{title[:60]}': {exc}"))
                    total_errors += 1
                    run_notes.append(f"{source_name}: save error for '{title[:40]}' - {exc}")

        run.finished_at = timezone.now()
        run.total_created = total_created
        run.total_skipped = total_skipped
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
                'total_errors', 'status', 'notes'
            ]
        )

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. Created: {total_created} | Skipped (dupes): {total_skipped} | Warnings: {total_warnings} | Errors: {total_errors}"
        ))

    def _parse_feed_with_fallback(self, feed_url):
        """Parse feed by URL first, then retry using raw HTTP bytes for brittle feeds."""
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
            if getattr(fallback_feed, 'bozo', False):
                return None, (
                    f"{fallback_reason}; fallback parser warning: "
                    f"{getattr(fallback_feed, 'bozo_exception', 'unknown bozo warning')}"
                )
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
