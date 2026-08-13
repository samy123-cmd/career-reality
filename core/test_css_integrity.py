"""Structural integrity checks for hand-maintained stylesheets.

An unbalanced brace silently discards every rule that follows it, so the page
still returns 200 and only looks wrong. These checks turn that into a test
failure instead of a visual regression found in production.
"""

from pathlib import Path

from django.conf import settings
from django.test import TestCase

STYLESHEETS = ("feature-product.css",)


class StylesheetIntegrityTests(TestCase):
    def _css_path(self, name):
        return Path(settings.BASE_DIR) / "static" / "css" / name

    def test_braces_are_balanced(self):
        for name in STYLESHEETS:
            with self.subTest(stylesheet=name):
                css = self._css_path(name).read_text()
                self.assertEqual(
                    css.count("{") - css.count("}"),
                    0,
                    msg=f"{name} has an unbalanced brace; rules after it are dropped",
                )

    def test_no_block_closes_before_it_opens(self):
        for name in STYLESHEETS:
            with self.subTest(stylesheet=name):
                depth = 0
                for line_no, line in enumerate(self._css_path(name).read_text().splitlines(), 1):
                    depth += line.count("{") - line.count("}")
                    self.assertGreaterEqual(
                        depth, 0, msg=f"{name}:{line_no} closes a block that was never opened"
                    )

    def test_no_empty_rule_swallows_the_next_selector(self):
        """Catches `.a, .b {` immediately followed by another selector block."""
        for name in STYLESHEETS:
            with self.subTest(stylesheet=name):
                lines = self._css_path(name).read_text().splitlines()
                for i, line in enumerate(lines[:-1]):
                    stripped = line.strip()
                    if not stripped.endswith("{") or stripped.startswith("@"):
                        continue
                    next_line = lines[i + 1].strip()
                    self.assertFalse(
                        next_line.endswith("{") and not next_line.startswith("@"),
                        msg=f"{name}:{i + 1} opens a rule with no declarations before "
                            f"the next selector ({stripped!r} then {next_line!r})",
                    )

    def test_mobile_breakpoints_present(self):
        css = self._css_path("feature-product.css").read_text()
        for breakpoint in ("max-width: 768px", "max-width: 480px", "max-width: 375px"):
            self.assertIn(breakpoint, css)

    def test_focus_visible_styles_present(self):
        css = self._css_path("feature-product.css").read_text()
        self.assertIn(":focus-visible", css)

    def test_both_roots_receive_the_design_tokens(self):
        """`.cr-dash` once lacked the tokens, so dashboards lost every colour.

        A custom property that resolves to nothing takes the SVG presentation
        attribute with it, which is why the trajectory chart drew unlabelled
        dots on black rather than failing loudly.
        """
        css = self._css_path("feature-product.css").read_text()
        token_block = css.split("{")[1] if "{" in css else ""
        declaration = css[: css.index("{")]
        self.assertIn(".cr-feature", declaration)
        self.assertIn(".cr-dash", declaration)
        for token in ("--feature-accent", "--feature-border", "--feature-text-primary"):
            self.assertIn(token, token_block)

    def test_svg_colours_declare_literal_fallbacks(self):
        """SVG strokes must survive a missing custom property."""
        css = self._css_path("feature-product.css").read_text()
        for selector in (".cr-trajectory__line", ".cr-trajectory__dot", ".cr-radar__data"):
            index = css.find(selector)
            self.assertNotEqual(index, -1, msg=f"{selector} missing")
            block = css[index : css.index("}", index)]
            self.assertIn("#", block, msg=f"{selector} has no literal colour fallback")
