
import os
import sys
from src.messaging.outreach_manager import OutreachManager
from src.messaging.sales_bot import SalesBot

def run_functional_test():
    print("🧪 Iniciando Prueba Funcional: Wajtsup + Evolution API")
    print("-" * 50)
    
    # 1. Configurar managers
    om = OutreachManager()
    bot = SalesBot()
    
    # 2. Definir negocio ficticio
    prospect = {
        'nombre': 'Pinturas Rápidas Mataró',
        'telefono': '+34600000000', # Cambiar por un número real para pruebas reales si se desea
        'categoria': 'Pintor',
        'ubicacion': 'Mataró',
        'slug': 'pintores-mataro'
    }
    
    print(f"🏢 Negocio Ficticio: {prospect['nombre']}")
    print(f"📍 Ubicación: {prospect['ubicacion']}")
    
    # 3. Generar mensaje de Outreach inicial
    # Usamos la lógica de OutreachManager para el primer contacto
    first_message_link = om.get_whatsapp_link(
        prospect['telefono'],
        prospect['nombre'],
        prospect['categoria'],
        prospect['slug'],
        prospect['ubicacion']
    )
    
    # Extraer el texto del mensaje (para enviarlo vía API, no solo el link)
    import urllib.parse
    parsed = urllib.parse.urlparse(first_message_link)
    query_params = urllib.parse.parse_qs(parsed.query)
    outreach_text = query_params['text'][0]
    
    print("\n📝 Mensaje de Outreach Generado:")
    print("-" * 30)
    print(outreach_text)
    print("-" * 30)
    
    # 4. Simular respuesta del cliente y respuesta del Bot
    print("\n🤖 Simulando interacción con SalesBot...")
    user_query = "¿Cuánto cuesta la web?"
    print(f"👤 Cliente dice: {user_query}")
    
    bot_response = bot.generate_response(user_query)
    print(f"🤖 Bot responde: {bot_response}")
    
    # 5. Intentar envío vía API (Solo si el usuario quiere probar el envío real)
    print("\n🚀 Intento de envío vía Evolution API...")
    # NOTA: En este entorno de prueba, probablemente fallará si no hay un WhatsApp conectado realmente
    # pero verificamos que la construcción de la petición sea correcta.
    success = om.send_whatsapp_message(prospect['telefono'], outreach_text)
    
    if success:
        print("✅ ÉXITO: La API aceptó el mensaje.")
    else:
        print(f"⚠️ AVISO: El envío falló (esperado si no hay sesión activa). Detalle: {result}")

if __name__ == "__main__":
    run_functional_test()
