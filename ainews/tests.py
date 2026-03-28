from types import SimpleNamespace
from unittest.mock import patch

from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import AINewsFetchRun, AINewsItem, AITag


@override_settings(
    CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}
    }
)
class AINewsModelAndViewTests(TestCase):
    def setUp(self):
        cache.clear()
        self.tag_release = AITag.objects.create(name='Model Release', slug='model-release')
        self.tag_research = AITag.objects.create(name='Research Paper', slug='research-paper')

    def _create_item(self, title, slug, status='published', significance='medium', **kwargs):
        item = AINewsItem.objects.create(
            title=title,
            slug=slug,
            summary=kwargs.get('summary', f'Summary for {title}'),
            source_name=kwargs.get('source_name', 'TestSource'),
            source_url=kwargs.get('source_url', 'https://example.com/article'),
            status=status,
            significance=significance,
            event_date=kwargs.get('event_date'),
            reviewed_at=kwargs.get('reviewed_at'),
            published_at=kwargs.get('published_at', timezone.now()),
            external_id=kwargs.get('external_id', f'ext-{slug}'),
        )
        if 'tags' in kwargs:
            for tag in kwargs['tags']:
                item.tags.add(tag)
        return item

    # --- Model Tests ---

    def test_ai_news_item_get_absolute_url(self):
        item = self._create_item('Test Item', 'test-item')

        self.assertEqual(item.get_absolute_url(), '/ai/test-item/')

    def test_ai_tag_get_absolute_url(self):
        self.assertEqual(self.tag_release.get_absolute_url(), '/ai/tag/model-release/')

    def test_ai_news_item_str(self):
        item = self._create_item('My Title', 'my-title')

        self.assertEqual(str(item), 'My Title')

    # --- Hub View Tests ---

    def test_ai_news_hub_shows_only_published(self):
        self._create_item('Published', 'published', status='published')
        self._create_item('Draft', 'draft', status='draft')

        response = self.client.get(reverse('ai_news_hub'))

        self.assertEqual(response.status_code, 200)
        items = list(response.context['page_obj'].object_list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].slug, 'published')
        self.assertIn('ai_evolution_timeline', response.context)
        self.assertTrue(len(response.context['ai_evolution_timeline']) >= 5)

    def test_ai_news_hub_pagination(self):
        for i in range(18):
            self._create_item(f'Item {i}', f'item-{i}')

        response = self.client.get(reverse('ai_news_hub'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj'].object_list), 15)
        self.assertTrue(response.context['page_obj'].has_next())

    def test_ai_news_hub_tag_filter(self):
        item_a = self._create_item('Release A', 'release-a', tags=[self.tag_release])
        item_b = self._create_item('Paper B', 'paper-b', tags=[self.tag_research])

        response = self.client.get(reverse('ai_news_hub') + '?tag=model-release')

        self.assertEqual(response.status_code, 200)
        items = list(response.context['page_obj'].object_list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].slug, 'release-a')

    # --- Detail View Tests ---

    def test_ai_news_detail_returns_200_for_published(self):
        self._create_item('Detail Test', 'detail-test')

        response = self.client.get(reverse('ai_news_detail', kwargs={'slug': 'detail-test'}))

        self.assertEqual(response.status_code, 200)
        self.assertIn('timeline_position', response.context)

    def test_ai_news_detail_returns_404_for_draft(self):
        self._create_item('Draft Detail', 'draft-detail', status='draft')

        response = self.client.get(reverse('ai_news_detail', kwargs={'slug': 'draft-detail'}))

        self.assertEqual(response.status_code, 404)

    # --- Tag View Tests ---

    def test_ai_news_by_tag_filters_correctly(self):
        self._create_item('Tagged', 'tagged', tags=[self.tag_release])
        self._create_item('Untagged', 'untagged', tags=[self.tag_research])

        response = self.client.get(reverse('ai_news_by_tag', kwargs={'slug': 'model-release'}))

        self.assertEqual(response.status_code, 200)
        items = list(response.context['page_obj'].object_list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].slug, 'tagged')

    def test_ai_news_by_tag_returns_404_for_invalid_tag(self):
        response = self.client.get(reverse('ai_news_by_tag', kwargs={'slug': 'nonexistent'}))

        self.assertEqual(response.status_code, 404)

    # --- Deduplication Tests ---

    def test_external_id_enforces_uniqueness(self):
        self._create_item('First', 'first', external_id='ext-unique-1')

        with self.assertRaises(Exception):
            self._create_item('Second', 'second', external_id='ext-unique-1')

    def test_summary_is_sanitized_on_save(self):
        item = self._create_item(
            'Unsafe', 'unsafe',
            status='draft',
            summary='<script>alert(1)</script><h2>Allowed</h2><p>Body</p>'
        )
        item.summary = '<script>alert(1)</script><h2>Allowed</h2><p>Body</p>'
        item.save()
        item.refresh_from_db()

        self.assertIn('<h2>Allowed</h2>', item.summary)
        self.assertNotIn('<script>', item.summary)

    # --- Sitemap Tests ---

    def test_ai_news_sitemap_includes_published_items(self):
        self._create_item('Published News', 'published-news', status='published')
        self._create_item('Draft News', 'draft-news', status='draft')

        response = self.client.get('/sitemap.xml')

        self.assertEqual(response.status_code, 200)
        body = response.content.decode('utf-8')
        self.assertIn('/ai/published-news/', body)
        self.assertNotIn('/ai/draft-news/', body)

    # --- Management Command Tests ---

    @patch('ainews.management.commands.fetch_ai_news.RSS_FEEDS', [
        {
            'name': 'Test Feed',
            'url': 'https://example.com/feed.xml',
            'default_tags': ['Industry News'],
        }
    ])
    @patch('ainews.management.commands.fetch_ai_news.feedparser.parse')
    def test_fetch_ai_news_deduplication(self, mock_parse):
        mock_parse.return_value = SimpleNamespace(
            bozo=False,
            entries=[
                SimpleNamespace(
                    id='ext-123',
                    link='https://example.com/post-1',
                    title='Test Feed Item',
                    summary='<p>Summary content</p>',
                    published_parsed=None,
                    updated_parsed=None,
                )
            ],
        )

        call_command('fetch_ai_news', limit=5)
        call_command('fetch_ai_news', limit=5)

        self.assertEqual(AINewsItem.objects.filter(external_id='ext-123').count(), 1)
        self.assertEqual(AINewsFetchRun.objects.count(), 2)
