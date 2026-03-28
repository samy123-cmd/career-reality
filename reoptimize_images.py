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

# Optimization Config
files_to_process = [lies_dest, reality_dest]
TARGET_WIDTHS = [400, 600, 800, 1024] # Added intermediate sizes
QUALITY = 75 # Reduced from 85

for file_path in files_to_process:
    if os.path.exists(file_path):
        try:
            img = Image.open(file_path)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            base_name = os.path.splitext(file_path)[0]
            
            for width in TARGET_WIDTHS:
                # Calculate height
                w_percent = (width / float(img.size[0]))
                h_size = int((float(img.size[1]) * float(w_percent)))
                
                img_resized = img.resize((width, h_size), Image.Resampling.LANCZOS)
                
                # Naming scheme matches srcset expectations
                # Base (1024) is just name.webp, others are name_Widthw.webp
                if width == 1024:
                    new_path = f"{base_name}.webp"
                else:
                    new_path = f"{base_name}_{width}w.webp"
                
                img_resized.save(new_path, "WEBP", optimize=True, quality=QUALITY)
                print(f"Generated {new_path}: {img_resized.size}, {os.path.getsize(new_path)} bytes")
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
