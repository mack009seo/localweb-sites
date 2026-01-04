
import os
import csv
import sys
sys.path.append(os.getcwd())
from src.generator.site_generator import StaticSiteGenerator

def update_all_blogs():
    # Use the main CSV
    csv_file = "data/cleaned_prospects_BARCELONA.csv"
    generator = StaticSiteGenerator(csv_file)
    
    base_sites_dir = "sites"
    if not os.path.exists(base_sites_dir):
        print("Sites directory not found.")
        return

    # Load all prospects to match slugs
    prospects = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        prospects = list(reader)

    slug_to_prospect = {}
    for p in prospects:
        slug = generator._slugify(p['nombre'])
        slug_to_prospect[slug] = p

    updated = 0
    for site_slug in os.listdir(base_sites_dir):
        if site_slug.startswith('.'): continue
        site_path = os.path.join(base_sites_dir, site_slug)
        if not os.path.isdir(site_path): continue
        
        if site_slug in slug_to_prospect:
            prospect = slug_to_prospect[site_slug]
            # Full re-generation of the site (it will overwrite index.html and assets)
            generator.generate_site(prospect)
            updated += 1
            if updated % 50 == 0:
                print(f"Refreshed {updated} sites...")

    print(f"Successfully refreshed {updated} sites with blogs and new template.")

if __name__ == "__main__":
    update_all_blogs()
