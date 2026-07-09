"""Tests for boilerplate padding removal."""

from django.test import TestCase

from content.boilerplate import strip_safety_pad

PAD = (
    "<p>Indian IT compensation decisions in 2026 should always be stress-tested "
    "with in-hand cash flow, not headline CTC alone. Use structured comparison tools, "
    "talk to three people who made the same choice last year, and write down your "
    "assumptions before committing — ambiguity favors employers and coaching "
    "marketers, not candidates.</p>"
)


class BoilerplateStripTests(TestCase):
    def test_removes_repeated_safety_pad(self):
        html = f"<p>Real content.</p>{PAD}{PAD}{PAD}"
        cleaned = strip_safety_pad(html)
        self.assertEqual(cleaned, "<p>Real content.</p>")
        self.assertNotIn("stress-tested with in-hand cash flow", cleaned)
