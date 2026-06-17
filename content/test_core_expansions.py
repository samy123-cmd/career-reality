"""Tests for core article 900+ word expansions."""

from django.test import TestCase

from content.expansions import (
    CORE_ARTICLE_EXPANSIONS,
    expansion_salary_words,
    expansion_word_count,
    resolve_slugs,
)


class CoreArticleExpansionContentTests(TestCase):
    """Generated editorial bodies must meet AdSense-quality thresholds."""

    def test_six_canonical_articles_defined(self):
        self.assertEqual(len(CORE_ARTICLE_EXPANSIONS), 6)

    def test_all_expansions_meet_word_threshold(self):
        for slug, data in CORE_ARTICLE_EXPANSIONS.items():
            wc = expansion_word_count(data)
            sw = expansion_salary_words(data)
            self.assertGreaterEqual(wc, 900, msg=f"{slug} has {wc} words")
            self.assertGreaterEqual(sw, 150, msg=f"{slug} salary section has {sw} words")

    def test_meta_descriptions_are_substantive(self):
        for slug, data in CORE_ARTICLE_EXPANSIONS.items():
            self.assertGreaterEqual(
                len(data["meta_description"]),
                100,
                msg=f"{slug} meta too short",
            )

    def test_resolve_slugs_includes_aliases(self):
        slugs = resolve_slugs(
            "why-upskilling-stops-working-career-trap",
            CORE_ARTICLE_EXPANSIONS["why-upskilling-stops-working-career-trap"],
        )
        self.assertIn("why-upskilling-stops-working", slugs)


class ExpandCoreArticlesCommandTests(TestCase):
    def test_dry_run_does_not_mutate(self):
        from io import StringIO

        from django.core.management import call_command

        out = StringIO()
        call_command("expand_core_articles", stdout=out)
        self.assertIn("Dry run", out.getvalue())
