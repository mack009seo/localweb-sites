import os
import json

def generate_index():
    sites_dir = "sites"
    if not os.path.exists(sites_dir):
        print("No sites directory found.")
        return

    sites = []
    for d in os.listdir(sites_dir):
        site_path = os.path.join(sites_dir, d)
        if os.path.isdir(site_path) and os.path.exists(os.path.join(site_path, "index.html")):
            # Intentar leer el nombre del negocio del index.html si es posible, o usar el slug
            sites.append({
                "slug": d,
                "name": d.replace("-", " ").title()
            })

    # Ordenar alfabéticamente
    sites.sort(key=lambda x: x["name"])

    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Directorio de Servicios Locales</title>
    <style>
        :root {{
            --primary: #3b82f6;
            --bg: #0f172a;
            --text: #f8fafc;
            --card: #1e293b;
        }}
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            color: var(--primary);
            margin-bottom: 40px;
        }}
        .grid {{
            display: grid;
            gap: 15px;
        }}
        .site-card {{
            background: var(--card);
            padding: 20px;
            border-radius: 12px;
            text-decoration: none;
            color: inherit;
            transition: transform 0.2s, border-color 0.2s;
            border: 1px solid transparent;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .site-card:hover {{
            transform: translateY(-2px);
            border-color: var(--primary);
        }}
        .site-card span {{
            color: var(--primary);
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Directorio de Landing Pages</h1>
        <div class="grid">
            {"".join([f'<a href="{s["slug"]}/" class="site-card"><div>{s["name"]}</div><span>Ver Sitio &rarr;</span></a>' for s in sites])}
        </div>
    </div>
</body>
</html>
    """

    with open(os.path.join(sites_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ Directorio generado con {len(sites)} sitios.")

if __name__ == "__main__":
    generate_index()
