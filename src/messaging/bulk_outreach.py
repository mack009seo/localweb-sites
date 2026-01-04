
import sys
import os
import time
import argparse

# Ensure root is in path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.crm.tracker import ProspectTracker
from src.messaging.outreach_manager import OutreachManager

def run_bulk_outreach(csv_path, limit=5, dry_run=False):
    print(f"🚀 Iniciando Outreach Automático (Limit: {limit}, Dry Run: {dry_run})")
    
    tracker = ProspectTracker(csv_path)
    om = OutreachManager()
    
    # Get prospects to contact
    prospects_to_contact = []
    import csv
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('estado') == 'demo_ready':
                prospects_to_contact.append(row)
    
    print(f"📊 Encontrados {len(prospects_to_contact)} prospectos listos para contactar.")
    
    count = 0
    for p in prospects_to_contact:
        if count >= limit:
            break
            
        name = p['nombre']
        phone = p['telefono']
        category = p['categoria']
        demo_url = p.get('url_demo', '')
        localidad = p.get('localidad', p.get('ubicacion', 'su zona'))
        
        # Determine slug from URL
        demo_slug = demo_url.strip('/').split('/')[-1] if demo_url else name.lower().replace(' ', '-')
        
        # Generate message
        # We'll use the one from OutreachManager.get_whatsapp_link template or similar
        msg = (
            f"Hola. He visto el negocio *{name}* en *{localidad}* y las buenas opiniones que tiene "
            f"como *{category}*. Se nota que hacéis un buen trabajo. 👍\n\n"
            f"He visto que ahora mismo no tenéis página web, y hoy en día mucha gente busca en Google "
            f"antes de llamar a un profesional. 📱\n\n"
            f"Por eso he preparado una *página web sencilla y profesional* para vuestro negocio:\n"
            f"🔗 {demo_url}\n\n"
            f"Incluye:\n"
            f"• Diseño adaptado a móviles\n"
            f"• Botón para que te llamen directo ({phone})\n"
            f"• Lista para usar con vuestro propio dominio\n\n"
            f"Es una opción **muy económica** (pago único, sin cuotas mensuales).\n"
            f"Contestadme por aquí si os gustaría ver cómo funciona o probar otra cosa."
        )
        
        print(f"📧 Enviando a {name} ({phone})...")
        
        if dry_run:
            print(f"📝 [DRY RUN] Mensaje:\n{msg}\n")
            success = True
        else:
            success = om.send_whatsapp_message(phone, msg)
            if success:
                tracker.update_status(name, 'contacted', notes="Primer contacto automático enviado.")
                # Give it a small delay to avoid spam detection
                time.sleep(2)
        
        if success:
            count += 1
            
    print(f"✅ Proceso finalizado. Mensajes enviados: {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Envío masivo de mensajes de prospección.")
    parser.add_argument("--csv", type=str, default="data/prospects_cleaned.csv", help="Ruta al CSV de prospectos.")
    parser.add_argument("--limit", type=int, default=5, help="Límite de mensajes a enviar.")
    parser.add_argument("--dry-run", action="store_true", help="Simular el envío sin contactar realmente.")
    
    args = parser.parse_args()
    
    # Check if cleaned file exists, fallback to default if not
    if not os.path.exists(args.csv):
        args.csv = "data/amb_barcelona_sin_web_20260102_223732.csv"
        
    run_bulk_outreach(args.csv, args.limit, args.dry_run)
