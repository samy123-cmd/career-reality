from PIL import Image
import os

files = [
    'static/images/hero_reality.webp',
    'static/images/hero_reality_800w.webp',
    'static/images/hero_reality_600w.webp',
    'static/images/hero_lies_800w.webp',
]

for f in files:
    if os.path.exists(f):
        img = Image.open(f)
        print(f"{f}: {img.format}, {img.size} (WxH), {os.path.getsize(f)} bytes")
    else:
        print(f"{f}: NOT FOUND")
