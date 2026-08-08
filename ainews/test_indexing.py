"""Tests for IT workplace-impact AI news filters and indexing."""

from django.test import TestCase
from django.utils import timezone

from ainews.impact_filters import passes_ingest_filter
from ainews.indexing import item_is_indexable
from ainews.models import AINewsItem


class AIImpactFilterTests(TestCase):
    def test_rejects_benchmark_noise(self):
        self.assertFalse(
            passes_ingest_filter(
                "New SOTA benchmark on MMLU leaderboard",
                "Researchers release arxiv preprint with parameter count details.",
                "MarkTechPost",
            )
        )

    def test_accepts_enterprise_impact(self):
        self.assertTrue(
            passes_ingest_filter(
                "Microsoft expands Copilot to enterprise IT teams",
                "Workflow automation and security compliance updates for developers.",
                "VentureBeat AI",
            )
        )


class AIIndexabilityTests(TestCase):
    def test_published_without_career_angle_not_indexable(self):
        item = AINewsItem.objects.create(
            title="Enterprise layoffs in tech",
            slug="enterprise-layoffs-tech",
            summary="Companies cut workforce amid automation push.",
            source_name="VentureBeat AI",
            source_url="https://example.com/1",
            status="published",
            published_at=timezone.now(),
            external_id="test-1",
        )
        self.assertFalse(item_is_indexable(item))

    def test_published_with_career_angle_indexable(self):
        summary = " ".join(
            [
                "IT services firms slow fresher hiring as clients delay projects."
                " Indian engineering orgs rewrite staffing plans around AI-assisted delivery,"
                " evaluation discipline, and tighter utilization targets."
            ]
            * 40
        )
        item = AINewsItem.objects.create(
            title="Enterprise hiring freeze for junior roles",
            slug="enterprise-hiring-freeze",
            summary=summary,
            career_angle=(
                "If you are a 0–2 YOE engineer in India, expect longer bench time and "
                "stronger competition for GCC roles — update skills toward production SQL and cloud. "
                "Build one evidence artifact with metrics before you switch, and treat vague AI "
                "titles without scope as conventional engineering roles with marketing labels."
            ),
            source_name="VentureBeat AI",
            source_url="https://example.com/2",
            status="published",
            published_at=timezone.now(),
            reviewed_at=timezone.now(),
            external_id="test-2",
        )
        self.assertTrue(item_is_indexable(item))

    def test_thin_body_not_indexable(self):
        item = AINewsItem.objects.create(
            title="Enterprise hiring freeze for junior roles",
            slug="enterprise-hiring-freeze-thin",
            summary="IT services firms slow fresher hiring as clients delay projects.",
            career_angle=(
                "If you are a 0–2 YOE engineer in India, expect longer bench time and "
                "stronger competition for GCC roles — update skills toward production SQL and cloud."
            ),
            source_name="VentureBeat AI",
            source_url="https://example.com/3",
            status="published",
            published_at=timezone.now(),
            reviewed_at=timezone.now(),
            external_id="test-3",
        )
        self.assertFalse(item_is_indexable(item))
