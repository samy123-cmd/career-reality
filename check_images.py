try:
    from PIL import Image
    import os

    files = [
        'static/images/tourists_optimists.webp',
        'static/images/professional_frustrated.webp'
    ]

    for f in files:
        if os.path.exists(f):
            img = Image.open(f)
            print(f"{f}: {img.format}, {img.size}, {os.path.getsize(f)} bytes")
        else:
            print(f"{f}: NOT FOUND")
except ImportError:
    print("Pillow not installed")
