
import os
import sys
import time
from src.messaging.outreach_manager import OutreachManager
from src.messaging.sales_bot import SalesBot

def run_serra_workflow():
    print("🚑 Iniciando Workflow: Ambulancies Serra")
    print("-" * 50)
    
    om = OutreachManager()
    bot = SalesBot()
    
    prospect = {
        'nombre': 'Ambulancies Serra',
        'telefono': '+34696043437',
        'categoria': 'Servicio de Ambulancias',
        'ubicacion': 'Girona',
        'slug': 'ambulancies-serra'
    }
    
    # 1. Generar mensaje inicial
    link = om.get_whatsapp_link(
        prospect['telefono'], 
        prospect['nombre'], 
        prospect['categoria'], 
        prospect['slug'],
        prospect['ubicacion']
    )
    
    import urllib.parse
    parsed = urllib.parse.urlparse(link)
    query_params = urllib.parse.parse_qs(parsed.query)
    outreach_text = query_params['text'][0]
    
    print(f"📩 Enviando Outreach Inicial a {prospect['nombre']}...")
    success = om.send_whatsapp_message(prospect['telefono'], outreach_text)
    
    if success:
        print("✅ Mensaje de outreach enviado con éxito.")
    else:
        print(f"❌ Error al enviar mensaje: {result}")
        return

    # 2. Simular respuesta y seguimiento (opcional para el manual)
    print("\n--- PASO SIGUIENTE ---")
    print("Una vez el cliente responda, el SalesBot se encargará.")
    print("Ejemplo de respuesta de la IA ante duda de precio:")
    print(f"Bot: {bot.generate_response('¿Me pasas precios?')}")

if __name__ == "__main__":
    run_serra_workflow()
