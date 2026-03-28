from PIL import Image
import os

files = [
    'static/images/tourists_optimists.webp',
    'static/images/professional_frustrated.webp'
]

TARGET_WIDTH = 600

for file_path in files:
    if os.path.exists(file_path):
        try:
            img = Image.open(file_path)
            
            # Calculate height to maintain aspect ratio
            w_percent = (TARGET_WIDTH / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            
            img_resized = img.resize((TARGET_WIDTH, h_size), Image.Resampling.LANCZOS)
            
            # Construct new filename
            name, ext = os.path.splitext(file_path)
            new_path = f"{name}_{TARGET_WIDTH}w{ext}"
            
            img_resized.save(new_path, optimize=True, quality=85)
            print(f"Created {new_path}: {img_resized.size}, {os.path.getsize(new_path)} bytes")
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    else:
        print(f"File not found: {file_path}")
