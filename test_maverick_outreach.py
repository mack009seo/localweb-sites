
import os
import sys
import time
import urllib.parse
from src.messaging.outreach_manager import OutreachManager
from src.crm.tracker import ProspectTracker

def test_maverick_outreach():
    print("🛠️ Test Outreach: Lampistería Maverick")
    print("-" * 50)
    
    om = OutreachManager()
    tracker = ProspectTracker("data/prospects_cleaned.csv")
    
    # Datos del negocio (obtenidos del CSV generado)
    prospect = {
        'nombre': 'Lampistería Maverick',
        'telefono': '+34671429320',
        'categoria': 'lampista',
        'ubicacion': 'Barcelona',
        'slug': 'lampistería-maverick'
    }
    
    # 1. Generar mensaje inicial
    link = om.get_whatsapp_link(
        prospect['telefono'], 
        prospect['nombre'], 
        prospect['categoria'], 
        prospect['slug'],
        prospect['ubicacion']
    )
    
    parsed = urllib.parse.urlparse(link)
    query_params = urllib.parse.parse_qs(parsed.query)
    outreach_text = query_params['text'][0]
    
    print(f"📩 Intentando enviar WhatsApp a {prospect['nombre']} ({prospect['telefono']})...")
    success = om.send_whatsapp_message(prospect['telefono'], outreach_text)
    
    if success:
        print("✅ Mensaje de outreach enviado con éxito via Bridge.")
        # 2. Actualizar estado en el tracker
        tracker.update_status(prospect['nombre'], 'contacted', notes="Test de automatización completado")
        print("✅ Estado actualizado a 'contacted' en data/prospects_cleaned.csv")
    else:
        print("❌ Error al enviar mensaje via Bridge (¿Está el bridge encendido?)")
        print(f"🔗 Link manual: {link}")

if __name__ == "__main__":
    test_maverick_outreach()
