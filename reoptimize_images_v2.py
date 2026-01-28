import shutil
import os
from PIL import Image

# Source paths (Artifacts)
lies_src = r"C:\Users\pmish\.gemini\antigravity\brain\09a13142-a31f-421b-975f-a0c01cef7945\career_lies_concept_1769522121021.png"
reality_src = r"C:\Users\pmish\.gemini\antigravity\brain\09a13142-a31f-421b-975f-a0c01cef7945\career_reality_concept_1769522358560.png"

# Dest paths (Project)
dest_dir = r"c:\Users\pmish\Downloads\career_reality\static\images"
lies_dest = os.path.join(dest_dir, "hero_lies.png")
reality_dest = os.path.join(dest_dir, "hero_reality.png")

# Copy files
if os.path.exists(lies_src):
    shutil.copy2(lies_src, lies_dest)
if os.path.exists(reality_src):
    shutil.copy2(reality_src, reality_dest)

# Optimization config
files_config = [
    {
        'path': lies_dest,
        'quality': 70, # Clean vector style needs reasonable quality
        'widths': [400, 600, 800, 1024]
    },
    {
        'path': reality_dest,
        'quality': 50, # Glitch/dark style can handle heavier compression
        'widths': [400, 600, 800, 1024]
    }
]

for item in files_config:
    file_path = item['path']
    quality = item['quality']
    widths = item['widths']
    
    if os.path.exists(file_path):
        try:
            img = Image.open(file_path)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            print(f"Processing {file_path}: Intrinsic Size {img.size}")

            base_name = os.path.splitext(file_path)[0]
            
            for width in widths:
                # Calculate height
                w_percent = (width / float(img.size[0]))
                h_size = int((float(img.size[1]) * float(w_percent)))
                
                img_resized = img.resize((width, h_size), Image.Resampling.LANCZOS)
                
                if width == 1024:
                    new_path = f"{base_name}.webp"
                else:
                    new_path = f"{base_name}_{width}w.webp"
                
                img_resized.save(new_path, "WEBP", optimize=True, quality=quality)
                print(f"Generated {new_path}: {img_resized.size}, {os.path.getsize(new_path)} bytes")
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
