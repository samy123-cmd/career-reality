"""WCAG contrast enforcement for the feature design tokens.

Colour regressions are invisible to every other kind of test: the page still
returns 200 and the markup is unchanged, only the text cannot be read. These
tests parse the real stylesheet, resolve each token per theme, and compute the
contrast ratio, so a palette change that drops below the standard fails here.

Thresholds are WCAG 2.1 AA: 4.5:1 for body text, 3:1 for large text and
non-text UI such as borders and focus indicators.
"""

import re
from pathlib import Path

from django.conf import settings
from django.test import TestCase

BODY_TEXT_MIN = 4.5
LARGE_TEXT_MIN = 3.0


def _relative_luminance(hex_colour: str) -> float:
    value = hex_colour.lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    channels = []
    for offset in (0, 2, 4):
        channel = int(value[offset : offset + 2], 16) / 255
        channels.append(channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4)
    red, green, blue = channels
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(foreground: str, background: str) -> float:
    light = _relative_luminance(foreground)
    dark = _relative_luminance(background)
    if light < dark:
        light, dark = dark, light
    return (light + 0.05) / (dark + 0.05)


# Resolved palettes: what a browser actually computes for each theme once the
# site tokens and the feature overrides have both been applied.
DARK = {
    "page": "#06060b",
    "surface": "#0e0e16",
    "elevated": "#14141f",
    "text_primary": "#fafafa",
    "text_secondary": "#c8c8d0",
    "text_muted": "#9e9ea8",
    "accent": "#38bdf8",
    "positive": "#34d399",
    "warning": "#fbbf24",
    "danger": "#f87171",
}

LIGHT = {
    "page": "#fafafa",
    "surface": "#ffffff",
    "elevated": "#f4f4f5",
    "text_primary": "#09090b",
    "text_secondary": "#52525b",
    "text_muted": "#63636b",
    "accent": "#0369a1",
    "positive": "#166534",
    "warning": "#92400e",
    "danger": "#b91c1c",
}

TEXT_ROLES = ("text_primary", "text_secondary", "text_muted",
              "accent", "positive", "warning", "danger")
BACKGROUNDS = ("page", "surface", "elevated")


class ContrastRatioTests(TestCase):
    """Every text colour must be readable on every surface it can appear on."""

    def test_dark_mode_text_meets_wcag_aa(self):
        for role in TEXT_ROLES:
            for surface in BACKGROUNDS:
                with self.subTest(theme="dark", role=role, surface=surface):
                    ratio = contrast_ratio(DARK[role], DARK[surface])
                    self.assertGreaterEqual(
                        ratio, BODY_TEXT_MIN,
                        msg=f"dark {role} on {surface} is {ratio:.2f}:1, below {BODY_TEXT_MIN}:1",
                    )

    def test_light_mode_text_meets_wcag_aa(self):
        for role in TEXT_ROLES:
            for surface in BACKGROUNDS:
                with self.subTest(theme="light", role=role, surface=surface):
                    ratio = contrast_ratio(LIGHT[role], LIGHT[surface])
                    self.assertGreaterEqual(
                        ratio, BODY_TEXT_MIN,
                        msg=f"light {role} on {surface} is {ratio:.2f}:1, below {BODY_TEXT_MIN}:1",
                    )

    def test_primary_button_is_legible_in_both_themes(self):
        """The CTA inverts the palette, so it needs checking separately."""
        for name, palette in (("dark", DARK), ("light", LIGHT)):
            with self.subTest(theme=name):
                ratio = contrast_ratio(palette["page"], palette["text_primary"])
                self.assertGreaterEqual(ratio, BODY_TEXT_MIN, msg=f"{name} CTA is {ratio:.2f}:1")

    def test_regression_light_mode_is_not_dark_on_dark(self):
        """The original defect: text and background both resolved near-black."""
        ratio = contrast_ratio(LIGHT["text_primary"], LIGHT["page"])
        self.assertGreater(ratio, 10, msg=f"light body text is {ratio:.2f}:1")


class TokenWiringTests(TestCase):
    """The stylesheet must read tokens the theme files actually define."""

    def setUp(self):
        self.css = (Path(settings.BASE_DIR) / "static" / "css" / "feature-product.css").read_text()
        self.theme_css = "".join(
            (Path(settings.BASE_DIR) / "static" / "css" / name).read_text()
            for name in ("theme-premium-dark.css", "theme-light.css")
        )

    def test_every_consumed_site_token_is_defined(self):
        consumed = set(re.findall(r"var\((--cr-[a-z0-9-]+)", self.css))
        defined = set(re.findall(r"(--cr-[a-z0-9-]+)\s*:", self.theme_css))
        missing = consumed - defined
        self.assertEqual(
            missing, set(),
            msg=f"feature CSS reads tokens no theme defines, so they silently fall back: {missing}",
        )

    def test_light_theme_overrides_the_semantic_palette(self):
        self.assertIn('[data-theme="light"] .cr-feature', self.css)
        self.assertIn('[data-theme="light"] .cr-dash', self.css)
        light_block = self.css[self.css.index('[data-theme="light"] .cr-feature'):]
        light_block = light_block[: light_block.index("}")]
        for token in ("--feature-accent", "--feature-positive", "--feature-warning", "--feature-danger"):
            with self.subTest(token=token):
                self.assertIn(token, light_block, msg=f"{token} has no light-mode value")

    def test_light_palette_under_test_matches_the_stylesheet(self):
        """Keeps the ratios above honest if someone edits the CSS.

        Without this the contrast tests would keep passing against a palette
        the site no longer ships.
        """
        block = self.css[self.css.index('[data-theme="light"] .cr-feature'):]
        block = block[: block.index("}")]
        declared = dict(re.findall(r"(--feature-[a-z-]+):\s*(#[0-9a-fA-F]{6})", block))
        for token, role in (
            ("--feature-text-muted", "text_muted"),
            ("--feature-accent", "accent"),
            ("--feature-positive", "positive"),
            ("--feature-warning", "warning"),
            ("--feature-danger", "danger"),
        ):
            with self.subTest(token=token):
                self.assertEqual(
                    declared.get(token, "").lower(), LIGHT[role].lower(),
                    msg=f"{token} in CSS does not match the value these tests check",
                )

    def test_borders_follow_the_theme(self):
        """A white border at 8% opacity is invisible on a white surface."""
        token_block = self.css[: self.css.index('[data-theme="light"]')]
        border_line = [ln for ln in token_block.splitlines() if "--feature-border:" in ln]
        self.assertTrue(border_line)
        self.assertIn("--cr-border", border_line[0], msg="border must inherit the theme token")
