from PIL import Image
import os
import glob

image_folder = "images"
quality = 80
max_width = 1200

# Get all image files
image_files = glob.glob(os.path.join(image_folder, "*.jpg")) + \
              glob.glob(os.path.join(image_folder, "*.jpeg")) + \
              glob.glob(os.path.join(image_folder, "*.png"))

print(f"Found {len(image_files)} images to compress\n")

for image_path in image_files:
    try:
        img = Image.open(image_path)
        original_size = os.path.getsize(image_path) / 1024  # KB
        
        # Resize if too large
        if img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert RGBA to RGB for JPG files
        if image_path.lower().endswith(('.jpg', '.jpeg')):
            if img.mode == 'RGBA':
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
                img = rgb_img
            img.save(image_path, "JPEG", quality=quality, optimize=True)
        else:
            # PNG optimization
            img.save(image_path, "PNG", optimize=True)
        
        new_size = os.path.getsize(image_path) / 1024  # KB
        reduction = ((original_size - new_size) / original_size) * 100
        
        print(f"✓ {os.path.basename(image_path)}")
        print(f"  {original_size:.2f} KB → {new_size:.2f} KB ({reduction:.1f}% reduction)")
        
    except Exception as e:
        print(f"✗ Error processing {os.path.basename(image_path)}: {e}")

print("\nImage compression complete!")
