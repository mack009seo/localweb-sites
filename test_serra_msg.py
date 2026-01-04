
import csv
import urllib.parse
from src.messaging.outreach_manager import OutreachManager

def print_test_message():
    om = OutreachManager()
    
    print("\n--- Mensaje para AMBULANCIES SERRA ---\n")
    
    # Simulate reading the specific prospect we just added
    prospect = {
        'nombre': 'Ambulancies Serra',
        'telefono': '+34696043437',
        'categoria': 'Servicio de Ambulancias',
        'ubicacion': 'Girona'
    }
    
    slug = 'ambulancies-serra'
    
    # Get the link
    link = om.get_whatsapp_link(
        prospect['telefono'],
        prospect['nombre'],
        prospect['categoria'],
        slug,
        prospect['ubicacion']
    )
    
    # Decode only for display
    parsed = urllib.parse.urlparse(link)
    query_params = urllib.parse.parse_qs(parsed.query)
    message_text = query_params['text'][0]
    
    print(f"🔹 Destinatario: {prospect['nombre']} ({prospect['telefono']})")
    print("-" * 40)
    print(message_text)
    print("-" * 40)

if __name__ == "__main__":
    print_test_message()
