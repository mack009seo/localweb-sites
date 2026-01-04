import os
import csv
import re

class DirectoryGenerator:
    """Generates a central static directory hub for all landing pages."""

    def __init__(self, csv_file, sites_dir="sites", template_path="templates/directory/premium_hub.html"):
        self.csv_file = csv_file
        self.sites_dir = sites_dir
        self.template_path = template_path

    def _slugify(self, text: str) -> str:
        text = text.lower()
        # Remove accents
        text = re.sub(r'[áàäâ]', 'a', text)
        text = re.sub(r'[éèëê]', 'e', text)
        text = re.sub(r'[íìïî]', 'i', text)
        text = re.sub(r'[óòöô]', 'o', text)
        text = re.sub(r'[úùüû]', 'u', text)
        text = re.sub(r'[ñ]', 'n', text)
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_-]+', '-', text)
        return text.strip('-')

    def generate(self, output_path="index.html"):
        from datetime import datetime
        import json

        if not os.path.exists(self.csv_file):
            print(f"Error: CSV file not found at {self.csv_file}")
            return

        if not os.path.exists(self.template_path):
            print(f"Error: Template not found at {self.template_path}")
            return
            
        with open(self.template_path, 'r', encoding='utf-8') as f:
            template = f.read()
            
        # Copy Hub Assets (e.g., hero images)
        hub_assets_src = "assets/home"
        hub_assets_dst = os.path.join(self.sites_dir, "assets", "home")
        
        if os.path.exists(hub_assets_src):
            import shutil
            os.makedirs(hub_assets_dst, exist_ok=True)
            # Copy file by file to avoid errors if dir exists
            for item in os.listdir(hub_assets_src):
                s = os.path.join(hub_assets_src, item)
                d = os.path.join(hub_assets_dst, item)
                if os.path.isfile(s):
                    shutil.copy2(s, d)
            print(f"✓ Copied hub assets from {hub_assets_src} to {hub_assets_dst}")

        businesses = []
        categories_list = [
            {"name": "Electricista", "slug": "electricista", "icon": "⚡"},
            {"name": "Pintor", "slug": "pintor", "icon": "🎨"},
            {"name": "Fontanero", "slug": "fontanero", "icon": "🚰"},
            {"name": "Jardinero", "slug": "jardinero", "icon": "🌳"},
            {"name": "Carpintero", "slug": "carpintero", "icon": "🪚"},
            {"name": "Carpintería de Aluminio", "slug": "carpinteria-aluminio", "icon": "🪟"},
            {"name": "Limpieza", "slug": "limpieza", "icon": "🧹"},
            {"name": "Placas Solares", "slug": "placas-solares", "icon": "☀️"},
            {"name": "Cerrajero", "slug": "cerrajero", "icon": "🔑"},
            {"name": "Reformas", "slug": "reformas", "icon": "🏠"},
            {"name": "Aire Acondicionado", "slug": "aire-acondicionado", "icon": "❄️"}
        ]

        cities_list = ["Barcelona", "Madrid", "Valencia", "Sevilla", "Zaragoza", "Málaga"]

        with open(self.csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("nombre", "")
                slug = self._slugify(name)
                site_path = os.path.join(self.sites_dir, slug)
                
                if os.path.exists(site_path):
                    category = row.get("categoria", "").lower()
                    city = row.get("ubicacion", "Barcelona")
                    
                    businesses.append({
                        "name": name,
                        "slug": slug,
                        "category": category.capitalize(),
                        "city": city
                    })

        # Generate Category Links HTML
        cat_links_html = ""
        for cat in categories_list:
            cat_links_html += f"""
            <a href="/categoria/{cat['slug']}" class="category-card">
                <div class="category-icon">{cat['icon']}</div>
                <h3>{cat['name']}</h3>
            </a>
            """

        # Generate City Links HTML
        city_links_html = ""
        for city in cities_list:
            city_links_html += f'<a href="/{city.lower()}/fontanero" class="city-link">{city}</a>'

        # Perform replacements
        replacements = {
            "[[BUSINESS_DATA_JSON]]": json.dumps(businesses),
            "[[CATEGORY_LINKS]]": cat_links_html,
            "[[CITY_LINKS]]": city_links_html,
            "[[YEAR]]": str(datetime.now().year)
        }

        for key, value in replacements.items():
            template = template.replace(key, value)

        # Save the final directory index
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template)

        print(f"✓ Directorio central PREMIUM generado en {output_path} ({len(businesses)} negocios)")

if __name__ == "__main__":
    gen = DirectoryGenerator("data/cleaned_prospects_BARCELONA.csv")
    gen.generate()
