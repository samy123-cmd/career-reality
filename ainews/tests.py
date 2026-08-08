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
        default_career_angle = (
            "Indian IT teams should expect hiring and on-call workflow changes — "
            "update skills toward production deployment and security compliance. "
            "Build an evaluation sheet, document failure modes, and show cost controls "
            "before you claim AI ownership on your résumé. Hiring managers in GCCs and "
            "product companies now ask for evidence artifacts, not certificate lists. "
            "If you ignore measurement, you compete for shrinking ticket-only roles while "
            "AI delivery clauses reduce headcount per project across services accounts."
        )
        default_summary = kwargs.get('summary') or (
            f"<p>Enterprise developer hiring and workplace policy update: {title}. "
            "Affects engineering teams and IT services delivery in India.</p>"
            "<h2>Career Impact</h2>"
            "<p>Indian engineers should treat this as a staffing and skills signal. "
            "Document production constraints, evaluation discipline, and multilingual "
            "failure cases. GCCs and product companies are hiring for implementation "
            "and review strength, not for model-name fluency alone.</p>"
            "<p>Prepare a portfolio artifact with metrics: latency, cost per run, "
            "defect escape, and rollback notes. Interview loops increasingly include "
            "system design for AI-assisted workflows and questions about when to forbid "
            "agents in auth, payments, and migrations.</p>"
            "<p>Services engineers at mid levels face tighter utilization when clients "
            "renegotiate AI delivery clauses. The durable move is ownership of quality "
            "systems, cloud architecture, or client-facing solution design with numbers.</p>"
            "<p>Freshers should pair DSA practice with code-review drills on AI-generated "
            "patches. Seniors should publish playbooks that keep productivity targets honest "
            "when agents accelerate boilerplate and amplify weak review culture.</p>"
            "<p>Compensation premiums attach to scarce proof of ownership. Negotiate with "
            "written scope, hybrid terms, and ninety-day success metrics. Vague AI titles "
            "without eval ownership are conventional engineering jobs with marketing labels.</p>"
            "<p>Use this brief to decide what to learn next, which requisitions are real "
            "headcount, and which headlines are resume bait. Update your materials with "
            "shipped constraints and outcomes rather than another tool certificate.</p>"
            "<p>Market context remains uneven across Bengaluru, Hyderabad, Pune, and Chennai. "
            "Match preparation to employer type: captives buy enterprise platforms first; "
            "startups adopt coding agents faster but hire fewer juniors; services firms "
            "rewrite delivery math in renewals. One evidence artifact travels across all three.</p>"
            "<p>Common mistakes include listing model names without constraints, confusing "
            "editor plugins with applied AI ownership, and resigning before scope is written. "
            "Committees reward dashboards, eval sheets, and architecture one-pagers tied to "
            "business outcomes. Spend four weeks building one vertical slice with logging, "
            "a noisy-input eval set, and a short failure taxonomy you can defend in interviews.</p>"
            "<p>If your current role is ticket-only, treat this update as a forcing function. "
            "Own a quality gate, a cost dashboard, or a client-facing pilot narrative with "
            "numbers. That is the path off the bench when utilization targets tighten again.</p>"
            "<p>Keep a weekly log of decisions: what the assistant drafted, what you changed, "
            "what failed in review, and what shipped. That log becomes interview evidence and "
            "stops you from confusing motion with impact when productivity targets rise.</p>"
        )
        item = AINewsItem.objects.create(
            title=title,
            slug=slug,
            summary=default_summary,
            career_angle=kwargs.get('career_angle', default_career_angle),
            source_name=kwargs.get('source_name', 'VentureBeat AI'),
            source_url=kwargs.get('source_url', 'https://example.com/article'),
            status=status,
            significance=significance,
            event_date=kwargs.get('event_date'),
            reviewed_at=kwargs.get('reviewed_at', kwargs.get('published_at', timezone.now())),
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

    def test_ai_news_detail_redirects_draft_to_hub(self):
        self._create_item('Draft Detail', 'draft-detail', status='draft')

        response = self.client.get(reverse('ai_news_detail', kwargs={'slug': 'draft-detail'}))

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, reverse('ai_news_hub'))

    def test_stale_ai_news_detail_redirects_to_hub(self):
        from datetime import timedelta

        stale_date = timezone.now() - timedelta(days=30)
        self._create_item(
            'Stale News',
            'stale-news',
            reviewed_at=stale_date,
            published_at=stale_date,
        )

        response = self.client.get(reverse('ai_news_detail', kwargs={'slug': 'stale-news'}))

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, reverse('ai_news_hub'))

    # --- Tag View Tests ---

    def test_ai_news_by_tag_filters_correctly(self):
        self._create_item('Tagged', 'tagged', tags=[self.tag_release])
        self._create_item('Untagged', 'untagged', tags=[self.tag_research])

        response = self.client.get(reverse('ai_news_by_tag', kwargs={'slug': 'model-release'}))

        self.assertEqual(response.status_code, 200)
        items = list(response.context['page_obj'].object_list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].slug, 'tagged')
        self.assertIn('noindex', response.context['meta_robots'])
        self.assertIn('noindex', response.get('X-Robots-Tag', ''))

    def test_ai_news_by_tag_empty_redirects_to_hub(self):
        response = self.client.get(reverse('ai_news_by_tag', kwargs={'slug': 'model-release'}))
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, reverse('ai_news_hub'))

    def test_ai_news_detail_meta_description_strips_html(self):
        self._create_item(
            'Meta Clean',
            'meta-clean',
            summary=(
                "<p>Enterprise Gemini rollouts create integration roles for Indian engineers "
                "with API, security, and Indic language testing experience on client teams.</p>"
                + (" Production constraints, evaluation discipline, and multilingual failure "
                   "cases matter more than model-name fluency in Indian GCC hiring loops.") * 20
            ),
        )
        response = self.client.get(reverse('ai_news_detail', kwargs={'slug': 'meta-clean'}))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode('utf-8')
        # Meta/OG description must be plain text — never escaped HTML from summary.
        self.assertNotIn('&lt;p&gt;', html)
        self.assertRegex(html, r'name="description"\s+content="[^"]{20,}"')

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
                    title='Microsoft expands Copilot for enterprise developer teams',
                    summary='<p>Workplace productivity and hiring impact for engineering teams.</p>',
                    published_parsed=None,
                    updated_parsed=None,
                )
            ],
        )

        call_command('fetch_ai_news', limit=5)
        call_command('fetch_ai_news', limit=5)

        self.assertEqual(AINewsItem.objects.filter(external_id='ext-123').count(), 1)
        self.assertEqual(AINewsFetchRun.objects.count(), 2)
