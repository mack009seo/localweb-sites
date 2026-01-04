import os
import shutil
import csv
import re
import sys

# Ensure src path is available
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

def sync_sites():
    clean_csv = "data/prospects_cleaned.csv"
    sites_dir = "sites"
    
    if not os.path.exists(clean_csv):
        print(f"Error: {clean_csv} not found. Run cleaner first.")
        return

    # 1. Get valid slugs
    valid_slugs = set()
    with open(clean_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            valid_slugs.add(slugify(row['nombre']))
            
    # 2. Scan sites dir
    if not os.path.exists(sites_dir):
        print(f"Sites dir {sites_dir} does not exist.")
        return

    existing_sites = [d for d in os.listdir(sites_dir) if os.path.isdir(os.path.join(sites_dir, d)) and d != 'assets']
    
    deleted_count = 0
    for site_slug in existing_sites:
        if site_slug not in valid_slugs:
            print(f"🗑️ Deleting zombie site: {site_slug}")
            shutil.rmtree(os.path.join(sites_dir, site_slug))
            deleted_count += 1
            
    print(f"✅ Sync Complete: Deleted {deleted_count} zombie sites.")
    print(f"ℹ️ Remaining valid sites: {len(valid_slugs)}")

if __name__ == "__main__":
    sync_sites()
