import os
import sys
import shutil
import csv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.generator.site_generator import StaticSiteGenerator

def update_all_images():
    csv_file = "data/cleaned_prospects_BARCELONA.csv"
    generator = StaticSiteGenerator(csv_file)
    
    # Load prospect data to map slugs to categories
    slug_to_category = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('nombre'):
                slug = generator._slugify(row['nombre'])
                slug_to_category[slug] = row.get('categoria', '')

    base_sites_dir = "sites"
    updated_count = 0
    
    print(f"Checking images for {len(slug_to_category)} potential sites...")

    if not os.path.exists(base_sites_dir):
        print("Sites directory not found.")
        return

    for site_slug in os.listdir(base_sites_dir):
        if site_slug.startswith('.'):
            continue
        site_path = os.path.join(base_sites_dir, site_slug)
        if not os.path.isdir(site_path):
            continue
            
        category = slug_to_category.get(site_slug, "default")
        
        # Determine the correct image
        hero_filename = generator._get_hero_image(category)
        
        # Source and Dest
        src_image = os.path.join(generator.assets_dir, hero_filename)
        dest_image = os.path.join(site_path, "assets/images/hero.jpg")
        
        # Fallback if specific image doesn't exist
        if not os.path.exists(src_image):
            # print(f"  Missing specific image {src_image}, trying default...")
            src_image = os.path.join(generator.assets_dir, "default.png")
            
        if os.path.exists(src_image):
            # Check if we actually need to update (simple existence check or always overwrite?)
            # Always overwrite to ensure correctness
            shutil.copy(src_image, dest_image)
            updated_count += 1
            # print(f"Updated {site_slug} with {os.path.basename(src_image)}")
        else:
            print(f"Error: Neither specific nor default image found for {site_slug}")

    print(f"✅ Successfully checked and updated images for {updated_count} sites.")

if __name__ == "__main__":
    update_all_images()
