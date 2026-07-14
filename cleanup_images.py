import os
import re
import shutil
from pathlib import Path

# Paths
BASE_DIR = Path('d:/site/site-frappe/webapp')
PUBLIC_IMAGES = BASE_DIR / 'webapp' / 'public' / 'images'
ARCHIVE_DIR = BASE_DIR / 'assets-library' / 'archive'

# File extensions to search in
SEARCH_EXTENSIONS = {'.html', '.js', '.py', '.scss', '.css'}

def get_all_images(image_dir):
    images = []
    for root, _, files in os.walk(image_dir):
        for f in files:
            images.append(Path(root) / f)
    return images

def get_all_search_files(base_dir):
    search_files = []
    for root, _, files in os.walk(base_dir):
        # Exclude node_modules, .git, etc.
        if '.git' in root or 'node_modules' in root or 'assets-library' in root:
            continue
        for f in files:
            if Path(f).suffix in SEARCH_EXTENSIONS:
                search_files.append(Path(root) / f)
    return search_files

def main():
    print("Finding all images...")
    images = get_all_images(PUBLIC_IMAGES)
    print(f"Total images found: {len(images)}")
    
    print("Finding all files to search in...")
    search_files = get_all_search_files(BASE_DIR)
    print(f"Total searchable files: {len(search_files)}")
    
    # Read contents of all searchable files
    file_contents = []
    for sf in search_files:
        try:
            with open(sf, 'r', encoding='utf-8') as f:
                file_contents.append(f.read())
        except Exception as e:
            pass
            
    full_text = " ".join(file_contents)
    
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    
    unused_count = 0
    for img_path in images:
        # Check if the filename or relative path is in the full text
        img_name = img_path.name
        
        # We need a robust way: just check if the filename exists in the text.
        # This is conservative (might keep unused images if filename matches another word),
        # but prevents deleting used ones.
        if img_name not in full_text:
            # It's unused!
            # Move to archive
            rel_path = img_path.relative_to(PUBLIC_IMAGES)
            dest = ARCHIVE_DIR / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(img_path), str(dest))
            print("Moved a file")
            unused_count += 1
            
    print(f"Total unused images moved: {unused_count}")

if __name__ == '__main__':
    main()
