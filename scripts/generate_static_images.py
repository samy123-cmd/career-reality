#!/usr/bin/env python3
"""Generate static image assets referenced by templates (og-default.png, PWA icons)."""

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("Install Pillow: pip install Pillow")

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "static" / "img"


def _draw_brand(draw: ImageDraw.ImageDraw, size: int) -> None:
    draw.rectangle((0, 0, size, size), fill="#0d0d0d")
    draw.rectangle((int(size * 0.12), int(size * 0.18), int(size * 0.16), int(size * 0.82)), fill="#d93025")
    font = ImageFont.load_default()
    draw.text((int(size * 0.22), int(size * 0.38)), "CR", fill="#ffffff", font=font)


def write_og_default(path: Path) -> None:
    img = Image.new("RGB", (1200, 630), "#0d0d0d")
    draw = ImageDraw.Draw(img)
    draw.rectangle((88, 88, 98, 542), fill="#d93025")
    font_lg = ImageFont.load_default()
    font_sm = ImageFont.load_default()
    draw.text((136, 170), "Career Reality India", fill="#ffffff", font=font_lg)
    draw.text((136, 240), "Salary Truths. Career Trade-offs. No Fluff.", fill="#d8d8d8", font=font_sm)
    draw.text((136, 310), "Data-backed insights for Indian tech professionals.", fill="#b0b0b0", font=font_sm)
    draw.rectangle((136, 430, 566, 490), outline="#3a3a3a", fill="#111111")
    draw.text((160, 450), "careerreality.in", fill="#ffffff", font=font_sm)
    img.save(path, format="PNG", optimize=True)


def write_icon(path: Path, size: int) -> None:
    img = Image.new("RGB", (size, size), "#0d0d0d")
    draw = ImageDraw.Draw(img)
    _draw_brand(draw, size)
    img.save(path, format="PNG", optimize=True)


def main() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    write_og_default(IMG / "og-default.png")
    write_icon(IMG / "icon-192.png", 192)
    write_icon(IMG / "icon-512.png", 512)
    print("Wrote og-default.png, icon-192.png, icon-512.png")


if __name__ == "__main__":
    main()
