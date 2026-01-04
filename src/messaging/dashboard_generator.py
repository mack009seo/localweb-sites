import csv
import os
from datetime import datetime
from src.messaging.outreach_manager import OutreachManager

class DashboardGenerator:
    """Genera un panel HTML interactivo para gestionar el outreach."""

    def __init__(self, csv_file, output_file="outreach_dashboard.html"):
        self.csv_file = csv_file
        self.output_file = output_file
        self.outreach = OutreachManager()

    def _get_status_color(self, status):
        colors = {
            'pending': '#6c757d',
            'demo_ready': '#0d6efd',
            'contacted': '#ffc107',
            'interested': '#198754',
            'on_hold': '#fd7e14',
            'converted': '#20c997',
            'rejected': '#dc3545'
        }
        return colors.get(status, '#6c757d')

    def generate(self):
        if not os.path.exists(self.csv_file):
            print(f"Error: {self.csv_file} no existe.")
            return

        prospects = []
        with open(self.csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('estado') != 'pending' or True: # Por ahora mostramos todos para el dashboard
                    prospects.append(row)

        # Generar HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LocalWeb - Panel de Control de Ventas</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #25D366;
            --secondary: #128C7E;
            --dark: #1a1a1a;
            --light: #f8f9fa;
            --border: #e0e0e0;
        }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #f0f2f5;
            color: var(--dark);
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            background: white;
            padding: 20px 30px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        h1 {{ margin: 0; font-size: 24px; color: var(--secondary); }}
        .stats {{ display: flex; gap: 20px; }}
        .stat-card {{ background: #eee; padding: 5px 15px; border-radius: 20px; font-size: 14px; font-weight: 600; }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }}
        .card {{
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            transition: transform 0.2s;
            display: flex;
            flex-direction: column;
            border-left: 5px solid transparent;
        }}
        .card:hover {{ transform: translateY(-5px); }}
        
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }}
        .biz-name {{ font-weight: 700; font-size: 18px; margin-bottom: 4px; }}
        .biz-cat {{ font-size: 13px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; }}
        
        .badge {{
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
            color: white;
            text-transform: uppercase;
        }}

        .info-row {{
            margin: 10px 0;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .actions {{
            margin-top: auto;
            display: flex;
            gap: 10px;
            padding-top: 15px;
        }}
        
        .btn {{
            flex: 1;
            padding: 10px;
            border-radius: 8px;
            text-decoration: none;
            text-align: center;
            font-weight: 600;
            font-size: 14px;
            transition: opacity 0.2s;
        }}
        .btn-wa {{ background-color: var(--primary); color: white; }}
        .btn-demo {{ background-color: #f0f0f0; color: var(--dark); }}
        .btn:hover {{ opacity: 0.8; }}

        .empty {{ text-align: center; padding: 50px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 LocalWeb Outreach Dashboard</h1>
            <div class="stats">
                <div class="stat-card">Total: {len(prospects)}</div>
                <div class="stat-card" style="color: #0d6efd">Ready: {len([p for p in prospects if p['estado'] == 'demo_ready'])}</div>
            </div>
        </header>

        <div class="grid">
"""

        if not prospects:
            html_content += '<div class="empty">No hay prospectos procesados aún. Ejecuta automate.py primero.</div>'
        else:
            for item in prospects:
                slug = item['url_demo'].split('/')[-2] if item['url_demo'] else ""
                wa_link = self.outreach.get_whatsapp_link(
                    item['telefono'], 
                    item['nombre'], 
                    item['categoria'], 
                    slug,
                    item.get('ubicacion', 'su zona')
                )
                
                status_color = self._get_status_color(item['estado'])
                
                html_content += f"""
            <div class="card" style="border-left-color: {status_color}">
                <div class="card-header">
                    <div>
                        <div class="biz-name">{item['nombre']}</div>
                        <div class="biz-cat">{item['categoria']}</div>
                    </div>
                    <span class="badge" style="background-color: {status_color}">{item['estado']}</span>
                </div>
                
                <div class="info-row">📍 {item['ubicacion']}</div>
                <div class="info-row">📞 {item['telefono']}</div>
                
                <div class="actions">
                    <a href="{item['url_demo']}" target="_blank" class="btn btn-demo">Ver Demo</a>
                    <a href="{wa_link}" target="_blank" class="btn btn-wa">Enviar WhatsApp</a>
                </div>
            </div>
"""

        html_content += """
        </div>
    </div>
</body>
</html>
"""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ Dashboard generado con éxito: {self.output_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=str, default="data/amb_barcelona_sin_web_20260102_223732.csv")
    args = parser.parse_args()
    
    gen = DashboardGenerator(args.csv)
    gen.generate()
